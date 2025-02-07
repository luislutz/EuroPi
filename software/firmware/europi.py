from machine import Pin, PWM, ADC, I2C
from ssd1306 import SSD1306_I2C
from time import sleep, ticks_ms
from sys import exit


#Copyright 2021 Rory Allen

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License. 




#Import this library into your own programs using 'from europi import *'
#You can then use the inputs, outputs, knobs, and buttons as objects, and make use of the general purpose functions

#General use functions
def clamp(value, low, high): #Returns a value that is no lower than 'low' and no higher than 'high'
    return max(min(value, high), low)
        
def get_output_calibration_data(): #Retrieves the calibration data for the output
    with open('lib/calibration.txt', 'r') as data: #Open the text file in read mode
        data = data.readlines() #Create a list containing the lines read from the file
        OUTPUT_MULTIPLIER = float(data[2].replace('\n','')) #The third line is the output multiplier, convert to float as it is a string in the text file
    return OUTPUT_MULTIPLIER

def get_input_calibration_data(): #Retrieves the calibration data for the input
    with open('lib/calibration.txt', 'a+') as file: #Open the text file in 'all+' mode which means it will create a file if one isn't present
        data = file.readlines() #Create a list containing the lines read from the file
        if len(data) == 0: #If the file is empty
            file.write(str(0.003646677)+'\n'+str(-0.05753613)+'\n'+str(6347.393)) #Populate the file with default values
            data = file.readlines() #Re-read the file now it contains the default values
        
        INPUT_MULTIPLIER = float(data[0].replace('\n','')) #The first line is the input multiplier
        INPUT_OFFSET = float(data[1].replace('\n','')) #The second line is the input offset
        return INPUT_MULTIPLIER, INPUT_OFFSET

def sample_adc(adc, samples=256): #Over-samples the ADC and returns the average. Default 256 samples
    values = [] #Empty list to begin with
    for sample in range(samples): #Sample continuously for as many samples as specified
        values.append(adc.read_u16() / 16) #Add the value to values list. /16 as u16 reads as a 16 bit number but the ADC is only 12 bit
    return round(sum(values) / len(values)) #Return the average (mean) of the values list




class Display(SSD1306_I2C): #Class used to write to the OLED display
    def __init__(self, sda, scl, channel=0, freq=400000): #Takes the pin used for SDA, pin used for SCL, and then default values used for channel and i2c frequency
        self.i2c = I2C(channel, sda=Pin(sda), scl=Pin(scl), freq=freq)
        
        if len(self.i2c.scan()) == 0: #If no i2c devices are detected on the given channel
            print("\033[1;31;00mEuroPi Hardware Error:\nMake sure the OLED display is connected correctly") #Display a useful error message
            exit() #End the program
            
        super().__init__(128, 32, self.i2c)
    
    def clear(self): #Removes all filled pixels from the display
        self.fill(0)
    
    def centre_text(self, text): #Writes up to 3 lines of text (separated by \n) centred both vertically and horizontally
        self.clear() #Clears the display to prevent over-writing previously displayed information
        try: #Try in case the value sent is anything that cannot be .split()
            lines = text.split('\n')
        except:
            print("\033[1;31;00mEuroPi Software Error:\ncentre.text() only accepts string") #Display a useful error message
            return
        if len(lines) > 3: #If too many lines are passed (display is only capable of 3 lines)
            print("\033[1;31;00mEuroPi Software Error:\nOLED cannot print more than 3 lines of text") #Display a useful error message
            return
        center_line_height = int((-5 * len(lines)) + 25) #Calculations to convert the number of lines into the pixel height of the middle line
        heights = [center_line_height - 10, center_line_height, 2 * center_line_height] #Calculations to convert the line numbers into pixel heights for each line
        for line in lines:
            self.text(str(line), int(64 - (((len(line) * 5) + ((len(line) - 1) * 2)) / 2)), heights[lines.index(line)], 1) #Write each line to the display at the given height




class Output: #Class used to control the CV outputs
    def __init__(self, pin): #Takes only the GPIO pin being used for the output
        self.output = PWM(Pin(pin))
        self.output.freq(1000000) #This is specified as the default is too low to prevent audible PWM 'hum'
        self.pin = pin
        self.current_duty = 0
        self.output_multiplier = get_output_calibration_data() #Uses the calibration data stored in calibration.txt to scale the duty into a voltage
        
    def current_voltage(self): #A method used to see what the current voltage of the output is
        return self.current_duty / self.output_multiplier
        
    def duty(self, cycle): #A method to set the output based on a duty cycle of the PWM. Not very useful from a user perspective but required to be able to define voltage()
        cycle = int(cycle)
        self.output.duty_u16(clamp(cycle, 0, 65534)) #Clamps the duty cycle to 0-65534. By default values over or under that range will cycle over to the next limit which is not very useful
        self.current_duty = cycle
        
    def voltage(self, voltage): #Set the output voltage based on a float voltage
        self.duty(voltage * self.output_multiplier)
        
    def on(self): #Set the output voltage to 5. Useful if using the output as a faux-digital output
        self.voltage(5)
    
    def off(self): #Turns off the output (0V) 
        self.duty(0)
    
    def toggle(self): #Toggles the output between 0V and 5V depending on the current voltage.
        if self.current_duty > 500: #Arbitrary duty cycle to compare against, but some value is required otherwise toggle would only work when it begins at exactly 0V or 5V
            self.off()
        else:
            self.on()
        
    def value(self, value): #Sets the output to 0V or 5V depending on a binary input of 0 or 1. Useful if replicating the digital input for example
        if value == 1:
            self.on()
        else:
            self.off()




class AnalogueInput: #Class used to read the analogue input
    def __init__(self, pin):
        self.input = ADC(Pin(pin))
        self.input_multiplier, self.input_offset = get_input_calibration_data() #Retreives the calibration data from the calibration.txt file

    def read_duty(self, samples=256): #Reads the un-corrected duty cycle of the ADC
        return clamp(sample_adc(self.input, samples), 0, 65535)
    
    def read_voltage(self, samples=256): #Reads the voltage read by the ADC, corrected to convert both duty to voltage, and also correct the offset
        return clamp((self.read_duty(samples) * self.input_multiplier) + self.input_offset, 0, 12)




class Knob: #Class used to read the knob positions
    def __init__(self, pin):
        self.input = ADC(Pin(pin)) #The knobs are 'read' by analogue to digital converters
        
    def read_position(self, steps=100, samples=256): #Returns an int in the range of steps based on knob position.
        if not isinstance(steps, int):
            print("\033[1;31;00mPlease only use integer type with the read_position method")
            exit()
        return round(steps - ((sample_adc(self.input, samples) / 4096) * steps)) #If an integer is used, return a value from 0-integer based on the knob position

    def choice(self, values, samples=256): #Returns a choice from a list of values based on the knob position.
        if not isinstance(values, list):
            print("\033[1;31;00mPlease only use list type with the choice method")
            exit()
        return values[self.read_position(len(values)-1, samples)] #If a list is used, return the value in the list that is found at the position chosen by the knob position


class DigitalInput: #Class to handle any digital input, so is used for both the actual digital input and both buttons
    def __init__(self, pin, debounce_delay=100):
        self.pin = Pin(pin, Pin.IN)
        self.debounce_delay = debounce_delay  #Minimum time passed before a new trigger is allowed
        self.last_pressed = ticks_ms() #Time since last triggered, also used for debouncing
    
    def value(self): #Return the current value of the input
        return 1 - self.pin.value() #Both the digital input and buttons are normally high, and 'pulled' low when on, so this is flipped to be more intuitive (1 when on, 0 when off)

    def handler(self, func): #Allows the function that is run when triggered to be changed
        def bounce_wrapper(pin):
            if (ticks_ms() - self.last_pressed) > self.debounce_delay: #As long as the debounce time has been reached
                self.last_pressed = ticks_ms() #Reset the debounce counter to the current time
                func() #Run the chosen function
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=bounce_wrapper) 
        
    def reset_handler(self):
        self.pin.irq(trigger=Pin.IRQ_FALLING)




#Define all the I/O using the appropriate class and with the pins used
oled = Display(0,1)

k1 = Knob(27)
k2 = Knob(28)

b1 = DigitalInput(4)
b2 = DigitalInput(5)

din = DigitalInput(22, 0)
ain = AnalogueInput(26)

cv1 = Output(21)
cv2 = Output(20)
cv3 = Output(16)
cv4 = Output(17)
cv5 = Output(18)
cv6 = Output(19)

cvs = [cv1, cv2, cv3, cv4, cv5, cv6] #A list containing all the outputs which is generally useful
for cv in cvs: #When imported, all outputs are turned off. This is because otherwise the op-amps may be left 'floating' and output unpredictable voltages
    cv.duty(0)




#Calibration program. Run this program to calibrate the module
if __name__ == '__main__':
    def wait_for_range(low, high):
        while ain.read_duty() < low or ain.read_duty() > high:
            sleep(0.05)
            
    def centre_and_show(text):
        oled.centre_text(text)
        oled.show()
            
    def wait_and_show(low, high):
        wait_for_range(low, high)
        oled.centre_text('Calibrating...')
        oled.show()
        sleep(2)
            
    LOW_VOLTAGE = 1 #Change these values if you have easier access to alternative accurate voltage sources
    HIGH_VOLTAGE = 10 #Make sure you still use as wide a range as you can and keep it within the 0-10V range
    
    low_threshold_low = (270*LOW_VOLTAGE)-150
    low_threshold_high = (270*LOW_VOLTAGE)+150
    high_threshold_low = (270*HIGH_VOLTAGE)-150
    high_threshold_high = (270*HIGH_VOLTAGE)+150
    
    samples = 8192
    
    centre_and_show('Welcome\nto the\ncalibrator')
    sleep(3)
    if ain.read_duty() > 100:
        centre_and_show('Please unplug\nall patch\ncables')
    wait_for_range(0, 100)
    centre_and_show('Plug 1V into\nanalogue input')
    wait_and_show(low_threshold_low, low_threshold_high)
    low_reading = ain.read_duty(samples)
    centre_and_show('Now plug 10V\ninto analogue\ninput')
    wait_and_show(high_threshold_low, high_threshold_high)
    high_reading = ain.read_duty(samples)
    
    input_multiplier = (HIGH_VOLTAGE - LOW_VOLTAGE) / (high_reading - low_reading)
    input_offset = HIGH_VOLTAGE - (input_multiplier * high_reading)
    
    centre_and_show('Please unplug\nall patch\ncables')
    wait_for_range(0, 100)
    centre_and_show('Plug output 1\ninto analogue\ninput')
    cv1.duty(65534)
    wait_and_show(high_threshold_low, high_threshold_high)
    output_multiplier = 65534 / ((ain.read_duty(samples) * input_multiplier) + input_offset)

    with open('lib/calibration.txt', 'w') as file:
        file.write(str(input_multiplier) + '\n' + str(input_offset) + '\n' + str(output_multiplier))

    centre_and_show('Calibration\ncomplete!')

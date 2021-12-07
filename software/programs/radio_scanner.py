from europi import *
from time import sleep
from random import randint
import machine



def remap_knob(): 
    global knob_mapping
    knob_mapping += 1
    if knob_mapping == 3:
        knob_mapping = 0
        
    global display_time
    display_time = 0

def rotate_cvs():
    global cv_mapping
    new_cv_mapping = []
    for cv in cv_mapping[1:]: #Append all but the first (in order)
        new_cv_mapping.append(cv)
    new_cv_mapping.append(cv_mapping[0]) #Append the first
    
    cv_mapping = new_cv_mapping

def value_to_cv(value):
    return value * 16

def x_to_oled(x):
    return round(x * 0.0312)
def y_to_oled(y):
    return 31 - round(y * 0.0076)

cv_mapping = [cv1, cv2, cv3, cv4, cv5, cv6]
knob_mapping = 0 #0 = not used, 1 = knob 1, 2 = knob 2
knob_mapping_text = ['Off', 'Knob 1', 'Knob 2']

b1.handler(rotate_cvs)
din.handler(rotate_cvs)
b2.handler(remap_knob)

def do_step(x, y):
    oledx = x_to_oled(x)
    oledy = y_to_oled(y)
    
    cvx = value_to_cv(x)
    cvy = value_to_cv(y)
    
    oled.clear()
    oled.vline(oledx, 0, 32, 1)
    oled.hline(0, oledy, 128, 1)
    
    cv_mapping[0].duty(cvx) #0-65534
    cv_mapping[1].duty(cvy) #0-65534
    cv_mapping[2].duty(abs(cvy - cvx))
    cv_mapping[3].duty(32767 - cvx)
    cv_mapping[4].duty(32767 - cvy)
    cv_mapping[5].duty(32767 - abs(cvy - cvx))
    
    sleep(0.01)
    
    global display_time
    display_time += 0.01


def display_mapping(new_map):
    oled.fill_rect(0, 0, 64, 12, 1)
    oled.text(knob_mapping_text[new_map], 0, 2, 0)
    
    
    
display_time = 9999
while True:

    if knob_mapping != 1:
        x = k1.read_position(4096)
    else:
        x = ain.read_duty() + k1.read_position(4096)
        
    if knob_mapping != 2:
        y = k2.read_position(4096)
    else:
        y = ain.read_duty() + k2.read_position(4096)
    
    do_step(x, y)
    
    if display_time < 1:
        display_mapping(knob_mapping)
        
    oled.show()    
        

    
    
    
    #include this at the end of your loop to reboot Pi with both Buttons Pressed for longer
    
    #Dont forget to add the libraryy at the top: import machine
    
    millis = ticks_ms()
    Button1 = b1.value()
    Button2 = b2.value()
       
    
    if Button1 == 1 and Button1_toggle == 0:
        Button1_toggle = 1
        Button1_time = millis
    if Button1 == 0:
        Button1_toggle = 0
    
    if Button2 == 1 and Button2_toggle == 0:
        Button2_toggle = 1
        Button2_time = millis
    if Button2 == 0:
        Button2_toggle = 0
    
    if (Button1 == 1 and Button2 == 1 and millis-Button1_time > 1500 and millis-Button2_time > 1500):     
        oled.centre_text('Reboot...')  
        oled.show()
        cv1.voltage(0)
        cv2.voltage(0)
        cv3.voltage(0)
        cv4.voltage(0)
        cv5.voltage(0)
        cv6.voltage(0)
        sleep(1)
        machine.reset()
    
    


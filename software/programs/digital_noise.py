from europi import *
from random import randint
import machine

#machine.freq(250000000)

while True:
    
    
    if randint(0,1) == 0:
        cv1.duty(65534)
    else:
        cv1.off()
        
    if randint(0,1) == 0:
        cv2.duty(65534)
    else:
        cv2.off()
        
    if randint(0,1) == 0:
        cv3.duty(65534)
    else:
        cv3.off()
        
    if randint(0,1) == 0:
        cv4.duty(65534)
    else:
        cv4.off()
        
    if randint(0,1) == 0:
        cv5.duty(65534)
    else:
        cv5.off()
        
    if randint(0,1) == 0:
        cv6.duty(65534)
    else:
        cv6.off()
        
        
        
        
        
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
    

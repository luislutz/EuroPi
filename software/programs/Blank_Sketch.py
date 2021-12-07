from europi import *
import machine



#Insert Functions Here



while True:
    
    
    
    
    #Insert Loop Code here
    
    
    
    
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
    

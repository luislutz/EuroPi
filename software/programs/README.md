# Programs

This folder contains programs written by me (Rory) for the EuroPi, using the europi.py library.  
You will need to have this library installed on your EuroPi to use any of these programs, along with the SSD1306 module.  
Instructions on how to install both of these can be found in [programming_instructions.md](/software/programming_instructions.md).  

The europi.py library is often updated, and there is a chance that some of these updates may cause issues with older programs. I'll always try to rectify these at the same time as pushing the europi.py update, but if there are any I have missed, please add the bug as an [Issue](https://github.com/Allen-Synthesis/EuroPi/issues) on GitHub


---------Update-------- by Luis

this main.py script allows the use of multiple scripts without reconnecting to a PC. If you want to add more Programs you just have to add your script to the main.py code as i have done it for mine :) This has to be done manually for now... maybe more later. While a program is loaded, holding both of the buttons for 2 seconds will reboot the Pi and get you back in the selecting menu. Button 1 goes to the next script, Button 2 selects it. Dont forget to add the bit of code at the end of your looping statement to be able to reboot, and dont forget to include the machine library for scripts which dont have it already:






#include this at the end of your loop to reboot Pi with both Buttons Pressed for longer:
  
    
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
    


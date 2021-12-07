# Programs

This folder contains programs written by me (Rory) for the EuroPi, using the europi.py library.  
You will need to have this library installed on your EuroPi to use any of these programs, along with the SSD1306 module.  
Instructions on how to install both of these can be found in [programming_instructions.md](/software/programming_instructions.md).  

The europi.py library is often updated, and there is a chance that some of these updates may cause issues with older programs. I'll always try to rectify these at the same time as pushing the europi.py update, but if there are any I have missed, please add the bug as an [Issue](https://github.com/Allen-Synthesis/EuroPi/issues) on GitHub


---------Update-------- by Luis

this main.py script allows the use of multiple scripts without reconnecting to a PC. If you want to add more Programs you just have to add your script to the main.py code as i have done it for mine :) This has to be done manually for now... maybe more later. While a program is loaded, holding both of the buttons for 2 seconds will reboot the Pi and get you back in the selecting menu. Button 1 goes to the next script, Button 2 selects it. Dont forget to add the bit of code at the end of your looping statement to be able to reboot:





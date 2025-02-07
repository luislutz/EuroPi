# EuroPi

The EuroPi is a fully user reprogrammable module based on the Raspberry Pi Pico, which allows users to process inputs and controls to produce outputs based on code written in Python. The entire project is open-source.


This repository relates to the EuroPi module, however some users may be expecting to see what is now referred to as the 'EuroPi Prototype'. The repository for this (now deprecated) module [can be found here](https://github.com/roryjamesallen/EuroPi-Prototype)

You can find more about this (including a project diary) and other projects of mine on [my website](https://www.allensynthesis.co.uk)

![Imgur](https://i.imgur.com/wHL7558.png)

## Capabilities

* 6 0-10V Control Voltage outputs, each with indicator LED
* 2 Knobs with 12 bit resolution
* 2 Push Buttons
* 1 0-12V Control Voltage input with 12 bit resolution
* 1 Digital input for external clocking or gate sources
* 128x32 OLED Display
* I²C expansion header on the rear for extra sensors or outputs

### Improvements on the Prototype version

* All outputs are the full Eurorack unipolar range of 0-10V
* Two inputs, previously no way to accept input from other modules
* The buttons have hardware debouncing to allow users to change out capacitor values for reduced accidental 'double click'
* A 10 pin Eurorack shrouded power header is now used to prevent accidental reverse powering of the module
* The 5V supply for the Pico is now regulated down from the +12V supply, so no 5V rail is required from your Eurorack power supply
* The power supply is now diode protected to prevent back-powering your rack when the module is connected via USB
* All jacks are protected from overvoltage input (previously the Pico GPIO pin was directly exposed to any input, potentially leading to damage)

Please see the README.md files in the hardware and software folders for more specific information about each, including hardware specifications and how to use the *europi.py* library.


### Issues
If you find any bugs, either in the software, the hardware, or the documentation, please create an Issue by clicking the 'Issue' tab along the top.  
Please feel free to create any issue you see fit, I'll either attempt to fix it or explain it.  
There are Issue templates available, so please choose whichever is most relevant, depending on if your Issue is a hardware or software bug, if it's a documentation error or suggestion, if it's a question about the project as a whole, or a suggestion about the project as a whole.


### License

This module, and any documentation included in this repository, is entirely "free" software and hardware, under difference licenses depending on the software, hardware, and documentation itself.
  
Software: Apache 2.0
Hardware CERN OHL-S v2
Documentation: CC0 1.0
  
Anyone is welcome to design their own versions of the idea, or modify my designs.
The only thing I would ask is that you refrain from using the brand name 'Allen Synthesis' on your DIY builds if they have modified my files in any way, just to prevent any confusion if they end up being re-sold or distributed. This is in line with section 8.2 of the CERN license. You may use the brand name if you have simply copied the files from this repository to replicate without modification.
 
### Disclaimer
 
Recreate any of the files found in this repository at your own risk; I will attempt to solve any issues that you might have with my designs, but I can't guarantee that there are not minor bugs in any of the documents, both hardware and software.

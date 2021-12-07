from europi import *


Scripts = ['Radio Scanner','Digital Noise','CV','Sixd']
script = 0


cv1.voltage(0)
cv2.voltage(0)
cv3.voltage(0)
cv4.voltage(0)
cv5.voltage(0)
cv6.voltage(0)


oled.centre_text('Boot Up...')
oled.show()
sleep(1)



def next_script():
    global script
    script = script + 1
    if script >= 4:
        script = 0
    
    
    
def select_script():
    if (script == 0):
        import Radio_Scanner
                
    if (script == 1):
        import Digital_Noise
            
    if (script == 2):
         import CV
         
    if (script == 3):
         import Sixd
    
    
b1.handler(next_script)
b2.handler(select_script)

while True:
       
    oled.centre_text(Scripts[script])
    oled.show()
    
             
            

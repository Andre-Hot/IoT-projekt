# A simple LCD contrast control using PWM
from machine import Pin, PWM

#########################################################################
# CONFIGURATION
pin_lcd_contrast = 23
contrast_level = 250                        # Varies from LCD to LCD and wanted contrast level: 0-1023

#########################################################################
# OBJECT
lcd_contrast = PWM(Pin(pin_lcd_contrast))   # Create PWM object from a pin

#########################################################################    
# PROGRAM
print("LCD PWM contrast, remember to set the JP5 jumper to the left (R7) OR to the right (ESP PWM)\n")

lcd_contrast.freq(440)                      # Set PWM frequency

lcd_contrast.duty(contrast_level)
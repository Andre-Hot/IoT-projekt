# A program to show how to control an RGB (NeoPixel) with a single parameter (potentiometer)
# The program has two different color gradient: Red-Green-Blue or Rainbow
# https://www.instructables.com/How-to-Make-Proper-Rainbow-and-Random-Colors-With-/
from machine import ADC, Pin
from neopixel import NeoPixel
from time import sleep_ms
import math

########################################
# CONFIGURATION
number_neopixels = 12                  # The number of NeoPixel LEDs
pin_np = 26                            # The NeoPixel pin

pin_potmeter = 34                      # The potmeter pin

########################################
# OBJECTS
potmeter_adc = ADC(Pin(pin_potmeter))  # The potmeter object
potmeter_adc.width(ADC.WIDTH_10BIT)    # 10 bits
potmeter_adc.atten(ADC.ATTN_11DB)      # Full range: 3,3 V

np = NeoPixel(Pin(pin_np), number_neopixels) # The NeoPixel object

########################################
# VARIABLES
prev_red = -999
prev_green = -999

########################################
# FUNCTIONS
def rgb_gradient(value, max_value = 255):
    pi_2 = math.pi / 2.0
    angle = math.pi * value / max_value
    
    # Red
    if angle > pi_2:
        red = 0
    else:
        red = int(max_value * math.cos(angle))
        if red > max_value:
            red = max_value    

    # Green
    green = int(max_value * math.sin(angle))
    if green > max_value:
        green = max_value
    
    # Blue
    if angle < pi_2:
        blue = 0
    else:
        blue = -int(max_value * math.cos(angle))
        if blue > max_value:
            blue = max_value
        
    return (red, green, blue)
    
    
def rainbow_gradient(value, max_value = 255):
    pi_2 = math.pi / 2.0
    angle = 1.25 * math.pi * value / max_value
    
    # Red
    if angle < pi_2:
        red = int(max_value * math.cos(angle))
        if red > max_value:
            red = max_value    
    elif angle > math.pi:
        red = -int(max_value * math.sin(angle))
        if red > max_value:
            red = max_value    
    else:
        red = 0

    # Green
    if angle < math.pi:
        green = int(max_value * math.sin(angle))
        if green > max_value:
            green = max_value
    else:
        green = 0
    
    # Blue
    if angle < pi_2:
        blue = 0
    else:
        blue = -int(max_value * math.cos(angle))
        if blue > max_value:
            blue = max_value
        
    return (red, green, blue)    

########################################
# PROGRAM

while True:
    val = potmeter_adc.read()          # The potmeter returns a 10 bit value
    
    red, green, blue = rainbow_gradient(val >> 2) # Normalize the 8 bits
    if prev_red != red or prev_green != green:   
        # Fill each NeoPixels with the same RGB value
        for i in range(number_neopixels):
            np[i] = (red, green, blue)    
        
        np.write()
        
        prev_red = red
        prev_green = green
        
        sleep_ms(100)

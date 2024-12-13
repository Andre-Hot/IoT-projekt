# A simple LED and PWM demo program
from machine import Pin, PWM

#########################################################################
# CONFIGURATION
# Hardware
pin_led_red = 26                       # Red LED pin (must be a PWM able pin!)

# Red LED
led_red_freq = 40                      # The RED LED PWM frequency
led_red_duty = 512                     # The RED LED duty cycle, 0-1023, e.g. 50% -> 512

#########################################################################
# OBJECTS
led_red = PWM(Pin(pin_led_red))        # Create PWM object for the pin

#########################################################################
# PROGRAM
print("LED PWM test program")

led_red.freq(led_red_freq)             # Set PWM frequency
led_red.duty(led_red_duty)             # Set the duty cycle


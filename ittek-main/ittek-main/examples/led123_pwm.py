# A simple program to turn on LED1, LED2 and LED3 using PWM
from machine import DAC, Pin, PWM

###########################################################
# CONFIGURATION
pin_led1 = 26                           # Direct connection
pin_led2 = 12                           # Put jumper between JP1-MISO and JP6-GP2
pin_led3 = 13                           # Put jumper between JP1-MOSI and JP6-GP3

###########################################################
# PROGRAM
print("LED1, LED2 and LED3 PWM test program")
print("Remember to short \"JP1-MISO <-> JP6-GP2\" and \"JP1-MOSI <-> JP6-GP3\"")

led1_pwm = PWM(Pin(pin_led1))           # Create PWM object for the pin
led1_pwm.freq(70)                       # Set PWM frequency    
led1_pwm.duty(222)                      # Set the duty cycle, 0-1023, e.g. 50% -> 512

led2_pwm = PWM(Pin(pin_led2))           # Create PWM object for the pin
led2_pwm.freq(70)                       # Set PWM frequency, LED2 is active low!  
led2_pwm.duty(888)                      # Set the duty cycle, 0-1023, e.g. 50% -> 512

led3_pwm = PWM(Pin(pin_led3))           # Create PWM object for the pin
led3_pwm.freq(70)                       # Set PWM frequency    
led3_pwm.duty(999)                      # Set the duty cycle, 0-1023, e.g. 50% -> 512
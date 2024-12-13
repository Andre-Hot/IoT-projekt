# A simple potmeter test program
from machine import ADC, Pin, PWM
from time import sleep

import hw                              # Get the Educaboard ESP32 hardware definitions

########################################
# OBJECTS
potmeter_adc = ADC(Pin(hw.pin_potmeter))
potmeter_adc.atten(ADC.ATTN_11DB)      # Full range: 3,3 V and 12 bits

led1_pwm = PWM(Pin(hw.pin_led1))            # Create PWM object from a pin, 12 bits
led1_pwm.freq(40)                      # Set PWM frequency

########################################
# PROGRAM
print("Potmeter test, PWM on LED1\n")

while True:
    val = potmeter_adc.read()
    print(val)
    led1_pwm.duty(int(val >> 2))       # Convert 12 bits to 10 bits
    
    sleep(0.2)

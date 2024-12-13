from time import sleep

from lmt87 import LMT87

###########################################################
# CONFIGURATION
pin_lmt87 = 35

average = 1                            # The number of averages used

# Calibration values
t1 = 25.2
adc1 = 2659
t2 = 24.2
adc2 = 2697

###########################################################
# OBJECTS
temperature = LMT87(pin_lmt87)

###########################################################
# PROGRAM

print("LMT87 test\n")

print(temperature.calibrate(t1, adc1, t2, adc2))

while True:
    adc_val = temperature.get_adc_value()
    print(adc_val)
    
    sleep(1)
    
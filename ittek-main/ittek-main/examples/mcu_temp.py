# A simple to show the MCU temperature
import esp32
from time import sleep

###########################################################
# PROGRAM
while True:
    temp_farenheit = esp32.raw_temperature()
    temp_celcius = (temp_farenheit - 32) * 5 / 9
    
    print("MCU temp: %.f °C" % temp_celcius)
    
    sleep(0.5)
# A simple progrma that detects if a magnetic object is getting close to the ESP32
# Doesn't work when inserted into the Educaboard. No idea why

import esp32
from time import sleep

###########################################################
# PROGRAM
while True:
    val = esp32.hall_sensor()
    print(val)
    sleep(0.5)
# A simple push button test program
from machine import Pin
from time import sleep_ms

###########################################################
# OBJECTS
pb1 = Pin(4, Pin.IN)                 # External pull-up and debounce
pb2 = Pin(0, Pin.IN)                 # Direct connection with pull-up thus inverted

led1 = Pin(26, Pin.OUT)
led1.value(0)

###########################################################
# PROGRAM
print("Running push button test. Press PB1 and/or PB2 and watch LED1")

while True:
    val1 = pb1.value()
    val2 = pb2.value()
    
    if (val1 == 0) & (val2 == 0):
        led1.value(not led1.value())
        sleep_ms(50)
    elif val1 == 0:
        led1.value(1)
    elif val2 == 0:
        led1.value(not led1.value())
        sleep_ms(100)
    else:
        led1.value(0)
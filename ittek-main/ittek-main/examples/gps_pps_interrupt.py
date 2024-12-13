# A simple program to show how a GPS PPS can be used to make a H/W interrupt
from machine import Pin
import time

###########################################################
# FUNCTIONS
def interruptGpsPps(pin):
    ticks = time.ticks_ms()
    print("PPS! %d" % ticks)

###########################################################
# PROGRAM
print("GPS PPS interrupt\n")

pinGpsPps = Pin(5, Pin.IN)

pinGpsPps.irq(trigger = Pin.IRQ_RISING, handler = interruptGpsPps)
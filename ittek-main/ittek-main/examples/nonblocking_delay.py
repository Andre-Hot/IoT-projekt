# A small program showing how to implemen
# a non-blocking delayed event
from machine import Pin
import time

########################################
# CONFIGURATION
event_delay = 1000                     # The event delay in ms

########################################
# OBJECTS

########################################
# VARIABLES
next_time = 0                          # Non blocking flow control

########################################
# PROGRAM

print("Non blocking delayed event")

while True:
    # Here something else can be done
    
    # Delayed event
    if time.ticks_diff(time.ticks_ms(), next_time) >= 0:
        print("Event occured again")
        next_time = time.ticks_ms() + event_delay

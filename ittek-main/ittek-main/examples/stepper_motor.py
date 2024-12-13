# A simple progrma to control a 28BYJ-48 stepper motor
from machine import Pin
from time import sleep_ms

########################################
# CONFIGURATION
pin_stepper_in1 = 21                   # Using Educaboard LCD DB4-DB7 pins
pin_stepper_in2 = 22
pin_stepper_in3 = 32
pin_stepper_in4 = 33

########################################
# OBJECTS
IN1 = Pin(pin_stepper_in1, Pin.OUT)    # 28BYJ-48 controlling pins
IN2 = Pin(pin_stepper_in2, Pin.OUT)
IN3 = Pin(pin_stepper_in3, Pin.OUT)
IN4 = Pin(pin_stepper_in4, Pin.OUT)
stepper_pins = [IN1, IN2, IN3, IN4]

########################################
# FUNCTIONS
def stepper_motor(pins, sequence):
    for step in sequence:              # Run through the sequence
        for i in range(len(pins)):
            pins[i].value(step[i])
            sleep_ms(10)
            
    pins[-1].value(0)                  # Clear the pins before next step, "cosmetic"


def step_clockwise(pins):
    sequence_cw = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    stepper_motor(pins, sequence_cw)


def step_counter_clockwise(pins):
    sequence_ccw = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    stepper_motor(pins, sequence_ccw)
            
########################################
# PROGRAM
print("Stepper motor test program")

for i in range(512):
   step_clockwise(stepper_pins)

sleep_ms(1000)

for i in range(512):
   step_counter_clockwise(stepper_pins)

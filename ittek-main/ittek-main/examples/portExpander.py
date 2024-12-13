# https://rfzero.net/tutorials/communication/spi/

from machine import Pin, SPI
import time
from time import sleep_ms

from portExp_MCP23S08 import PortExp_MCP23S08

#############################################
# CONFIGURATION AND OBJECTS
# SPI BUS
hspi = SPI(1, 10000000)                     # Create the SPI bus object running at 10 MHz


# MCP23S08
pin_portexp_cs = 15                         # The MCP23S08 CS pin number
pin_portexp_int = 2                         # The MCP23S08 interrupt pin on the ESP32
portexp_addr = 0                            # The MSP23S08 subaddress, not a real SPI thing!
portExp = PortExp_MCP23S08(hspi, pin_portexp_cs, portexp_addr)

gp_t1           = 0                         # T1: base on NPN
gp_t2           = 1                         # T2: base on PNP
gp_led2         = 2                         # LED2: active low
gp_led3         = 3                         # LED3: active high

#############################################
# PROGRAM VARIABLES
# Non blocking flow control
timeLastToggle = 0
timeToggle = 500

spi_busy = False

#############################################
# FUNCTIONS
# The port expander interrupt handling
def portExp_interrupt(pin):
    global spi_busy
    
    print("Interrupt detected from ", end = '')
    
    # Find out which GP caused the interrupt
    spi_busy = True
    res = portExp.read_register(portExp.INTF)
    spi_busy = False
    
    if res & 0x10:                          # GP4
        print("the rotary encoder push button")
    else:
        print("an unknown device")

#############################################
# PROGRAM
# Configure the port expander
portExp.write_register(portExp.IODIR, 0xF0) # Bulk setting of GP7:4 as input and GP3:0 as output, datasheet 1.6.1
portExp.gp_pullup(4, portExp.ON)            # Enable pull-up on GP4 = RE PB, datasheet 1.6.7
portExp.gp_interrupt(4, portExp.ON)         # Enable interrupt on GP4, datasheet 1.6.3

# Prepare the interrupt handling from the port expander
portExp_interrupt_detect = Pin(pin_portexp_int, Pin.IN, Pin.PULL_UP)
portExp_interrupt_detect.irq(trigger = Pin.IRQ_FALLING, handler = portExp_interrupt)

print("SPI MCP23S08 test program, input GP7:4 and flipping GP3:0\n")

while True:
    if spi_busy == False:                   # Don't use the SPI bus if interrupt handling is going on
        if time.ticks_diff(time.ticks_ms(), timeLastToggle) > timeToggle:
            res = portExp.gp_get_value(gp_led2)
            if res == portExp.OFF:
                portExp.gp_set_value(gp_t1, portExp.ON)
                portExp.gp_set_value(gp_t2, portExp.ON)
                portExp.gp_set_value(gp_led2, portExp.ON)
                portExp.gp_set_value(gp_led3, portExp.ON)
            else:        
                portExp.gp_set_value(gp_t1, portExp.OFF)
                portExp.gp_set_value(gp_t2, portExp.OFF)
                portExp.gp_set_value(gp_led2, portExp.OFF)
                portExp.gp_set_value(gp_led3, portExp.OFF)
            
            timeLastToggle = time.ticks_ms()
# A simple ESP32 USB port to UART and back echo program
import sys, uselect
from machine import UART


#########################################################################
# CONFIGURATION
uart_port  = 2                              # ESP32 UART port
uart_speed = 9600                           # UART speed

#########################################################################
# OBJECTS AND VARIABLES
uart = UART(uart_port, uart_speed)          # UART object creation

usb = uselect.poll()                        # Set up an input polling object.
usb.register(sys.stdin, uselect.POLLIN)     # Register polling object.

#########################################################################
# PROGRAM
print("USB <-> UART 2 echo program")
print("Remember to short the UART 2 TX and RX pins")
print("Type something on the keyboard\n")

while True:
    # Receive data from the UART
    if uart.any() > 0:
        string = uart.read().decode()       # UART returns bytes. They have to be conv. to chars/a string
        print(string)                       # Echo received data
        
    # Receive data from the USB
    if usb.poll(0):
        ch = sys.stdin.read(1)              # Read one character at a time
        uart.write(ch)                      # Send it to the UART
        if ch == '\n':                      # This is strange. But it doesn't work without it
            print()
            
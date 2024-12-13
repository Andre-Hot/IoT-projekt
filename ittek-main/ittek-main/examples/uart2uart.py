# A simple ESP32 USB <-> UART <-> ESP32 USB program
import sys, uselect
from machine import UART

#########################################################################
# CONFIGURATION
uart_port  = 2                              # ESP32 UART port
uart_speed = 9600                           # UART speed

#########################################################################
# OBJECTS
uart = UART(uart_port, uart_speed)          # UART object creation, 8 bits, parity None, 1 stop bit

usb = uselect.poll()                        # Set up an input polling object
usb.register(sys.stdin, uselect.POLLIN)     # Register polling object

#########################################################################
# PROGRAM
print("ESP32 USB <-> UART <-> UART <-> ESP32 USB program")
print("Remember to connect TX1 -> RX2 and RX1 <- TX2")
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
        if (ch == "Hej"):
            print("Hej modtaget")
        if ch == '\n':                      # This is strange. But it doesn't work without it
            print()
    
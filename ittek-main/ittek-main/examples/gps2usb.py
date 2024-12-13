# A simple ESP32 UART to USB port echo program
from machine import UART

#########################################################################
# CONFIGURATION
uart_port  = 2                              # ESP32 UART port
uart_speed = 9600                           # UART speed

#########################################################################
# OBJECTS AND VARIABLES
uart = UART(uart_port, uart_speed)          # UART object creation

#########################################################################
# PROGRAM
print("UART -> USB echo program\n")

while True:
    # Receive data from the UART
    if uart.any() > 0:
        string = uart.readline().decode()   # UART returns bytes. They have to be conv. to chars/a string
        print(string.strip())               # Echo received data
        
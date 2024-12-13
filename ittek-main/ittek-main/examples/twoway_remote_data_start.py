# A simple ESP32 <-> UART remote data system incl. EEPROM use
import sys, uselect
from machine import ADC, I2C, Pin, UART

#########################################################################
# CONFIGURATION
# Remote
uart_remote_port = 1                   # Remote UART port
uart_remote_pin_tx = 33                # Remote UART TX pin
uart_remote_pin_rx = 32                # Remote UART RX pin
uart_remote_speed = 9600               # Remote UART speed

# User data
group_id = 99                          # Own group ID

#########################################################################
# OBJECTS
uart_remote = UART(uart_remote_port, baudrate = uart_remote_speed, tx = uart_remote_pin_tx, rx = uart_remote_pin_rx)# Remote UART object creation, 8N1

usb = uselect.poll()                   # Set up an input polling but non-blocking object
usb.register(sys.stdin, uselect.POLLIN)# Register polling object


#########################################################################
# PROGRAM
print("Two-way ESP32 remote data system\n")

while True:
    # Receive commands from and send responses to the remote UART
    if uart_remote.any() > 0:          # Check if there is any remote UART data available
        string = uart_remote.read().decode()  # UART returns bytes. They have to be conv. to chars/a string
        string = string.strip()        # Remove leading and trailing white spaces and control characters from received string
        print("Remote: " + string)     # Echo the received string on the USB port
        
    
    # Receive user input from the USB and send commands to the remote UART
    if usb.poll(0):                    # Check if there is any USB data available
        string = sys.stdin.readline()  # Read one line at a time
        sys.stdin.readline()           # WEIRD! - Needed to avoid a second handling of the same input
        string = string.strip()        # Remove leading and trailing white spaces and control characters from received string
        print("USB   : " + string)     # Echo the USB string on the USB port
        
        uart_remote.write(string + "\n")# Send the command to the remote unit add <LF> terminating character
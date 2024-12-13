# A simple program to show how to receive USB input one character at a time and without <Enter>
import sys, uselect

########################################
# OBJECTS
usb = uselect.poll()                   # Set up an input polling object.
usb.register(sys.stdin, uselect.POLLIN)# Register polling object.

########################################
# PROGRAM
print("USB input program")
print("Type something on the keyboard\n")

while True:
    # Receive data from the USB
    if usb.poll(0):
        ch = sys.stdin.read(1)         # Read one character at a time
        print(ch, end = '')

            

# GPS PPS program
from machine import UART

#########################################################################
# CONFIGURATION
gpsPort = 2                                 # ESP32 UART port
gpsSpeed = 9600                             # UART speed

#########################################################################
# OBJECTS
uart = UART(gpsPort, gpsSpeed)              # UART object creation

###########################################################
# VARIABLES
ba = bytearray([
    0xB5, 0x62,             # Header
    0x06, 0x31,             # ID 
    0x20, 0x00,             # Fixed length payload 32 bytes
    0x00,                   # 0, tpIdx
    0x01,                   # 1, reserved0
    0x00, 0x00,             # 2, reserved1
    0x32, 0x00,             # 4, antCableDelay
    0x00, 0x00,             # 6, rfGroupDelay
    0x05, 0x00, 0x00, 0x00, # 8, freqPeriod
    0x05, 0x00, 0x00, 0x00, # 12, freqPeriodLock
    0x00, 0x00, 0x00, 0x80, # 16, pulseLenRatio
    0x00, 0x00, 0x00, 0x80, # 20, pulseLenRatioLock
    0x00, 0x00, 0x00, 0x00, # 24, userConfigDelay
    0xEF, 0x00, 0x00, 0x00, # 28, Flags
    0x83, 0xFA,             # Checksum
    0x0D, 0x0A ])           # <CR><LF>


#######################################################################    
# PROGRAM
print("GPS PPS set to 5 Hz unconditionally program\n")

uart.write(ba, len(ba))     # Send the configuration frame to the GPS

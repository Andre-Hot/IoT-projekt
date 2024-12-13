# A simple ESP32 I2C EEPROM 24LC64 program
from machine import I2C
from eeprom_24xx64 import EEPROM_24xx64

#########################################################################
# OBJECTS
i2c = I2C(0)                           # I2C H/W 0 object

eeprom = EEPROM_24xx64(i2c, 0x50)      # The EEPROM object

#########################################################################
# PROGRAM
print("EEPROM 24LC64 via I2C H/W 0 test program\n")

eeprom.  <- do something here or delete the line

eeprom.print(0, 256)                   # Print the EEPROM

# A simple ESP32 I2C EEPROM 24LC64 program
from machine import I2C
from time import sleep_ms

########################################
# CONFIGURATION       
eeprom_i2c_addr = 0x50                 # EEPROM I2C address

eeprom_mem_address = indsæt-en-adresse-her

########################################
# OBJECTS
i2c = I2C(0)                           # I2C H/W 0

########################################
# PROGRAM
def write_byte(i2cAddr, addr, val):
    ba = bytearray(1)                
    ba[0] = val
    
    res = i2c.writeto_mem(i2cAddr, addr, ba, addrsize = 16)
    sleep_ms(5)                        # Needed due to EEPROM write timing

    return res

def read_byte(i2cAddr, addr):
    val = i2c.readfrom_mem(i2cAddr, addr, 1, addrsize = 16)
    return val[0]

print("EEPROM test program\n")

write_byte(eeprom_i2c_addr, eeprom_mem_address, indsæt-en-værdi-her)

value = read_byte(eeprom_i2c_addr, eeprom_mem_address)
print(value)
print("%d: %02d/0x%02X" % (eeprom_mem_address, value, value))

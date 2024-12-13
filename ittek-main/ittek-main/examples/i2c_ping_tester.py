# A simple program to ping an I2C device. Uses the funkyFunctions library
from machine import I2C

###########################################################
# CONFIGURATION
i2c_bus = 0                            # The I2C bus 
i2c_addr = 0x50                        # The I2C address to ping

###########################################################
# FUNCTIONS
def i2c_ping(i2c_bus, addr):
    
    i2c = I2C(i2c_bus)                 # Create a local I2C object
    
    try:
        i2c.readfrom(addr, 0)          # Try to read from the device
        return True
    except:
        return False

###########################################################
# PROGRAM
res = i2c_ping(i2c_bus, i2c_addr)
print(res)

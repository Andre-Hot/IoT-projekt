from machine import I2C, Pin, SoftI2C
from time import sleep

i2c = I2C(0)                           # SDA: 19, SCL: 18   http://docs.micropython.org/en/latest/esp32/quickref.html#hardware-i2c-bus


print("\nRunning I2C scanner on I2C H/W 0\n")

while True:
    devicesIdentified = i2c.scan()
    
    devicesCount = len(devicesIdentified)
    print("Total number of devices: %d" % devicesCount)

    if devicesCount == 112:            # There are 16 reserved addresses, thus not 128!
        print("Looks like the I2C bus pull-up resistors are missing")
    else:
        for i in range(devicesCount):
            print("Device found at address: 0x%02X" % devicesIdentified[i])
    
    print()                            # Blank line before next scan

    sleep(1)
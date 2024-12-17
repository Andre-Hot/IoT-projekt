from machine import I2C
from machine import Pin
from time import sleep
from mpu6050 import MPU6050
import sys

n = 2
np = NeoPixel(Pin(26, Pin.OUT), n)

#Initialisering af I2C objekt
i2c = I2C(0)     
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)

def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()
    
while True:
    try:
        # printer hele dictionary som returneres fra get_values metoden
        #print(imu.get_values()) 
        print(imu.get_values().get('acceleration x'))
        print(imu.get_values().get('acceleration y'))
        sleep(0.1)
        
    except KeyboardInterrupt:
        print("Ctrl+C pressed - exiting program.")
        sys.exit()

"""
while True:
    values = imu.get_values()
    if  values["acceleration z"] < -15000:
        set_color(100, 0, 0)
        sleep(1)
    else:
        set_color(0, 0, 0)
    print(values["acceleration z"])
    sleep(0.05)
"""

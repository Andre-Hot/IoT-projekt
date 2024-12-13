from mpu6050 import MPU6050
from time import sleep
from machine import Pin, I2C

i2c = I2C(0)
imu = MPU6050(i2c)

while True:
    values = imu.get_values()
    print(values["acceleration z"])
    sleep(0.05) 
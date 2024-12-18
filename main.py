rom mpu6050 import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50
from time import sleep
from machine import Pin, I2C, ADC
from dht import DHT11
from gpio_lcd import GpioLcd
from machine import UART
from gps_simple import GPS_SIMPLE

gps_port = 2                                 # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600

uart = UART(gps_port, gps_speed)             # UART object creation
gps = GPS_SIMPLE(uart)


i2c = I2C(0)
imu = MPU6050(i2c)
dht11 = DHT11(Pin(0, Pin.IN))

potmeter_adc = ADC(Pin(36))
potmeter_adc.atten(ADC.ATTN_11DB)      # Full range: 3,3 V and 12 bits

adc1 = 1790
U1 = 3.0
adc2 = 2580
U2 = 4.2

a = (U1-U2)/(adc1-adc2)
b = U2 - a*adc2

def batt_voltage(adc_v):
    u_batt = a*adc_v+b
    return u_batt

#Procent:
# 3V = 0%
# 4.2V = 100%
def batt_percentage(u_batt):
    without_offset = (u_batt-3)
    normalized = without_offset / (4.2-3.0)
    percent = normalized * 100
    return percent

previous_battery_percent = 0

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)

custom_chr = bytearray([0b00111,
                        0b00101,
                        0b00111,
                        0b00000,
                        0b00000,
                        0b00000,
                        0b00000,
                        0b00000])


while True:
    if gps.receive_nmea_data():
        print(f"Latitude        : {gps.get_latitude():.8f}")
        print(f"Longitude       : {gps.get_longitude():.8f}")
        print(f"Validity        : {gps.get_validity()}")
        print(f"Speed           : km/t {gps.get_speed()}")
        lcd.move_to(0, 1)
        lcd.putstr(f"Latitude: {gps.get_latitude():.2f}")
        lcd.move_to(0, 2)
        lcd.putstr(f"Longitude: {gps.get_longitude():.2f}")
        lcd.move_to(0, 3)
        lcd.putstr(f"km/t: {gps.get_speed():.2f}")
        lcd.move_to(11, 3)
        lcd.putstr(f"Ret:{gps.get_course():.1f}\n")
        
    dht11.measure()
    temperature = dht11.temperature()
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Temp:")
    lcd.move_to(5, 0)
    lcd.putstr(str(temperature))
    lcd.move_to(7, 0)
    lcd.custom_char(0, custom_chr)
    lcd.putchar(chr(0))
    lcd.move_to(8, 0)
    lcd.putstr("C")
    
     
    val = potmeter_adc.read()
    u_batt = batt_voltage(val)
    percent = batt_percentage(u_batt)
    
    print('ADC value:',val)
    print('U_adc', (3.3/4096*val))
    print('U_batt', batt_voltage(val))
    print('U percentage', batt_percentage(batt_voltage(val)))
    print('*'*10)
    print(percent)
    lcd.move_to(10, 0)
    lcd.putstr(f"Bat: {percent:.1f}%")
    
    
    
    
    
    

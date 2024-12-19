from mpu6050 import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50
from time import sleep
from machine import Pin, I2C, ADC
from dht import DHT11
from gpio_lcd import GpioLcd
from machine import UART
from gps_simple import GPS_SIMPLE
from uthingsboard.client import TBDeviceMqttClient
from machine import PWM, DAC
from machine import Pin, time_pulse_us
import secrets

trigger = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)
buzzer = PWM(14, Pin.OUT)
pin_led1 = 26
pin_led3 = 13
gps_port = 2                                 # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600

uart = UART(gps_port, gps_speed)             # UART object creation
gps = GPS_SIMPLE(uart)

client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()  

i2c = I2C(0, freq=100000)
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

def measure_distance():
    #Send 10us puls til trigger pin
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()
    
    #Mål den tid det tager for echo pin at modtage signal
    duration = time_pulse_us(echo, 1, 30000)
    
    distance_cm = (duration * 0.0343) / 2
    return distance_cm

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

def get_lat_lon():
    lat = lon = None                       # create lat and lon variable with None as default value
    if gps.receive_nmea_data():            # check if data is recieved
                                           # check if the data is valid
        if gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            lat = str(gps.get_latitude())  # store latitude in lat variable
            lon = str(gps.get_longitude()) # stor longitude in lon variable
            return lat, lon                # multiple return values, needs unpacking or it will be tuple format
        else:                              # if latitude and longitude are invalid
            print(f"GPS data to server not valid:\nlatitude: {lat}\nlongtitude: {lon}")
            return False
    else:
        return False


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
    try:    
        print(imu.get_values())#.get("temperature celsius"))
    except:
        print('error reading imu')
        
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
    
    lat_lon = get_lat_lon()
    if not lat_lon:
        lat_lon = [0,0]
    # store telemetry in dictionary      
    telemetry = {'latitude': lat_lon[0],
                 'longitude': lat_lon[1],
                 'Battery': percent,
                 'speed': gps.get_speed(1),
                 'retning': gps.get_course(),
                 'temperatur':temperature}

    client.send_telemetry(telemetry)
    

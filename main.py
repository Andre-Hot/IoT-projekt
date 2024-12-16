from uthingsboard.client import TBDeviceMqttClient
from machine import ADC, Pin, PWM
from machine import Pin, I2C, ADC
from time import sleep
from gpio_lcd import GpioLcd
from machine import reset, UART
from gps_simple import GPS_SIMPLE


lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)
i2c = I2C(0)
gps_port = 2                             
gps_speed = 9600                          
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_SIMPLE(uart)

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
                                           # Make client object to connect to thingsboard
client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()                           # Connecting to ThingsBoard
print("connected to thingsboard, starting to send and receive data")


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

while True:
    
    val = potmeter_adc.read()
    u_batt = batt_voltage(val)
    percent = batt_percentage(u_batt)

    print('ADC value:',val)
    print('U_adc', (3.3/4096*val))
    print('U_batt', batt_voltage(val))
    print('U percentage', batt_percentage(batt_voltage(val)))
    print('*'*10)
     
    lcd.clear()
    lcd.putstr(f"Batteri: {percent:.1f}%")
    sleep(0.2)
    
    try:
        print(f"free memory: {gc.mem_free()}") # monitor memory left
        
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        
        if gps.receive_nmea_data():
            speed = gps.get_speed()  # Get speed from GPS data
   
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
            lcd.move_to(10, 0)
            
        lat_lon = get_lat_lon()           # multiple returns in tuple format
        print(lat_lon)
        if lat_lon:
                                          # store telemetry in dictionary      
            telemetry = {'latitude': lat_lon[0],
                         'longitude': lat_lon[1],
                         'speed': speed,
                         'temperature': temperature,
                         }
            client.send_telemetry(telemetry) #Sending telemetry  
        sleep(1)                          # send telemetry once every second
    except KeyboardInterrupt:
        print("Disconnected!")
        client.disconnect()               # Disconnecting from ThingsBoard
        reset()                           # reset ESP32


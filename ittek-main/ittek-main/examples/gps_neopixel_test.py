# A program to test a GPS RX and NeoPixel ring
from machine import ADC, Pin, UART
from neopixel import NeoPixel
from time import sleep, sleep_ms
import math

from gpio_lcd import GpioLcd

from gps_simple import GPS_SIMPLE


########################################
# CONFIGURATION
number_neopixels = 12                  # The number of NeoPixel LEDs
pin_np = 26                            # The NeoPixel pin

pin_potmeter = 34                      # The potmeter pin


########################################
# OBJECTS
lcd = GpioLcd(rs_pin = Pin(27), enable_pin = Pin(25),   # Create the LCD object
              d4_pin = Pin(33), d5_pin = Pin(32), d6_pin = Pin(21), d7_pin = Pin(22),
              num_lines = 4, num_columns = 20)

uart = UART(2, 9600)                   # UART object creation
gps = GPS_SIMPLE(uart, False)          # GPS object creation

potmeter_adc = ADC(Pin(pin_potmeter))  # The potmeter object
potmeter_adc.width(ADC.WIDTH_10BIT)    # 10 bits
potmeter_adc.atten(ADC.ATTN_11DB)      # Full range: 3,3 V

np = NeoPixel(Pin(pin_np), number_neopixels) # The NeoPixel object


########################################
# VARIABLES
prev_red = -999
prev_green = -999


########################################
# FUNCTIONS
def ctrlC():
    try:
        pass
    except KeyboardInterrupt:
        print("Ctrl+C pressed - exiting program.")
        sys.exit() 
   
    
def rainbow_gradient(value, max_value = 255):
    pi_2 = math.pi / 2.0
    angle = 1.25 * math.pi * value / max_value
    
    # Red
    if angle < pi_2:
        red = int(max_value * math.cos(angle))
        if red > max_value:
            red = max_value    
    elif angle > math.pi:
        red = -int(max_value * math.sin(angle))
        if red > max_value:
            red = max_value    
    else:
        red = 0

    # Green
    if angle < math.pi:
        green = int(max_value * math.sin(angle))
        if green > max_value:
            green = max_value
    else:
        green = 0
    
    # Blue
    if angle < pi_2:
        blue = 0
    else:
        blue = -int(max_value * math.cos(angle))
        if blue > max_value:
            blue = max_value
        
    return (red, green, blue)    


########################################
# PROGRAM
y = 1

while True:
    # GPS
    if (gps.receive_nmea_data()):
        lcd.move_to(0, 0)
        lcd.putstr("%04d-%02d-%02d" % (gps.get_utc_year(), gps.get_utc_month(), gps.get_utc_day()))
        
        lcd.move_to(12, 0)
        lcd.putstr("%02d:%02d:%02d" % (gps.get_utc_hours(), gps.get_utc_minutes(), gps.get_utc_seconds()))

        lcd.move_to(0, y)
        lcd.putstr(gps.get_latest_frame()[0:20])
        y = y + 1
        if y > 3:
            y = 1
    
    # NeoPixel
    val = potmeter_adc.read()          # The potmeter returns a 10 bit value
    
    red, green, blue = rainbow_gradient(val >> 2) # Normalize the 8 bits
    if prev_red != red or prev_green != green:   
        # Fill each NeoPixels with the same RGB value
        for i in range(number_neopixels):
            np[i] = (red, green, blue)    
        
        np.write()
        
        prev_red = red
        prev_green = green
        
        sleep_ms(100)


    ctrlC()
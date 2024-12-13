# Smart Home sensor program
# MicroPython and ESP32 https://docs.micropython.org/en/latest/esp32/quickref.html
# https://docs.micropython.org/en/latest/library/espnow.html

import network
import espnow

from machine import ADC, Pin
import time

# Modules specific to this program 
import smarthome_misc as misc

########################################
# OWN MODULES
from adc_sub import ADC_substitute

########################################
# CONFIGURATION
dashboard_mac_address = b'\xA1\xB2\xC3\xD4\xE5\xF6' # MAC address of dashboard (Educaboard). Byte string format!

# Sensor
sensor_id = "Template"                 # The sensor ID
pin_sensor_1 = 32                      # The sensor GPIO input pin 1
pin_sensor_2 = 33                      # The sensor GPIO input pin 2

# LED
pin_led = 26                           # The LED pin

duration_on = 50                       # Duration of LED on in ms
duration_off = 2000                    # Duration of LED off in ms

# Battery
pin_battery = 34                       # The battery measurement input pin, ADC1_6

########################################
# OBJECTS
# ESP-NOW
sta = network.WLAN(network.STA_IF)     # Or network.AP_IF
sta.active(True)                       # WLAN interface must be active to send()/recv()

en = espnow.ESPNow()                   # ESP-NOW object
en.active(True)                        # Make ESP-NOW active

# Sensor
sensor = Pin(pin_sensor_1, Pin.IN)

# LED
led = Pin(pin_led, Pin.OUT)            # The on LED object

# Battery
battery = ADC_substitute(pin_battery)  # The battery object
ip1 = 1234                             # Insert own measured value here when the battery is fully discharged
ip2 = 3210                             # Insert own measured value here when the battery is fully charged
bp1 = 0                                # Battery percentage when fully discharged
bp2 = 100                              # Battery percentage when fully charged
alpha = (bp2 - bp1) / (ip2 - ip1)      # alpha is the slope in the first degree equation bp = alpha * input + beta
beta = bp1 - alpha * ip1               # beta is the crossing point on the y axis

########################################
# VARIABLES
# Previous values
prev_sensor_value = -999               # The previous value from the sensor
prev_bat_pct = -1                      # The previous battery percentage value

next_time = 0                          # Non blocking flow control

########################################
# FUNCTIONS
def get_battery_percentage():          # The battery voltage percentage
    ip = battery.read_adc()            # Either use this or the one below. Remove if not used
    ip = battery.read_voltage()        # Either use this or the one abore. Remove if not used
    #print(ip)                          # Only used during calibration. Comment out after calibration is complete
    
    bp = alpha * ip + beta             # Calculate the battery percentage based on the measured input value
    bp = int(bp)                       # Take the interger value
    
    # Make sure noise on the readings don't result in invalid values
    if bp < 0:                         
        bp = 0
    elif bp > 100:
        bp = 100
    
    return bp


def led_blink():                       # The asymmetric LED blink
    global next_time
    
    if time.ticks_diff(time.ticks_ms(), next_time) > 0:
        if led.value() == 1:
            led.value(0)
            next_time = time.ticks_ms() + duration_off
        else:
            led.value(1)
            next_time = time.ticks_ms() + duration_on
                  
                  
def pack_data(mac, sid, bp, val):
    string = "0000"                    # The frame version number, four digits
    string += '|' + mac
    string += '|' + sid
    string += '|' + str(time.ticks_ms())
    string += '|' + str(bp)
    string += '|' + str(val)

    return string

########################################
# PROGRAM

# INITIALIZATION
sensor_mac_address = misc.get_mac_address() # MAC address

# ESP-NOW
en.add_peer(dashboard_mac_address)     # Must add_peer() before send()
en.send(dashboard_mac_address, sensor_id + " ready", False)

print(sensor_id + ", " + sensor_mac_address + ", ready")

# MAIN (super loop)
while True:
    # Measure the battery percentage
    bat_pct = get_battery_percentage()
    
    # LED blink
    led_blink()
    
    # Check the sensor
    sensor_value = 0                   # Replace with the specific way to interface with the sensor here

    # Send data if there is a change (this principle saves power)
    if bat_pct != prev_bat_pct or sensor_value != prev_sensor_value:
        data_string = pack_data(sensor_mac_address, sensor_id, bat_pct, sensor_value)
        
        print("Sending: " + data_string)
        try:
            en.send(dashboard_mac_address, data_string, False)
        except ValueError as e:
            print("Error sending the message: " + str(e))  
        
        # Update the previous values for use next time
        prev_bat_pct = bat_pct
        prev_sensor_value = sensor_value

    # Check to see if there is a message
    host, msg = en.recv(10)
    if msg:
        msg = msg.decode("utf-8")
        print(msg)
        #Do something useful here

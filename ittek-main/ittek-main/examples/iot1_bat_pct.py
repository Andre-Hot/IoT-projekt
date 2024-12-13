# IoT1: battery voltage measured through a voltage divider
from machine import ADC, Pin
from time import sleep

#########################################################################
# CONFIGURATION
pin_adc_bat = 33                       # The battery ADC pin

k_u_pin = 1.642                        # Actual voltages measured on
k_u_bat = 3.229                        # the pin and on the battery
k = k_u_bat / k_u_pin                  # Actual ratio btwn voltages on battery and pin

#########################################################################
# OBJECTS
adc_bat = ADC(Pin(pin_adc_bat))        # The ADC object built from the ADC class
adc_bat.atten(ADC.ATTN_11DB)           # Full range: 3,3 V

#########################################################################
# FUNCTIONS
def read_battery_voltage_avg64():      # Average over 64 times to reduce fluctuations
    adc_val = 0
    for i in range(64):
        adc_val += adc_bat.read()      
    return adc_val >> 6                # >> is fast divide by 2^6 = 64

#########################################################################
# PROGRAM
print("IoT1 battery measurement\n")

while True:
    # 1: Get the battery ADC value
    adc_bat_val = read_battery_voltage_avg64()  # alt.: adc_bat_val = adc_bat.read()
    print("ADC value           : %4d" % adc_bat_val)

    # 2: Convert battery ADC value to the voltage on the input pin
    u_pin = adc_bat_val * 3.3 / 4095 + 0.15  # 150 mV offset due to the ESP32
    print("Voltage on input pin: %.2f V" % u_pin)
   
    # 3: Convert the voltage on the input pin to the batery voltage
    u_bat = u_pin * k
    print("Battery voltage     : %.2f V" % u_bat)

    # 4: Convert the battery voltage to a percentage
    # (x1;y1) = (3,0 V; 0%), (x2;y2) = (4,2 V; 100%)
    # y = ax + b => Upct = a * Ubat + b
    u_pct = 83.333 * u_bat - 250
    print("Battery percentage  : %4d %%\n" % u_pct)

    sleep(1)
    
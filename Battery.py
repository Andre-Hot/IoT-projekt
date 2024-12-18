from machine import ADC, Pin, PWM
from time import sleep
from gpio_lcd import GpioLcd

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)

potmeter_adc = ADC(Pin(36))
potmeter_adc.atten(ADC.ATTN_11DB)

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

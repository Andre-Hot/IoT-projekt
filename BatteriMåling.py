from machine import ADC, Pin, PWM
from time import sleep

# Initialisering af ADC og spændingsberegning
potmeter_adc = ADC(Pin(34))
potmeter_adc.atten(ADC.ATTN_11DB)  # Fuldt måleområde: 3.3 V og 12 bit

# Kalibrering
adc1 = 2390
U1 = 4.1
adc2 = 2080
U2 = 3.6

a = (U1-U2)/(adc1-adc2)
b = U2 - a*adc2

# Funktion til batterispænding
def batt_voltage(adc_v):
    u_batt = a * adc_v + b
    return u_batt

# Funktion til batteriprocent
def batt_percentage(u_batt):
    without_offset = (u_batt - 3)
    normalized = without_offset / (4.2-3.0)
    percent = normalized * 100
    return max(0, min(100, percent))  # Begræns til intervallet 0% - 100%

# Funktion til visning af opladningstilstand
def display_battery_status(percent):
    # Skab en simpel grafik baseret på batteriprocenten
    full_blocks = int(percent // 10)  # Antal fyldte blokke
    empty_blocks = 10 - full_blocks  # Resten er tomme blokke
    battery_bar = "[" + ("#" * full_blocks) + (" " * empty_blocks) + "]"
    return f"{battery_bar} {percent:.1f}%"

# Læsning og visning i loop
while True:
    val = potmeter_adc.read()
    u_batt = batt_voltage(val)  # Beregn batterispænding
    percent = batt_percentage(u_batt)  # Beregn batteriprocent
    status = display_battery_status(percent)  # Generer batterigrafik

    # Print værdier og opladningstilstand
    print('ADC værdi:', val)
    print('Batterispænding (V):', round(u_batt, 2))
    print('Batteri status:', status)
    print('*' * 20)

    sleep(0.5)

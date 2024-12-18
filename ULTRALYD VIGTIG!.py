from machine import PWM, DAC
from machine import Pin, time_pulse_us
import time

# Definer pins
trigger = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)
buzzer = PWM(14, Pin.OUT),
pin_led1 = 26
pin_led3 = 13

def measure_distance():
    # Send 10us puls til trigger pin
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()
    
    # Mål den tid det tager for echo pin at modtage signal
    duration = time_pulse_us(echo, 1, 30000)
    
    # Beregn afstand i cm (lydens hastighed er ca. 34300 cm/s)
    distance_cm = (duration * 0.0343) / 2
    return distance_cm

'''
while True:
    distance = measure_distance()
    print(distance)
    if distance <= 100:
        print("Distance: {:.2f} cm".format(distance))
    else:
        print("INGEN BAGVED")
    time.sleep(1)
'''    
#sensor = PWM(trigger_pin=4, echo_pin=5)

# Opsætning af LEDs og buzzer
red_led = Pin(26, Pin.OUT)
green_led = Pin(13, Pin.OUT)
buzzer = PWM(Pin(14), freq=1000)

def main():
    while True:
        distance = measure_distance()
        print('Distance:', distance, 'cm')
        
        if distance < 100 and distance >= 0:
            red_led.value(1)
            green_led.value(0)
            buzzer.duty(512)  # Tænd buzzer
        else:
            red_led.value(0)
            green_led.value(1)
            buzzer.duty(0)  # Sluk buzzer
        
        time.sleep(0.1)

main()

    



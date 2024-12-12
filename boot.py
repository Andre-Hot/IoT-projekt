import network
import time

SSID = 'Andre'         # Erstat med din WiFi's navn (SSID)
PASSWORD = ''  # Erstat med din WiFi-adgangskode

wifi = network.WLAN(network.STA_IF)

wifi.active(True)

wifi.connect(SSID, PASSWORD)

print("Forbinder til WiFi...")
while not wifi.isconnected():
    time.sleep(1)

print("Forbundet til WiFi!")
print("IP adresse:", wifi.ifconfig()[0])  # Udskriv IP-adressen, som ESP32 har fået tildelt
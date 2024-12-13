# https://docs.micropython.org/en/latest/library/espnow.html
import network, espnow, time

# A WLAN interface must be active to send()/recv()
station = network.WLAN(network.STA_IF)  # Or network.AP_IF
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)
peer = b'\xab\xcd\xef\x01\x23\x45'   # MAC address of peer's wifi interface
esp_now.add_peer(peer)      # Must add_peer() before send()
print(esp_now.get_peers())

esp_now.send(peer, "Starting...")
for i in range(10000):
    esp_now.send(peer, str(i), True)
    time.sleep(1)
    print(esp_now.get_peers())
   
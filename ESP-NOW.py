import network
import espnow


wifi = network.WLAN(network.STA_IF)

wifi.active(True)

wifi.connect("Andre", "Andre1234")
print("Searching Wifi....")

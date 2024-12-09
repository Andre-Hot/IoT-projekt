import network

wlan = network.WLAN(network.STA_IF)

wlan.active(True)

if wlan.active():
    
    mac_address = wlan.config("mac")
    print(mac_address)
    print("Device Mac Address: ", ":".join(["{:02X}".format(byte) for byte in mac_address]))
else:
    print("Wi-fi is not active.")
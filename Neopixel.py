from neopixel import NeoPixel
from machine import Pin

n = 16 # number of pixels in the Neopixel ring
p = 12 # pin atached to Neopixel ring
np = NeoPixel(Pin(p, Pin.OUT), n) # create NeoPixel instance

np[0] = (255, 255, 255) # set pixel 0 to white (r, g b)

np[3] = (255, 0, 0) # set pixel 3 to red (r, g b)

np[6] = (0, 255, 0) # set pixel 6 to green (r, g b)

np[9] = (0, 0, 255) # set pixel 9 to blue (r, g b)

np[11] = (0, 255, 255) # set pixel 11 to cyan (r, g b)

np.write() # write to pixels 

# GPS program
from machine import UART
from gps_simple import GPS_SIMPLE

import _thread
import time

#########################################################################
# CONFIGURATION
gpsPort = 2                                 # ESP32 UART port, Educaboard ESP32 default UART port
gpsSpeed = 9600                             # UART speed, defauls u-blox speed
gpsEcho = True                              # Echo NMEA frames: True or False
gpsAllNMEA = False                          # Enable all NMEA frames: True or False

threaded = False                            # Use threaded (True) or loop (False)

#########################################################################
# OBJECTS
uart = UART(gpsPort, gpsSpeed)              # UART object creation

gps = GPS_SIMPLE(uart, gpsAllNMEA)          # GPS object creation

#########################################################################    
# PROGRAM
print("GPS test program\n")

def gps_tread():
    while True:
        if (gps.receive_nmea_data(gpsEcho)):
            print("UTC YYYY-MM-DD: %04d-%02d-%02d" % (gps.get_utc_year(), gps.get_utc_month(), gps.get_utc_day()))
            print("UTC HH:MM:SS  : %02d:%02d:%02d" % (gps.get_utc_hours(), gps.get_utc_minutes(), gps.get_utc_seconds()))
            print("Latitude      : %.8f" % gps.get_latitude())
            print("Longitude     : %.8f" % gps.get_longitude())
            print("Altitude      : %.1f m" % gps.get_altitude())
            print("Fix quality   : %d" % gps.get_fix_quality())
            print("Satellites    : %d" % gps.get_satellites())
            print("HDOP          : %2.1f" % gps.get_hdop())
            print("Validity      : %s" % gps.get_validity())
            print("Speed         : %.1f m/s" % gps.get_speed())
            print("Course        : %.1f°" % gps.get_course())
            
            print("Frames RXed   : 0x%04X" % gps.get_frames_received())            
            
            print()
    
        time.sleep(1)
 
 
if threaded:
    _thread.start_new_thread(gps_tread, ())
else:
    while True:
        if (gps.receive_nmea_data(gpsEcho)):
            print("UTC YYYY-MM-DD: %04d-%02d-%02d" % (gps.get_utc_year(), gps.get_utc_month(), gps.get_utc_day()))
            print("UTC HH:MM:SS  : %02d:%02d:%02d" % (gps.get_utc_hours(), gps.get_utc_minutes(), gps.get_utc_seconds()))
            print("Latitude      : %.8f" % gps.get_latitude())
            print("Longitude     : %.8f" % gps.get_longitude())
            print("Altitude      : %.1f m" % gps.get_altitude())
            print("Fix quality   : %d" % gps.get_fix_quality())
            print("Satellites    : %d" % gps.get_satellites())
            print("HDOP          : %.1f" % gps.get_hdop())
            print("Validity      : %s" % gps.get_validity())
            print("Speed         : %.1f m/s" % gps.get_speed())
            print("Course        : %.1f°" % gps.get_course())
            
            print("Frames RXed   : 0x%04X" % gps.get_frames_received())

            print()        

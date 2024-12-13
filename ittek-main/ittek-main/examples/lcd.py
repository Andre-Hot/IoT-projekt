from machine import Pin

from gpio_lcd import GpioLcd

print("LCD 20x4 write test. Adjust contrast if necessary")

# Create the LCD object
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)

lcd.putstr('* Educaboard ESP32 *')

lcd.move_to(1, 1)
lcd.putstr('KEA ITT www.kea.dk')

lcd.move_to(0, 2)
lcd.putstr('Indlejrede Systemer')

lcd.move_to(0, 3)
lcd.putstr('og Programmering   ')
happy_face = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x11, 0x0E, 0x00])
lcd.custom_char(0, happy_face)
lcd.putchar(chr(0))


# #The following line of codes should be tested one by one according to your needs
#
# #1. To print a string to the LCD, you can use
# #2. Now, to clear the display.
# lcd.clear()
# #3. and to exactly position the cursor location
# # If you do not set the cursor position,
# # the character will be displayed in the
# # default cursor position starting from
# # 0, x and 0, y location which is the top left-hand side.
# # There are other useful functions we can use in using the LCD.
# #4. Show the cursor
# lcd.show_cursor()
# #5. Hide the cursor
# lcd.hide_cursor()
# #6. Turn ON blinking cursor
# lcd.blink_cursor_on()
# #7. Turn OFF blinking cursor
# lcd.blink_cursor_off()
# #8. Disable display
# lcd.display_off()
# this will only hide the characters
# #9. Enable display
# lcd.display_on()
# #10. Turn backlight OFF
# lcd.backlight_off()
# #11. Turn backlight ON
# lcd.backlight_on()
# # 12. Print a single character
# lcd.putchar('x')
# but this will only print 1 character
# #13. Display a custom characters using hex codes, you can create the character from <a href="https://maxpromer.github.io/LCD-Character-Creator/">here.</a>
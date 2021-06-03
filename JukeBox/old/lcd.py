from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

lcd = CharLCD(cols=16, rows=2, pin_rs=14, pin_e=15, pins_data=[18, 23, 24, 25], numbering_mode=GPIO.BCM)
lcd.write_string(u'Hello world!')

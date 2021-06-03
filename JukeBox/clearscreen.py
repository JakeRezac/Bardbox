import RPi.GPIO as GPIO	#For button controls
import DispLib

lcd = DispLib.LCD(bit_mode=DispLib.MODE_4BIT, pin_rs=14, pin_e=15, pins_data=[18,23,24,25])

lcd.clear_disp()
#lcd.disp_crs_on()
#lcd.home_crsr()


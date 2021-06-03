import RPi.GPIO as GPIO	#For button controls
import DispLib

#lcd = DispLib.LCD(bit_mode=DispLib.MODE_4BIT, pin_rs=14, pin_e=15, pins_data=[18,23,24,25])
#whoops pins 13 and 18 are reserved for audio output on pi zero so lets see if we can free them up
lcd = DispLib.LCD(bit_mode=DispLib.MODE_4BIT, pin_rs=14, pin_e=15, pins_data=[4,23,24,25])

lcd.disp_crs_on()
lcd.home_crsr()
lcd.clear_disp()

message = "I'ts finally working!!!"
#message = "TEST TEST TEST TEST TEST"
lcd.write_str(message)
#
##lcd.move_crsr(13, DispLib.LEFT)
##lcd.move_crsr(24, DispLib.LEFT)
##
#while (True):
#	lcd.move_disp(1, DispLib.LEFT)
#	DispLib.microSleep(400000)

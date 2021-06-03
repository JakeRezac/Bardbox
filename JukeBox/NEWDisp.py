import RPi.GPIO as GPIO	#For button controls
import NEWDispLib

lcd = NEWDispLib.LCD(bit_mode=NEWDispLib.MODE_4BIT, pin_rs=14, pin_e=15, pins_data=[4,23,24,25])

lcd.move_disp(1)
lcd.move_disp(2)
lcd.move_disp(4)
lcd.move_disp(-4)


lcd.move_crsr(1)
lcd.move_crsr(2)

#NEWDispLib.microSleep(1000000)
#lcd.home_crsr()

message = "I'ts finally working!!!"
lcd.write_str(message)

NEWDispLib.microSleep(1000000)
lcd.move_disp(1)
lcd.move_disp(2)
lcd.move_disp(4)
lcd.move_disp(-4)


lcd.move_crsr(1)
lcd.move_crsr(2)

NEWDispLib.microSleep(1000000)
lcd.home_crsr()

#		TO DO
#	1.  figure out why disp_crsr is acting oddly
#	2.  Get a write character function working consistently
#	3.  Get a write string funciton working consistently
#	4.  Get a function to move crsr to a position and write there
#	5.  Get a function to move a subsection of text in a lop

#No clue if the bottom 3 lines are working at all
#lcd.disp_crsr(0b0,0b0,0b0)
#NEWDispLib.microSleep(1000000)
#lcd.disp_crsr(0b1,0b1,0b1)
#NEWDispLib.microSleep(1000000)
#lcd.disp_crsr(0b1,0b0,0b1)
#NEWDispLib.microSleep(1000000)
#lcd.disp_crsr(0b1,0b1,0b0)
#NEWDispLib.microSleep(1000000)
#lcd.disp_crsr(0b1,0b0,0b0)
#
##lcd.move_crsr(13, DispLib.LEFT)
##lcd.move_crsr(24, DispLib.LEFT)
##
#while (True):
#	lcd.move_disp(1, DispLib.LEFT)
#	DispLib.microSleep(400000)

### 	Known Good Functions ###
#	move_disp
#	init
#	move_crsr (pretty sure)
#	home_crsr (pretty sure)

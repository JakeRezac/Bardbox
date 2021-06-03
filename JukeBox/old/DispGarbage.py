import RPi.GPIO as GPIO	#For button controls
import DispLib

lcd = DispLib.LCD(bit_mode=DispLib.MODE_4BIT, pin_rs=14, pin_e=15, pins_data=[18,23,24,25])

print("clearing display")
DispLib.microSleep(1000)
lcd.clearDisp()

print("homing display")
DispLib.microSleep(1000)
lcd.homeDisp()

print("writing...")
DispLib.microSleep(1000)
lcd.writeStr("HEYO WORLD!!!!")


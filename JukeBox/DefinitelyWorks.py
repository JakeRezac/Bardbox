import RPi.GPIO as GPIO	#For button controls
import DispLib

lcd = DispLib.LCD(bit_mode=DispLib.MODE_4BIT, pin_rs=14, pin_e=15, pins_data=[18,23,24,25])


#Hard Reset by using 8bit Function Set Instruction
instruction = 0b0011
GPIO.output(lcd.pin_rs, 0)

lcd._write4bits(instruction)

#Function Set		| 0 | 0 | 1 |8/4|2/1|10/7| * | * | 20 - 3F
instruction = 0b00101000
GPIO.output(lcd.pin_rs, 0)

lcd._write4bits(instruction >> 4)
lcd._write4bits(instruction)

#Disp On/Off & Crsr	| 0 | 0 | 0 | 0 | 1 | D  | U | B | 08 - 0F
instruction = 0b00001111
GPIO.output(lcd.pin_rs, 0)

lcd._write4bits(instruction >> 4)
lcd._write4bits(instruction)

#Disp & Crsr home	| 0 | 0 | 0 | 0 | 0 | 0  | 1 | * | 02 - 03
instruction = 0b00000010
GPIO.output(lcd.pin_rs, 0)

lcd._write4bits(instruction >> 4)
lcd._write4bits(instruction)

#Clr Disp		| 0 | 0 | 0 | 0 | 0 | 0  | 0 | 1 | 01 
instruction = 0b00000001
GPIO.output(lcd.pin_rs, 0)

lcd._write4bits(instruction >> 4)
lcd._write4bits(instruction)

#Char Entry Mode	| 0 | 0 | 0 | 0 | 0 | 1  |I/D| S | 04 - 07
#---------------------------------------------------------------------------
instruction = 0b00000110 #I/D = 1, S = 0 :entr char &  move crsr to next spot 
GPIO.output(lcd.pin_rs, 0)
#
lcd._write4bits(instruction >> 4)
lcd._write4bits(instruction)
#
#for char in ("----------------########################||||||||||||||||************************"):
for char in ("Hello There"):
#for char in ("Hello There"):
	data = ord(char) #ord() converts a char to its ascii table number
	GPIO.output(lcd.pin_rs, 1)
	
	lcd._write4bits(data >> 4)
	lcd._write4bits(data)

#Command    		|D7 |D6 |D5 |D4 |D3 |D2 |D1 |D0 | Hex
#-----------------------------------------------------------------
#Clr Disp		| 0 | 0 | 0 | 0 | 0 | 0  | 0 | 1 | 01 
#Disp & Crsr home	| 0 | 0 | 0 | 0 | 0 | 0  | 1 | * | 02 - 03
#Char Entry Mode	| 0 | 0 | 0 | 0 | 0 | 1  |I/D| S | 04 - 07
#Disp On/Off & Crsr	| 0 | 0 | 0 | 0 | 1 | D  | U | B | 08 - 0F
#Disp / Crsr Shift	| 0 | 0 | 0 | 1 |D/C|R/L | * | * | 10 - 1F
#Function Set		| 0 | 0 | 1 |8/4|2/1|10/7| * | * | 20 - 3F
#Set CGRAM Address	| 0 | 1 | A | A | A | A  | A | A | 40 - 7F

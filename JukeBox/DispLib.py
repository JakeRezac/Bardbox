"""
	This Library is heavily based on the RPLCD Library
"""
import RPi.GPIO as GPIO
import time
import string

#def microSleep(microseconds):
#	time.sleep(microseconds / 1000000.0)
def microSleep(microseconds):
	time.sleep(microseconds / 1000000.0)

#------------------------------------------------------------
#			GLOBALS 
#------------------------------------------------------------
#Char Entry Mode Bits
INCREMENT = 0x02
DECREMENT = 0x00
SHIFT     = 0x01
NOSHIFT   = 0x00

# Flags for RS pin modes
RS_INSTRUCTION = 0x00
RS_DATA = 0x01

# Flags for function set
MODE_8BIT = 0x10
MODE_4BIT = 0x00
LINE_NUM_2 = 0x08
LINE_NUM_1 = 0x00
CHAR_HEIGHT_10 = 0x04
CHAR_HEIGHT_7 = 0x00

#  Display / Cursor Shift
RIGHT = 0b00000100
LEFT  = 0b00000000

"""
DATA
-------------
	 Most basic characters are stored in a memory
	 location corresponding to their ASCII table entry

	 Char  | Hex	 | Dec
	 ---------------------------------
	 space | 20      | 32
	   %   | 25      | 37
	   :   | 3A      | 58
	 0 - 9 | 30 - 39 | 48 - 57
	 A - Z | 41 - 5A | 65 - 90
	 a - z | 61 - 7A | 97 - 122
	
INSTRUCTIONS
-------------
    	Instruction    		|D7 |D6 |D5 |D4 |D3 |D2 |D1 |D0 | Hex
	-----------------------------------------------------------------
	Clr Disp		| 0 | 0 | 0 | 0 | 0 | 0  | 0 | 1 | 01 
	Disp & Crsr home	| 0 | 0 | 0 | 0 | 0 | 0  | 1 | * | 02 - 03
	Char Entry Mode		| 0 | 0 | 0 | 0 | 0 | 1  |I/D| S | 04 - 07
	Disp On/Off & Crsr	| 0 | 0 | 0 | 0 | 1 | D  | U | B | 08 - 0F
	Disp / Crsr Shift	| 0 | 0 | 0 | 1 |D/C|R/L | * | * | 10 - 1F
	Function Set		| 0 | 0 | 1 |8/4|2/1|10/7| * | * | 20 - 3F
	Set CGRAM Address	| 0 | 1 | A | A | A | A  | A | A | 40 - 7F
	Set DDRAM Address	| 1 | A | A | A | A | A  | A | A | 80 - FF
	
	*   : not important to the functions operation

	I/D : 1 = increment, 	 0 = Decrement
	S   : 1 = Disp shift on  0 = Disp shift off
		S |I/D|
		0 | 0 | Cursor Decrement dont shift current char
		0 | 1 | Cursor Increment dont shift current char
		1 | 0 | Cursor Decrement shift current char with it
		1 | 1 | Cursor Increment shift current char with it

	D   : 1 = Disp ON	 0 = Disp OFF
	U   : 1 = Crsr Undrln	 0 = Underline OFF
	B   : 1 = Crsr Blink ON  0 = Crsr Blink OFF

	D/C : 1 = Disp Shift	 0 = Cursor Move
	R/L : 1 = Right Shift	 0 = Left Shift

	8/4 : 1 = 8bit Intrface	 0 = 4bit Interface
	2/1 : 1 = 2 line mode	 0 = 1 line mode
	10/7: 1 = 5x10 format	 0 = 5x7 dot format (Char. Dimensions WxH)

	CGRAM is some advanced shit for custom characters

	DDRAM is used to set address for DDRAM which informs characters
	      in posisitons on our display
"""
class LCD():
	def __init__(self, numbering_mode=GPIO.BCM, bit_mode=MODE_8BIT, line_num=LINE_NUM_2, char_height=CHAR_HEIGHT_10, pin_rs=None, pin_rw=None, pin_e=None, pins_data=None):
		#Move parameters into class variables	
		self.numbering_mode 	= numbering_mode
		self.bit_mode  		= bit_mode
		self.line_num 		= line_num
		self.char_height 	= char_height
		self.pin_rs    		= pin_rs
		self.pin_rw    		= pin_rw
		self.pin_e     		= pin_e
		self.pins_data 		= pins_data
		
		#GPIO Setup
		GPIO.setmode(self.numbering_mode)

		GPIO.setup(self.pin_rs, GPIO.OUT)
		GPIO.setup(self.pin_e, GPIO.OUT)
		if self.pin_rw is not None:
			GPIO.setup(pin_rw, GPIO.OUT)
		for pin in self.pins_data:
			GPIO.setup(pin, GPIO.OUT)

		# Initialization
		microSleep(50)
		GPIO.output(self.pin_rs, 0)
		GPIO.output(self.pin_e, 0)
		if self.pin_rw is not None:
		    GPIO.output(self.pin_rw, 0)

		microSleep(50)

		#Hard Reset by sending 0011**** 3 times 
		instruction = 0b00110000
		if self.bit_mode is MODE_8BIT:
			self._send(instruction, RS_INSTRUCTION)
			self._send(instruction, RS_INSTRUCTION)
			self._send(instruction, RS_INSTRUCTION)

		else:	#Follow up with 0010**** if in 4-bit mode
			instruction = instruction >> 4
			self._send(instruction, RS_INSTRUCTION)# We send an "8bit" instruction to set us to 8bit mode
			self._send(instruction, RS_INSTRUCTION)# Send twice in case of being in 4 bit mode

			instruction = 0b0010	      # Now the true 4 bit instructions are sent
			self._send(instruction, RS_INSTRUCTION)
			#self._write4bits(0b0000)     #A second nibble shouldnt need to be sent here

		#Call an actual FunctionSet with our desired settings
		self._functionset()


	#------------------------------------------------------------
	#		Background Methods
	#------------------------------------------------------------
	def _pulse_e(self):
		"""Pulse enable pin """
	    	GPIO.output(self.pin_e, 0)
		microSleep(1)
	    	GPIO.output(self.pin_e, 1)
		microSleep(3)	# E pulse time is 230nS min
	    	GPIO.output(self.pin_e, 0)
		microSleep(40) 	# commands need > 37us to settle
		#microSleep(1)
	    	#GPIO.output(self.pin_e, 0)
		#microSleep(1)
	    	#GPIO.output(self.pin_e, 1)
		#microSleep(2)
	    	#GPIO.output(self.pin_e, 0)
		#microSleep(40) 	# commands need > 37us to settle

	def _write4bits(self, value):
		"""Write to D4 - D7"""
		for i in range(4):
			bit = (value >> i) & 0x01
			GPIO.output(self.pins_data[i], bit)
		self._pulse_e()
		microSleep(1) # Address Hold Time is 10nS min

	def _write8bits(self, value):
		"""Write to D0 - D7"""
		for i in range(8):
			bit = (value >> i) & 0x01
			GPIO.output(self.pins_data[i], bit)
		self._pulse_e()
		microSleep(1) # Address Hold Time is 10nS min

	def _functionset(self):	
		"""
				  D7  D6  D5  D4  D3  D2   D1  D0  Decimal
		FunctionSet	| 0 | 0 | 1 |8/4|2/1|10/7| * | * | 20 - 3F

		8/4	1 = 8-bit mode 	0 = 4-bit mode
		2/1	1 = 2 line mode	0 = 1 line mode
		10/7	1 = 10 pixel	0 = 7 pixel		(char height)
		*	UNIMPORTANT BIT
		"""
	
		# Instruciton is set based on __init__ () arguments
		instruction = 0b00100000
		instruction = instruction | self.bit_mode
		instruction = instruction | self.line_num
		instruction = instruction | self.char_height
		
		self._send(instruction, RS_INSTRUCTION)
	
	#------------------------------------------------------------
	def _send(self, value, rs_mode):
		"""Value is:
			Char Data   for rs_mode = RS_DATA
			Instruction for rs_mode = RS_INSTRUCTION

		bit_mode is selected automatically based on self.bit_mode
		"""
		# Choose RS_DATA or RS_INSTRUCTION
	    	GPIO.output(self.pin_rs, rs_mode)	

		# If the RW pin is used, set it to low in order to write.
		if self.pin_rw is not None:
		    GPIO.output(self.pin_rw, 0)	

		microSleep(1) # Address Setup Time is 40nS minimum
		
		# Write data out in chunks of 4 or 8 bit dependng on bit_mode
		if self.bit_mode is MODE_8BIT:
		    self._write8bits(value)
		else:
		    self._write4bits(value >> 4)
		    self._write4bits(value)

	#------------------------------------------------------------
	#			End-User Methods
	#------------------------------------------------------------
	def clear_disp(self):
		self._send(0x01, RS_INSTRUCTION)
		microSleep(125) #needs additional time after 40us min

	def home_crsr(self):
		self._send(0x02, RS_INSTRUCTION)
		microSleep(125) #needs additional time after 40us min

	def disp_crs_on(self, disp=0x01, underline=0x01, blink=0x01):
		#We're having some real trouble getting this thing to work
		#Changing D U or B options just dont do anything
		#disp, underline, and blink are just always on
		"""
				      D7  D6  D5  D4  D3  D2  D1  D0
		    Disp/Crs On/Off  | 0 | 0 | 0 | 0 | 1 | D | U | B | 

			D - 	1 = display on 	, 0 = display off
			U - 	1 = underln on	, 0 = underline off
			B - 	1 = blink on 	, 0 = blink off
		"""
		instruction = 0b00001000
		instruction = instruction | ( disp << 2 )
		instruction = instruction | ( underline << 1 )
		instruction = instruction | ( blink )
		#print("Instruction disp_crs_on: " + str(instruction))

		self._send(instruction, RS_INSTRUCTION)

	def write_str(self, string, inc_or_dec=INCREMENT, shift=NOSHIFT):	
		"""
		uses 'Char Entry Mode Bits' globals

		Char Entry Mode	| 0 | 0 | 0 | 0 | 0 | 1  |I/D| S | 04 - 07

		inc_or_dec 	: 1 = increment, 	 0 = Decrement
		shift		: 1 = Disp shift on  0 = Disp shift off
			i_or_c|shift|
			  0   |  0  | Crsor Dec dont shift current char
			  0   |  1  | Crsor Dec shift current char
			  1   |  0  | Crsor Inc dont shift current char
			              actually enters char and moves forward
			  1   |  1  | Crsor Inc shift current char
		"""
		instruction = 0x03
		instruction = instruction | inc_or_dec
		instruction = instruction | shift

		self._send(instruction, RS_INSTRUCTION)
		for char in string:
			data = ord(char)
			self._send(data, RS_DATA)		

	def move_crsr(self, num, direction=RIGHT):
		"""
		-moves <num> spaces 
		-direction: 1 = move crsr right, 0 = move crsr left


				 D7  D6  D5  D4  D3  D2   D1  D0 
		Disp/Crsr Shift	| 0 | 0 | 0 | 1 |D/C|R/L | * | * |
	
		D/C : 1 = Disp Shift	 0 = Cursor Move
		R/L : 1 = Right Shift	 0 = Left Shift
		"""

		instruction = 0b00010000
		instruction = instruction | (direction)
		
		for i in range(num):
			self._send(instruction, RS_INSTRUCTION)


	def move_disp(self, num, direction=RIGHT):
		"""
		-moves <num> spaces 
		-direction: 1 = move crsr right, 0 = move crsr left


				 D7  D6  D5  D4  D3  D2   D1  D0 
		Disp/Crsr Shift	| 0 | 0 | 0 | 1 |D/C|R/L | * | * |
	
		D/C : 1 = Disp Shift	 0 = Cursor Move
		R/L : 1 = Right Shift	 0 = Left Shift
		"""

		instruction = 0b00011000
		instruction = instruction | (direction)
		
		for i in range(num):
			self._send(instruction, RS_INSTRUCTION)



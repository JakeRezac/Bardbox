import RPi.GPIO as GPIO	#For button controls
import time		#For reading buttons

#Library Assumes GPIO pins are connected to :
#	Globl Variable holds GPIO pin number for GPIO methods
#
#	Pin | Description 	| Globl |  Alternative to GPIO 
#	--------------------------------------------------
#	 E  | Enable	        |   E   |      	      
#	 RS | Register Select  	|   RS  |             
#	 RW | Read / !(write)	|   RW  | If you're only writing Tie Low
#	 D7 | Data		|   D7  |   ---               
#	 D6 | Data		|   D6  |      |___ Used for 8 or 4 bit mode
#	 D5 | Data		|   D5  |      |              
#	 D4 | Data		|   D4  |   ---               
#	 D3 | Data		|   D3  |   ---          
#	 D2 | Data		|   D2  |      |___ Not needed for 4-bit mode 
#	 D1 | Data		|   D1  |      |
#	 D0 | Data		|   D0  |   ---          

GPIO.setmode(GPIO.BCM) 		# Use Broad Com GPIO pin numbering
#GPIO.setmode(GPIO.BOARD) 	# Use Physical Board GPIO Pin number

GPIO.setwarnings(False)

#GPIO and Global Variable Setup
#----------------------------------------------------------------
E = 15
GPIO.setup(E, GPIO.OUT)
RS = 14
GPIO.setup(RS, GPIO.OUT)

D4 = 18
GPIO.setup(D4, GPIO.OUT)
D5 = 23
GPIO.setup(D5, GPIO.OUT)
D6 = 24
GPIO.setup(D6, GPIO.OUT)
D7 = 25
GPIO.setup(D7, GPIO.OUT)

#Function Definitions
#----------------------------------------------------------------
def PulseE():
	#time.sleep(40.0 / 1000000000)		#address setup time, Tas min of 40 nS
	time.sleep(0.0001)		
	GPIO.output(E, GPIO.HIGH)
	#time.sleep(230.0 / 1000000000)		#E must be pulsed for min of 230 nS
	time.sleep(0.0001)		
	GPIO.output(E, GPIO.LOW)		
	#time.sleep(10.0 / 1000000000)		#address hold tim, Tah min of 10 nS
	time.sleep(0.0001)		
	return
	
def Init4bit(Lines, Height):
	""" Both args are bits
		Lines 
			1 = 2 Lines 	0 = 1 Line

	    	Height 	(controls char height on screen)	
			1 = 10 pixels	0 = 7 pixels
	"""
	GPIO.output(RS, GPIO.LOW)

	#Send an "8-bit" command to set bit mode to 4
	#We do not care about the LSBs
	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.HIGH)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)	
	PulseE()

	#Resend Command as 2, 4-bit commands to make sure LSBs are set right
	#D0 doesn't  matter
	#D1 doesn't  matter
	GPIO.output(D6, Height)
	GPIO.output(D7, Lines)
	PulseE()
	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.HIGH)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)
	PulseE()
	return

def Clear4bit():
	GPIO.output(RS, GPIO.LOW)

	GPIO.output(D4, GPIO.HIGH)
	GPIO.output(D5, GPIO.LOW)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)
	PulseE()
	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.LOW)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)
	PulseE()
	return

def home4bit():
	GPIO.output(RS, GPIO.LOW)

	#GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.HIGH)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)	
	PulseE()
	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.LOW)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)	
	PulseE()

def PushChar4bit():
	#Send Command
	GPIO.output(RS, GPIO.LOW)

	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.HIGH)
	GPIO.output(D6, GPIO.HIGH)
	GPIO.output(D7, GPIO.LOW)	
	PulseE()
	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.LOW)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)
	PulseE()
	
	#Send Character 00000101
	GPIO.output(RS, GPIO.HIGH)

	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.LOW)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.LOW)	
	PulseE()
	GPIO.output(D4, GPIO.LOW)
	GPIO.output(D5, GPIO.HIGH)
	GPIO.output(D6, GPIO.LOW)
	GPIO.output(D7, GPIO.HIGH)
	PulseE()

	return

	

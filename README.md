Current Status
--------------------------
So Pygame comes default on raspbian OS, is well documented by sparkfun, and
has example code that more or less proves it will work for my application.

I've put this project off an entire year because I wanted to understand every
little nuiance of playing audio. This is clearly not the right way to learn.

	WE'LL BE MOVING FORWARD WITH THE PYGAME LIBRARY AND AMIXER LINUX TOOL 


Libraries
--------------------------
Pygame
	-This package comes default in Raspian and has the 'mixer' module
		from pygame import mixer
	-Example code and documentation available on sparkfun.com
	-GPIO support?

	mixer module
		sound = mixer.Sound('filename.wav')
		sound.play()

os
	-default python module for looking at directories

RPi.GPIO
	-this will handle GPIO input

SmBUS
	-used for general I2C communication 
	-default on Raspian OS
	-used for communicating with ADC on volume knob
		
adafruit-ads1x15
	-this ADC is fucking impossible 
	-im just gonna use adarfuits library
	-maybe ill read it to see how they use the 
	 SMBUS module
LCD is controlled with my own homebrew library. 
Heavily based on (if not a blatant copy of) RPLCD.
(If we ever release this as a 'product' we'll switch 
	to using the RPLCD lib)

GPIO Pins
--------------------------
The current plan is to implement everything with pushbuttons, 
including volume control. In order to use a volume control pot
an external ADCs will need to be hooked up to the pi first

Som ADCs will communicate with the pi using i2c so this volume
implementation won't use up any GPIO pins

Reading seems to indicate that GPIO 0 - 27 can technically be used
however we like. some GPIO pins are called GPIO_GEN pins, but this
is some old raspi history bullshit and does not effect the user

LCD Screen 
--------------------------
	The current goal is to make my own light weight library from scratch.
	I'll be assuming my bootleg LCD takes the same input as the common 44780's
	
	Most all of the LCD controls needed will be handled by the Data pins. 
	Other pins will be hard wired somehow. (ground, power, contrast, RW, etc.)
	
	Writing to the screen is a matter of writing to:
	-----------------------------------------------
	- Data (Dx) Pins
	- Register Select (RS) Pin
	- Enable (E) Pin			[pulse it high to 'send' cmd] 
	- RS and R/~W pins may be important as well
		* You may need to keep an eye on the "Busy Flag" (BF)
		When RS = 0, and R/~W = 1 D7 will show the state of the 
		BF
			1 = 44780 is busy with internal operation
			    and will not accept instruction
			0 = instruction will be accepted

		Instructions must only be written after ensuring BF = 0
		*So this flag is not necessary to check if you use sufficient delays
		*infact, not even the RPLCD library checks BF it seems

	   RS |R/~W| Operation                           
	   ---------------------------------------------------------
	   0  | 0 |IR write as internal op. (disp clear,etc.)  cmd write
	   0  | 1 |BF flag at D7, address counter at D0-D6     data write
	   1  | 0 |DR write as internal op. (DR to DDRAM / CGRAM) command read
	   1  | 1 |DR read as an internal op.(DDRAM or CGRAM to DR) data read

	Process	
	--------------
	To send instructions and write to the screen
		-Set E LOW		(to disable read/write)
		-Set RS LOW 		(LOW to send Instructions or HIGH to send character data)
		-Write to D pins 	(to send instruction based on command table or char based on char table)
		-Pulse E HIGH 		(to start Read/Write Process)
			Google 44780 Character map for a table of all of the 44780's 
			characters

	Reading info from the screen is not used in this project (so RW has just been tied LOW)
	
	Instruction table
		RS = R/~W = 0 whenever sending instructions from table 
		below (pulse enable between each command)
	
    	Command    		|D7 |D6 |D5 |D4 |D3 |D2 |D1 |D0 | Hex
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

		************************************
		Turns out to be a very simple way to 
		write to the screen 
		************************************

		the command uses D6-D0 to set address.
		For a 16 Character Wide Display:
		80-8F will be top row
		C0-CF will be bottom row

		1) send DDRAM comand to Instruction Reg
		RS|RW|D7|D6|D5|D4|D3|D2|D1|D0
		0 | 0| 1| A| A| A| A| A| A| A

		2) send Character map to Data Reg
		RS|RW|D7|D6|D5|D4|D3|D2|D1|D0
		1 | 0| x| x| x| x| x| x| x| x

	8bit Commands
	-------------
		- Write to RS and RW
		- Write to your Data pins  (D)
		- Wait a minimum of 40 nS (address setup time, Tas)
		- Pulse Enable (E) for minimum of 230 nS 
		- Wait a minimum of 10 nS (address Hold time, Tah)
	4bit Mode
	---------
		- 4 bit only uses the physical pins D4 - D7
		
		- All Commands and Data are sent as 2 nibble chunks
			-MSB bits(D4 D5 D6 D7)  sent first
				  ^  ^  ^  ^
			-LSB bits(D0 D1 D2 D3)  sent last
				-send 0-3 on physical pins 4-5 respectively
			
		*******************
		To Enter 4-bit mode:
			- Send it just like any 4bit command
			- Once the MSBs are sent the system is already in
			  4-bit mode and will be ready to receive LSBs

	Character Mapping
	-----------------
		- Luckily all of the basic characters are stored in a memory
		  location corresponding to their ASCII table entry
			Char  | Hex
			------|------------
			space | 20
			  %   | 25
			  :   | 3A
			0 - 9 | 30 - 39
			A - Z | 41 - 5A
			a - z | 61 - 7A

	Character Spaces Onscreen (2 Line Mode)
	---------------------------------------
		In terms of sending chars to memory. The cursor shifts from:
			-top row end to bottom row start
			-bottom row end to top row start

		So both lines are like one loop of characters that keep 
		wrapping into one another.

		Not all of the lines are shown on screen at once however.
		Each line is 40 chars long in memory, with only 16 of them on 
		screen at a time. 

		Once you write past a lines first 16 further characters
		  are off screen until you wrap around to the next line

	FIGURE:  a simple depiction of the LCDs char layout

		aaaaaaaaaaaaaaaaxxxxxxxxxxxxxxxxxxxxxxxx	} Top Row 
							 
		bbbbbbbbbbbbbbbbyyyyyyyyyyyyyyyyyyyyyyyy	} Bottom Row

		|              ||                      |
		 --------------  ----------------------
			|		   |___________Offscreen Cols (24 chars)
			|
			|______________________________Onscreen Cols (16 chars)
			



I2C communciation with ADC 
---------------------------
	The ADC being used is ADS1115 PGA ADC from adafruit (or rather a knockoff).
	The component is a breakout board hosuing the ADC adn other necessary resistors.

		-16 bit		-4 channel 	-2.0v - 5.0v

	So it is serious overkill for our purposes, but this was the cheapest individually 
	priced ADC anywhere online.
	If the board is ever 'massed' produced or moved to its own custom PCB the ADC 
	will be changed out for a better fit from digikey.

	ADS1115 Datasheet:
	www.ti.com/lit/ds/symlink/ads1113.pdf?HQS=TI-null-null-digikeymode-df-pf-null-wwe&ts=1598643900980

	Physical Connections
	---------------------
		ADC	| Desc.		|Raspberry Pi
		--------------------------------------
		VDD	|		|  3.3v 
		GRND	|		|  GRND 
		SCL	| CLK		|  GPIO pin
		SDA	| Data		|  GPIO pin
		ADDR	| hardwire to  	|  GRND 	
			| select addrs 	|
		A*	|		|  all analog inputs get connected 
					   to your sensor of choice

		appears that we dont need other pins connected anywhere to the pi
	
	2 types of methods to capture analog data
		- Differential 
			reads values between either A0 & A1
			or A2 & A3.
		- Single
			reads value between 1 channel and GRND.
			Can only be positive so our 16 bit res
			becomes 15 bits as MSB is a sign bit.


	ADS1115 Registers
	-------------------------------------------	
	There are 5 registers, but the last two control the max and min
	threshold values returned by the ADCs respectively. I'm not
	too concerned about changing these default values so Ill only be 
	worrying about the main 3.
	
		******Pointer Register Byte (write-only)******
		----------------------------------------------
	1 byte register; Always first to be written to. As it is used
	to determine which of the other registers you'll be accesssing.

	Bit|  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
	----------------------------------------------------
	Def|  -  |  -  |  -  |  -  |  -  |  -  |  Reg Addr |

	Bit 0 and 1 are the only ones that matter. Their value controls the
	register accessed next after writting to the pointer reg.

	00 	Access Conversion register
	01	Access Configuration register



		******Conversion Register (Read-Only)******
		-------------------------------------------
	2 Byte Register that holds the last reading of whichever
	ADC channel the Config Register is set to look at.

	Bit|  15  |   14  |  13  |  12  |  11  |  10  |  9  |  8  |
	-----------------------------------------------------------
	Def|  D15 |  D14  |  D13 |  D12 |  D11 |  D10 |  D9 |  D8 |

	Bit|   7  |   6   |   5  |   4  |   3  |   2  |  1  |  0  |
	-----------------------------------------------------------
	Def|   D7 |   D6  |  D5  |  D4  |  D3  |  D2  |  D1 |  D0 |
	
	D15-D0 all contain raw sensor values in 2's compliment format.
	(So D15 is a sign bit and will always be 0 when using a single
	 ADC channel is single ended mode.)


		******Configure Register (Read/Write)******
		-------------------------------------------
	2Byte Register where all of the ADS1115 settings can be configured

	Bit|  15  |   14  |  13  |  12  |  11  |  10  |  9  |  8  |
	-----------------------------------------------------------
	Def|  OS  |  MUX2 | MUX1 | MUX0 | PGA2 | PGA1 | PGA0 | MODE|

	Bit| 7 | 6 | 5 |   4     |   3    |   2    |    1    |    0    |
	----------------------------------------------------------------
	Def|DR2|DR1|DR0|COMP_MODE|COMP_POL|COMP_LAT|COMP_QUE1|COMP_QUE0|

	Bits	
	-------------------------
	OS - Operational Status 
		Only relevant when running in one-shot mode 
		When Writing
		0 - No Effect
		1 - Start a single Conversion
		When Reading
		0 - the conversion register is not yet ready to read
		1 - the conversion register is ready to read 

	MUX[2:0] 	Convtrols Which ADC Channel we access
		AINp = positive input
		AINn = negative input

		000 AINp = A0 AINn = A1 (default)
		001 AINp = A0 AINn = A3
		010 AINp = A1 AINn = A3
		011 AINp = A2 AINn = A3
		100 AINp = A0 AINn = GND
		100 AINp = A1 AINn = GND
		100 AINp = A2 AINn = GND
		100 AINp = A3 AINn = GND

	PGA[2:0]	Programmalbe Gain Amplifier
		Looks like they control the reference voltages (so max abs(v))

		000  +- 6.144V		 100  +- 0.512V
		001  +- 4.096V		 101  +- 0.256V
		010  +- 2.048V (default) 110  +- 0.256V
		011  +- 1.024V		 111  +- 0.256V

		The default value is perfect for the Raspberry Pi's 3.3v!

	MODE	
		0	run in continuous conversion mode
		1	single shot mode (default)

	DR[2:0]	controls data rate setting
		000 8 sps		100 128 sps (default)
		001 16 sps		101 250 sps
		010 32 sps		110 475 sps
		011 64 sps		111 860 sps

	##This COMP stuff is confusing because we wont be using comparator
	##mode. So for now I'll just be ignoring them.
	COMP_MODE	configures comparator mode
		0 traditional comparator (default)
		1 window comparator
	COMP_POL	controls polarit of Alert/RDY pin
		0 Active Low (default)
		1 Active High
	COMP_LAT	controls if ALERT/RDY pin latches after being asserted
			or if it clears after conversion are within margin of
			upper/lower threshold values
		0 nonlatching (default)
		1 Latching (stays latched until read by master or SMBus alert
			    response is sent by the master)
	COMP_QUE[1:0]	
		00 Assert after one conversion
		01 Assert after two conversions
		10 Assert after four conversions
		11 Disable comparatr & set ALRT/RDY to high-impedance (default)

	I2C Programming the ADS1115
	-------------------------------------

	ADDR pin Connection	| ADS slave address
	--------------------------------------------
		GND		| 1001000	
		VDD		| 1001001
		SDA		| 1001010	
		SCL		| 1001011	

	We'll connect ADDR to GND to avoid confusion. Special procedures
	for SDA and SCL connections are in the datasheet


	Receive mode - 
		First Byte transmitted to slave
		7 byte address, followed by bit R/W flag

		Second Byte transmitted to slave
		Address Pointer Register

		ADS111x acknoeledges recept of Address Pointer
					       ---------------
		Next two Bytes
		are written to the address given by the register pointer
		bits P[1:0]
	
		Register bytes sent MS byte followed by LS byte

	Transmit mod -
		First Byte transmitted to slave
		7 bit slave address, followed by R/W bit

		Slave then enters transmit mode

		Next Byte sent
		MS byte of the register indicated by the RegAddrPointer
		bits P[1:0]

		follow this byte with acknowledgment from master

		LSByte sent by slave
		
		follow with ackowledgment from master

		***master issues START or STOP condition or does not 
		   acknowledge in order to terminate transmission 
		   after any byte


Changes made to System
-------------------------------

	- sudo raspi-config
		was used to enable I2C

	- FUCK LEARNING THE ADS. IM GONNA JUST USE 
	ITS PREMADE PYTHON LIBRARY

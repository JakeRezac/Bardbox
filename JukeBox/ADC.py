import smbus
import time

BUS = 1
ADDRESS = 0x48
bus = smbus.SMBus(BUS)

#Bit|  15  |   14  |  13  |  12  |  11  |  10  |  9  |  8  |
#-----------------------------------------------------------
#Def|  OS  |  MUX2 | MUX1 | MUX0 | PGA2 | PGA1 | PGA0 | MODE|

#Bit| 7 | 6 | 5 |   4     |   3    |   2    |    1    |    0    |
#----------------------------------------------------------------
#Def|DR2|DR1|DR0|COMP_MODE|COMP_POL|COMP_LAT|COMP_QUE1|COMP_QUE0|

new_config = 0x00
new_config = new_config | ( 0b0   << 15)	#OS   0 ; No effect
new_config = new_config | ( 0b100 << 12)	#MUX 100; Ap = A0 An = GND
new_config = new_config | ( 0b010 << 9)		#PGA 010; 2.048v
new_config = new_config | ( 0b0	  << 8)		#MODE 0 ; continuous
new_config = new_config | ( 0b000 << 5)		#DR  000; 8 samples/s
					#This guy stays decidedly stuck
					#at 100; 128samples/s (default)
					#Its the MSB! it wont change from 1
#new_config = new_config | 0b00011 	#COMP DEFAULTS
""" 
	Something about the COMParator mode bits is fucking up our ADC
	the ADS1115 is only returning proper values when they are all left at 0

	looks like its the last two bits being 11
	which translates to:
		"disable comparator and set ALERT/RDY pin to High Impedance"

	perhaps this disabled the converter as a whole?
"""


bus.write_word_data(ADDRESS, 0x01, new_config)
time.sleep(1)

config = bus.read_word_data(ADDRESS, 0x01) #& 0xFFFF
#config = ((config & 0xFF) << 8) | (config >> 8)
print("config:")
print(bin(config))
time.sleep(1)

""" Okay so our high threshold is stuck at 0x4424 and we cant seem to change that for some reason"""
#high_thresh = bus.read_word_data(ADDRESS, 0x11) #& 0xFFFF
##high_thresh = ((high_thresh & 0xFF) << 8) | (high_thresh >> 8) #ADC is a different endian system so flip bytes
#print("High Thresh: " + hex(high_thresh))
#
#bus.write_word_data(ADDRESS, 0x11, 0x7FFF)


new_config = new_config | (0b1 << 15)		#OS  1; start 1 conversion
while (True):
	#bus.write_word_data(ADDRESS, 0x01, new_config) #write OS1 to start 1 conversion
	#time.sleep(0.1)
	value = bus.read_word_data(ADDRESS, 0x00) & 0xFFFF
	value = ((value & 0xFF) << 8) | (value >> 8) #ADC is a different endian system so flip bytes
	print("raw ADC value(unflipped):")
	print((value))
	print(hex(value))
	time.sleep(0.2)
	print("--------------------------------")

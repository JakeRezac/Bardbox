import pygame		#Has methods music methods
import os 		#Has methods for looking at file directories
import random 		#For shuffle functions
import RPi.GPIO as GPIO	#For button controls
import time		#For reading buttons
import JukeLib

pygame.init()
random.seed()

paused = False

#Playlist Directories
#------------------------------------------------------------------------
#path = './songs/'
#categories = ['sad/', 'dramatic/']
button_pins = {12 : "sad" , 21 : "dramatic" }


#GPIO Setup
#------------------------------------------------------------------------
GPIO.setmode(GPIO.BCM) 		# Use Broad Com GPIO pin numbering
#GPIO.setmode(GPIO.BOARD) 	# Use Physical Board GPIO Pin number

GPIO.setup(12, GPIO.IN)
GPIO.setup(21, GPIO.IN)
#inputValue = GPIO.input(25)
#if(InputValue == True):
	#take action

#This may be deleted later
time.sleep(0.03)		# Debouncing

def button_check ():
	for x in button_pins:
		val = GPIO.input(x)
		print(str(button_pins[x]) + " : " + str(val))
		print(" ")
#Main Loop
#------------------------------------------------------------------------
while (True):

	print ("Select a Playlist")
	print ("-----------------")
	print (os.listdir('./songs/'))
	
	while (True):
		button_check()
		time.sleep(1.2)

	category = raw_input("playlist: ")	
	
	path = './songs/' + category + '/'
	print ("starting: " + path)

	songs = JukeLib.start_playlist(path) #Starts first song and returns playlist as a list
	end = len(songs) - 1
	cur = 0

	while (True):
	
		command = raw_input("Command: ")

		#Skip
		#------------------------------------------------------------------------		
		if (command == 's'):			
			cur = cur + 1
			pygame.mixer.music.stop()
	
			if cur > end:
				break
	
			pygame.mixer.music.load(path + songs[cur])
			pygame.mixer.music.play(1)
	
		#Back
		#------------------------------------------------------------------------
		elif (command == 'b'):
			cur = cur -1
			if (cur < 0):
				cur = 0
			else:
				pygame.mixer.music.stop()
				pygame.mixer.music.load(path + songs[cur])
				pygame.mixer.music.play(1)
				
		#Pause
		#------------------------------------------------------------------------
		elif (command == 'p'):	

			if paused:
				pygame.mixer.music.unpause()
				paused = False
			else:
				pygame.mixer.music.pause()
				paused = True

		#Volume Control
		#------------------------------------------------------------------------
		#	volume up
		elif (command == "v+"):
			vol = pygame.mixer.music.get_volume()
			vol = vol + 0.05
			if (vol > 1.0):
				vol = 1.0

			pygame.mixer.music.set_volume(vol)
			print( "volume: " + str(vol) )

		#	volume down
		elif (command == "v-"):
			vol = pygame.mixer.music.get_volume()
			vol = vol - 0.05
			if (vol < 0.0):
				vol = 0.0

			pygame.mixer.music.set_volume(vol)
			print( "volume: " + str(vol) )

		#Next in Queue
		#------------------------------------------------------------------------
		#pygame.mixer.music.get_busy

#GPIO
#------------------------------------------------------------------------

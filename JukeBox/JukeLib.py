import pygame		#Has methods music methods
import os 		#Has methods for looking at file directories
import random 		#For shuffle functions

#Shuffle
#	path should lead to a directory of song files
#	i.e. 
#		path = './songs/dramatic'
#
#	Returns: list of shuffled song files
#------------------------------------------------------------------------
def shuffle_songs(path):
	songs = os.listdir(path)
	random.shuffle(songs)
	return songs


#Play
#	call shuffle_songs()
#	start playing first song in shuffled playlist
#
#	Returns: list of shuffled song files
#------------------------------------------------------------------------
path = './songs/dramatic/'

def start_playlist(path):
	songs = shuffle_songs(path)
	song = path + songs[0]
	#print("songs are: " + str(songs))
	#print("song is  : " + song)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(0)
	
	return songs

#Skip
#	
#
#	Returns: current index of our playlist after the skip
#------------------------------------------------------------------------
#def skip_song(path, cur, songs, end ):
#	cur = cur + 1
#	pygame.mixer.music.stop()
#	
#	if cur > end:
#		
#		
#	
#	pygame.mixer.music.load(path + songs[cur])
#	pygame.mixer.music.play(1)
#
#	return cur
#	

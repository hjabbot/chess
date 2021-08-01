import numpy as np
import pygame as pg


WIDTH = HEIGHT = 512 	# Board pixel dimensions
DIMENSION = 8 			# Board dimensions
SQ_SIZE = WIDTH // DIMENSION 	#Square pixel dimensions

MAX_FPS = 30			# FPS for animations

#List of all col and row names
COLS = 'abcdefgh'
ROWS = '12345678'
#Generates a dictionary which has positions in chess notation as keys, and array index as values
def define_pos():
	#Define a blank dict
	pos_dict = {}

	#Stores array location that corresponds to each position key
	i = 0

	#For each position
	for col in COLS:
		for row in ROWS:
			#Generate a key
			key = col+row
			#Add it to positions
			pos_dict[key] = i
			#Iterate to next position in array
			i += 1
	return pos_dict
POSITION2INDEX = define_pos()

BLACK        = (   0,   0,   0)
WHITE        = ( 255, 255, 255)
DARK_SQUARE  = ( 119, 149,  86)
LIGHT_SQUARE = ( 235, 236, 208)
RED_SQUARE	 = ( 188,  63,  63)




CHESSBOARD = np.array([
			['bR','bN','bB','bQ','bK','bB','bN','bR'],
			['bp','bp','bp','bp','bp','bp','bp','bp'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wp','wp','wp','wp','wp','wp','wp','wp'],
			['wR','wN','wB','wQ','wK','wB','--','wR']
			])

PAWNSONLY = np.array([
			['--','--','--','--','--','--','--','--'],
			['bp','bp','bp','bp','bp','bp','bp','bp'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wp','wp','wp','wp','wp','wp','wp','wp'],
			['--','--','--','--','--','--','--','--'],
			])

ROOKSONLY = np.array([
			['bR','--','--','--','--','--','--','bR'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wR','--','--','--','--','--','--','wR'],
			])


BISHOPSONLY = np.array([
			['--','--','bB','--','--','bB','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','wB','--','--','wB','--','--'],
			])
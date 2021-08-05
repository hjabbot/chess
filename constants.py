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

BLACK        = 'black'
WHITE        = 'white'
DARK_SQUARE  = 'darkolivegreen4'
LIGHT_SQUARE = 'beige'
SELECTION_SQUARE = 'firebrick'
HIGHLIGHT_SQUARE = 'indianred'
SELECTION_ALPHA  = 225
HIGHLIGHT_ALPHA  = 150


BPAWN_ATTACK_DIRECTIONS = (( 1, 1), ( 1,-1))
BPAWN_MOVING_DIRECTIONS = (( 1, 0), ( 2, 0))
WPAWN_ATTACK_DIRECTIONS = ((-1, 1), (-1,-1))
WPAWN_MOVING_DIRECTIONS = ((-1, 0), (-2, 0))
ROOK_DIRECTIONS 		= (( 1, 0), ( 0, 1), (-1, 0), ( 0,-1))
KNIGHT_DIRECTIONS 		= (( 2, 1), ( 2,-1), (-2, 1), (-2,-1), ( 1, 2), ( 1,-2), (-1, 2), (-1,-2))
BISHOP_DIRECTIONS 		= (( 1, 1), (-1, 1), ( 1,-1), (-1,-1))
QUEEN_DIRECTIONS 		= (( 1, 0), ( 0, 1), (-1, 0), ( 0,-1), ( 1, 1), (-1, 1), ( 1,-1), (-1,-1))
KING_DIRECTIONS 		= (( 1, 0), ( 0, 1), (-1, 0), ( 0,-1), ( 1, 1), (-1, 1), ( 1,-1), (-1,-1))


ENPASSANTBOARD = np.array([
			['--','--','--','--','--','--','--','--'],
			['bp','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','wp','--','--','--','--','--','--'],
			['--','--','--','--','bp','--','--','--'],
			['--','--','--','--','--','--','--','bK'],
			['--','--','--','wp','--','--','--','--'],
			['--','--','--','--','--','--','--','wK'],
			])

CASTLINGBOARD = np.array([
			['bR','--','--','--','bK','--','--','bR'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','wp','wp','wp'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['bp','bp','bp','bp','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wR','--','--','--','wK','--','--','wR'],
			])




CHESSBOARD = np.array([
			['bR','bN','bB','bQ','bK','bB','bN','bR'],
			['bp','bp','bp','bp','bp','bp','bp','bp'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wp','wp','wp','wp','wp','wp','wp','wp'],
			['wR','wN','wB','wQ','wK','wB','wN','wR']
			])

# TESTBOARD = CASTLINGBOARD
TESTBOARD = CHESSBOARD
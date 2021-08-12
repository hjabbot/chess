import numpy as np
import pygame as pg


BOARD_WIDTH = BOARD_HEIGHT = 512 	# Board pixel dimensions
MOVELOG_PANEL_WIDTH = 250
MOVELOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 			# Board dimensions
SQ_SIZE = BOARD_WIDTH // DIMENSION 	#Square pixel dimensions

MAX_FPS = 30			# FPS for animations
DEPTH = 3

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


# White will push to positive values
# Black will push to negative values
VALUES = {
			'K': 0,
			'Q': 8,
			'R': 5,
			'B': 3,
			'N': 3,
			'p': 1
}

CHECKMATE_VALUE = 9999
STALEMATE_VALUE = 0


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


# Only the queen is moving for black, and next move after Bb5, queen sacrifices for no reason
DEBUGBOARD1 = np.array([
			['bR','bN','bB','--','bK','bB','bN','bR'],
			['bp','bp','--','bp','bp','bp','bp','bp'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','wp','bQ','wp','--','--'],
			['--','--','--','--','--','wN','--','--'],
			['wp','wp','wp','--','--','--','wp','wp'],
			['wR','wN','wB','wQ','wK','wB','--','wR']
			])

# TESTBOARD = DEBUGBOARD1
TESTBOARD = CHESSBOARD
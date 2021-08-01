from constants import *

import pygame as pg

#Check if coordinates of mouse are within bounds of board
def check_in_bounds(x,y):
	# If outside of board width
	if x > BOARD_SIZE or x < 0:
		return False
	# If outside of board height
	elif y > BOARD_SIZE or y < 0:
		return False
	# Otherwise it must be within the board
	else:
		return True

# Determines if there's a piece at the position
def piece_at_position(position, pieces):
	# For each piece
	for piece in pieces:
		# If the positions match
		if piece.position == position:
			return piece
	# If no pieces position matches
	return False
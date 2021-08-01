from constants import *

# from pieces import Pawn
# from pieces import Rook
# from pieces import Knight
# from pieces import Bishop
# from pieces import Queen
# from pieces import King

from pieces import *

import pygame as pg
from pygame import gfxdraw







#####################################
#.........DRAWING FUNCTIONS.........#
#####################################
def gen_background(screen):
	 # First, clear the screen to light squares. 
	screen.fill(LIGHT_SQUARE)

	# Add dark squares on top of light background
	for r in range(NUM_ROWS):
		for c in range(NUM_COLS):
			if (r+c)%2 == 1:
				pg.draw.rect(screen, DARK_SQUARE, [r*SQUARE_SIZE, c*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE],0)


def gen_black_pieces():
	pieces = [
				Pawn('black', 'a7'),
				Pawn('black', 'b7'),
				Pawn('black', 'c7'),
				Pawn('black', 'd7'),
				Pawn('black', 'e7'),
				Pawn('black', 'f7'),
				Pawn('black', 'g7'),
				Pawn('black', 'h7'),
				# Rook('black', 'a8'),
				# Rook('black', 'h8'),
				# Knight('black', 'b8'),
				# Knight('black', 'g8'),
				# Bishop('black', 'c8'),
				# Bishop('black', 'f8'),
				# Queen('black', 'd8'),
				# King('black', 'e8')
				]

	return pieces


def gen_white_pieces():
	pieces = [
				Pawn('white', 'a2'),
				Pawn('white', 'b2'),
				Pawn('white', 'c2'),
				Pawn('white', 'd2'),
				Pawn('white', 'e2'),
				Pawn('white', 'f2'),
				Pawn('white', 'g2'),
				Pawn('white', 'h2'),
				# Rook('white', 'a1'),
				# Rook('white', 'h1'),
				# Knight('white', 'b1'),
				# Knight('white', 'g1'),
				# Bishop('white', 'c1'),
				# Bishop('white', 'f1'),
				# Queen('white', 'd1'),
				# King('white', 'e1')
				]

	return pieces



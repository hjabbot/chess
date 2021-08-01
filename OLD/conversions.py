from constants import *
import numpy as np

def pos2xy(position):
	# Convert col letter to integer
	col = ord(position[0]) - 96
	row = int(position[1])

	# Generate x,y coords of piece
	x = col*SQUARE_SIZE + PLACEMENT_OFFSET
	y = BOARD_SIZE - (row*SQUARE_SIZE + PLACEMENT_OFFSET + PIECE_SIZE)
	
	return(x,y)



def xy2pos(x,y):
	col = chr(int(np.ceil(x/SQUARE_SIZE)) + 96)

	row = int(np.ceil((BOARD_SIZE - y)/SQUARE_SIZE))

	pos = '{c}{r}'.format(c=col, r=row)

	return pos

# Swap who's turn it is
def change_turn(turn):
	if turn == 'white':
		turn = 'black'
	elif turn == 'black':
		turn = 'white'
	else:
		raise Exception("Invalid turn, must be 'black' or :'white'")
	return turn
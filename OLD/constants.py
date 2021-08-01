import numpy as np

# Define some colors
BLACK        = (   0,   0,   0)
WHITE        = ( 255, 255, 255)
DARK_SQUARE  = ( 119, 149,  86)
LIGHT_SQUARE = ( 235, 236, 208)

# Define dimensions of a chess game
SQUARE_SIZE = 80
NUM_COLS = 8
NUM_ROWS = NUM_COLS
BOARD_SIZE = SQUARE_SIZE * NUM_COLS

# Define size of piece sprites as proportion of square size
PIECE_SIZE = int(SQUARE_SIZE * 0.8)
PLACEMENT_OFFSET = - SQUARE_SIZE/2 - PIECE_SIZE/2


# SQUARE_CENTERS = 
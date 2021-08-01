'''
=====================================================================================
Gets user input
Displays game state
-------------------------------------------------------------------------------------
'''



import numpy as np
import pygame as pg


from constants import *
import engine

'''
Draws the squares and pieces on the board
'''
def draw_gs(screen, gs, row=None, col=None):
	draw_board(screen) #Draw the squares
	draw_selection(screen, row, col) #Draw the selected square
	draw_pieces(screen, gs.board)
	#add in piece highlighting
	#add in move suggestions

'''
=====================================================================================
Draw the squares on the board
-------------------------------------------------------------------------------------
'''
def draw_board(screen):
	colours = [LIGHT_SQUARE, DARK_SQUARE]
	for row in range(DIMENSION):
		for col in range(DIMENSION):
			#Sets the colour for the square
			c = colours[(row+col)%2]
			#Places a square in the correct position
			square = pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
			#Draw it on the screen
			pg.draw.rect(screen, c, square)

'''
=====================================================================================
Draw selection square
-------------------------------------------------------------------------------------
'''
def draw_selection(screen, row, col):
	if row and col:
		#Places a square in the correct position
		square = pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
		#Draw it on the screen
		pg.draw.rect(screen, RED_SQUARE, square)

'''
=====================================================================================
Draw the pieces on the squares
-------------------------------------------------------------------------------------
'''
def draw_pieces(screen, board):
	
	for row in range(DIMENSION):
		for col in range(DIMENSION):
			piece = board[row,col]
			if piece != '--':
				#Places a piece in the correct position
				p = pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
				screen.blit(IMAGES[piece], p)

'''
=====================================================================================
Automates importing images used for each piece
-------------------------------------------------------------------------------------
'''
def import_images():
	#Create dict to store all images with piece name
	imgs = {}
	pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
	for piece in pieces:
		filename = 'img/{}.png'.format(piece)
		img = pg.image.load(filename).convert_alpha()
		img = pg.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))
		imgs[piece] = img
	return imgs

'''
=====================================================================================
Main Function
-------------------------------------------------------------------------------------
'''
if __name__ == '__main__':
	#Initialise the game
	pg.init()
	#Set screen size
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	#Update cycle
	clock = pg.time.Clock()
	#Set a background
	screen.fill(pg.Color(*LIGHT_SQUARE))

	# Creates dict of images with naming scheme e.g. 'wK' = white King
	# Would have in constants.py but needs to be done after game initialised. 
	global IMAGES
	IMAGES = import_images()

	# Generates a fresh board
	gs = engine.GameState()
	# Generate all the valid moves initially
	valid_moves = gs.get_possible_moves()
	# valid_moves = gs.get_valid_moves()
	# Flag for tracking when move is made, stops valid_moves from being calculated constantly
	move_made = False
	#Flag for keeping the game running
	running = True

	# Keeps track of last square clicked on by user
	sq_selected = ()
	# Keeps track of previously selected squares
	prev_selected = []
	while running:
		# If user quits, shut game down
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False

			elif e.type == pg.MOUSEBUTTONDOWN:
				# Retrieve x,y coords of mouse
				location = pg.mouse.get_pos()
				col = location[0] // SQ_SIZE
				row = location[1] // SQ_SIZE

				# Deselect square if same as previously selected
				if sq_selected == (row, col):
					sq_selected = ()
					prev_selected = []
				# Otherwise select square
				else:
					sq_selected = (row, col)
					prev_selected.append(sq_selected)


				# If player selected a different square to the first 
				if len(prev_selected) == 2:
					print([x.moveID for x in valid_moves])
					move = engine.Move(start=prev_selected[0], end=prev_selected[1], board=gs.board)
					print(move.moveID)
					if move in valid_moves:
						gs.make_move(move)
						move_made = True
						sq_selected = ()
						prev_selected = []
					else:
						prev_selected = [sq_selected]

			# If user wants to undo
			elif e.type == pg.KEYDOWN:
				if e.key == pg.K_u:
					# Undo the move
					gs.undo_move()
					# Recalculate the valid moves
					move_made = True
		if move_made:
			valid_moves = gs.get_possible_moves()
			# valid_moves = gs.get_valid_moves()
			if gs.whitetomove:
				print("White's turn")
			else:
				print("Black's turn")
			move_made = False

		if sq_selected:
			draw_gs(screen, gs, row=row, col=col)
		else:
			draw_gs(screen, gs)

		clock.tick(MAX_FPS)
		pg.display.flip()
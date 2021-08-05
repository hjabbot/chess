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
def draw_gs(screen, gs, row=None, col=None, valid_moves=None):
	draw_board(screen) #Draw the squares
	highlight_squares(screen, row, col, gs, valid_moves) #Draw the selected square
	draw_pieces(screen, gs.board)
	

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
Highlight possible moves
-------------------------------------------------------------------------------------
'''
def highlight_squares(screen, row, col, gs, valid_moves):
	# If a square is selected
	if (row, col) != (None, None):
		# If the piece is on the ally team
		if gs.board[row, col][0] == ('w' if gs.whitetomove else 'b'):
			# Create a surface to draw on
			selection = pg.Surface((SQ_SIZE,SQ_SIZE))
			highlight = pg.Surface((SQ_SIZE,SQ_SIZE))

			# Colour the surfaces
			selection.fill(pg.Color(SELECTION_SQUARE))
			highlight.fill(pg.Color(HIGHLIGHT_SQUARE))

			# Alpha level of image. 255 is max
			selection.set_alpha(SELECTION_ALPHA)
			highlight.set_alpha(HIGHLIGHT_ALPHA)

			# Draw the selected square
			screen.blit(selection, (col*SQ_SIZE, row*SQ_SIZE))
			# Draw the highlighted squares
			for move in valid_moves:
				if move.start.row == row and move.start.col == col:
					screen.blit(highlight, (move.end.col*SQ_SIZE, move.end.row*SQ_SIZE))

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
Draws text on screen
-------------------------------------------------------------------------------------
'''
def draw_text(screen, text):
	font = pg.font.SysFont("Courier", 72, True, False)
	text_object = font.render(text, 4, pg.Color(DARK_SQUARE))
	text_origin = (WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
	text_location = pg.Rect(0,0, WIDTH, HEIGHT).move(text_origin[0], text_origin[1])

	backbackground = pg.Surface((WIDTH, text_object.get_height() + 10))
	background = pg.Surface((WIDTH, text_object.get_height()))
	backbackground.fill(pg.Color(BLACK))
	background.fill(pg.Color(LIGHT_SQUARE))

	screen.blit(backbackground, (0, text_origin[1] - 5))
	screen.blit(background, (0, text_origin[1]))
	screen.blit(text_object, text_location)

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
Animates the movements
-------------------------------------------------------------------------------------
'''
def animate_moves(move, screen, board, clock):
	# List of coordinates for animation to run through
	coords = []
	# Amount to move in each axis
	dr = move.end.row - move.start.row
	dc = move.end.col - move.start.col
	# Animation speed
	frames_per_square = 10
	# Number of frames in animation. Take distance between start and end, multiply by
	# number of frames per square, round to nearest int
	# frame_count = np.int_(np.linalg.norm(np.abs(dr)+np.abs(dc)) * frames_per_square)
	frame_count = MAX_FPS // 2

	# For each frame to draw
	for frame in range(frame_count+1):
		# Add small increments between start and start+dr for each frame
		r, c = (move.start.row + dr*(frame/frame_count), move.start.col + dc*(frame/frame_count))
		# Draw board normally (piece will be in end square already)
		draw_board(screen)
		draw_pieces(screen, board)
		# Draw blank square over the moved piece temporarily
		# Get colour of square
		colour = [LIGHT_SQUARE, DARK_SQUARE][(move.end.row + move.end.col)%2]
		# Create a square and draw it
		end_square = pg.Rect(move.end.col*SQ_SIZE, move.end.row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
		pg.draw.rect(screen, colour, end_square)
		# Draw captured piece on the square until it needs to appear to be captured
		if move.piece_captured != '--':
			screen.blit(IMAGES[move.piece_captured], end_square)
		# Draw the piece moving up each frame
		screen.blit(IMAGES[move.piece_moved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
		pg.display.flip()
		clock.tick(60)
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
	screen.fill(pg.Color(LIGHT_SQUARE))

	# Creates dict of images with naming scheme e.g. 'wK' = white King
	# Would have in constants.py but needs to be done after game initialised. 
	global IMAGES
	IMAGES = import_images()

	# Generates a fresh board
	gs = engine.GameState()
	# Generate all the valid moves initially
	valid_moves = gs.get_valid_moves()
	# Flag for tracking when move is made, stops valid_moves from being calculated constantly
	move_made = False
	# Flag for when to animate (don't bother when undoing)
	animate = False
	#Flag for keeping the game running
	running = True
	# Flag to notify user when game over
	game_over = False

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

				if not game_over:
					# If player selected a different square to the first 
					if len(prev_selected) == 2:
						print([x.get_chess_notation() for x in valid_moves])
						# Figures out what the move selected was
						move = engine.Move(start=prev_selected[0], end=prev_selected[1], board=gs.board)
						# Check if it's in list of valid moves
						for i in range(len(valid_moves)):
							if move == valid_moves[i]:
								# Make the move, reset variables for next turn
								print(move.get_chess_notation())
								gs.make_move(valid_moves[i])
								sq_selected = ()
								prev_selected = []
								move_made = True
								animate = True

						if not move_made:
							prev_selected = [sq_selected]


			# If a keyboard shortcut pressed
			elif e.type == pg.KEYDOWN:
				# If user wants to undo
				if e.key == pg.K_u:
					# Undo the move
					gs.undo_move()
					# Recalculate the valid moves
					move_made = True
					animate = False
					game_over = False

				# If user want to reset board
				if e.key == pg.K_r:
					gs = engine.GameState()
					valid_moves = gs.get_valid_moves()
					sq_selected = ()
					prev_selected = []
					move_made = False
					animate = False
					game_over = False
		

		if move_made:
			if animate:
				animate_moves( gs.movelog[-1], screen, gs.board, clock)
			
			valid_moves = gs.get_valid_moves()
			
			move_made = False
			animate = False

		if sq_selected:
			draw_gs(screen, gs, row=row, col=col, valid_moves=valid_moves)
		else:
			draw_gs(screen, gs)


		if gs.checkmate:
			game_over = True
			if gs.whitetomove:
				draw_text(screen, 'Black Wins!')
			else:
				draw_text(screen, 'White Wins!')
		elif gs.stalemate:
			game_over = True
			print('Stalemate')

	
			if gs.whitetomove:
				print("White's turn")
			else:
				print("Black's turn")
			



		clock.tick(MAX_FPS)
		pg.display.flip()
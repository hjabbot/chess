from constants import *

from functions import *

from mouse import *

import pygame as pg
from pygame.math import Vector2


if __name__ == '__main__':

	pg.init()

	size = (NUM_COLS*SQUARE_SIZE, NUM_ROWS*SQUARE_SIZE)
	screen = pg.display.set_mode(size)

	gen_background(screen)
	black_pieces = gen_black_pieces()
	white_pieces = gen_white_pieces()
	all_pieces = black_pieces + white_pieces

	# Set who's turn it is
	turn = 'white'
	move_made = False
	#
	carry_on = True
	held = False

	clock = pg.time.Clock()

	# -------- Main Program Loop -----------
	while carry_on:
		# --- Main event loop

		 # Sit idle until something happens
		event = pg.event.wait()
		# Retrieve mouse position
		x, y = pg.mouse.get_pos()
		


		if check_in_bounds(x,y):
			
			selected_piece = None

			# If user clicked to close, end game loop
			if event.type == pg.QUIT: 
				carry_on = False

			# If user clicks down on the screen
			elif event.type == pg.MOUSEBUTTONDOWN:
				held = True
				position = xy2pos(x, y)

				if event.button == 1:
					print('click')
					for piece in all_pieces:
						if piece.rect.collidepoint(event.pos):
							print('collision')
							offset = Vector2(piece.rect.topleft) - event.pos
							selected_piece = piece

			elif event.type == pg.MOUSEBUTTONUP:
				if event.button == 1:
					held = False
					selected_piece = None

			elif event.type == pg.MOUSEMOTION and held == True:
				if selected_piece:
					selected_piece.rect.topleft = event.pos + offset



			# if turn == 'white':
			# 	existing_piece = piece_at_position(position, white_pieces)
			# elif turn == 'black':
			# 	existing_piece = piece_at_position(position, black_pieces)

			# if existing_piece:
			# 	print(existing_piece.name)
			# 	move_made = True


					

					
			 # If user declicks on the screen
			# elif event.type == pg.MOUSEBUTTONUP:
			# 	move_made = True

		# If a valid move was made
		if move_made == True:
			# Reset for next turn
			move_made = False
			# Change who's turn it is
			turn = change_turn(turn)
	 
		 # --- Drawing code should go here
		for piece in all_pieces:
			screen.blit(piece.image, piece.rect)

		# --- Go ahead and update the screen with what we've drawn.
		pg.display.flip()

		# --- Limit to 60 frames per second
		clock.tick(60)
	 
	#Once we have exited the main program loop we can stop the game engine:
	pg.quit()
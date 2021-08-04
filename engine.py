'''
Stores board state
Determines valid moves
Logs moves
'''

import numpy as np
from constants import *


class GameState:
	def __init__(self):
		# self.board = CHESSBOARD
		self.board = TESTBOARD
		self.move_functions = {	'p': self.get_pawn_moves,
								'R': self.get_rook_moves,
								'N': self.get_knight_moves,
								'B': self.get_bishop_moves,
								'Q': self.get_queen_moves,
								'K': self.get_king_moves,
								}

		self.whitetomove = True
		self.movelog = []

		wK = np.where(self.board == 'wK')
		bK = np.where(self.board == 'bK')
		self.wK_location = tuple(pos[0] for pos in wK)
		self.bK_location = tuple(pos[0] for pos in bK)
		self.in_check = False
		self.pins = []
		self.checks = []

		self.stalemate = False
		self.checkmate = False

		# Coordinates of square where en passant possible
		self.enpassant_allowed = ()

		# Keeps track of the right to castle
		self.current_castling_rights = CastleRights(True, True, True, True)
		self.castling_rights_log = [CastleRights(
												self.current_castling_rights.wks,
												self.current_castling_rights.wqs,
												self.current_castling_rights.bks,
												self.current_castling_rights.bqs
												)
									]

	# Move a piece from start to end positions
	# Doesn't work for en passant, castling, and pawn promotion
	def make_move(self, move):

		self.perform_move(move)
		self.perform_promotion(move)
		self.perform_enpassant(move)
		self.perform_castle(move)

		self.update_king_location(move)
		self.update_castle_rights(move)



	# Goes back one move
	def undo_move(self):
		if len(self.movelog) != 0:
			last_move = self.movelog.pop()
			self.board[last_move.end.row,last_move.end.col] = last_move.piece_captured
			self.board[last_move.start.row,last_move.start.col] = last_move.piece_moved
			self.whitetomove = not(self.whitetomove)

			# Update king location if moved
			if last_move.piece_moved == 'wK':
				self.wK_location = (last_move.start.row, last_move.start.col)
			elif last_move.piece_moved == 'bK':
				self.bK_location = (last_move.start.row, last_move.start.col)

			# If undoing an en passant
			if last_move.is_enpassant:
				# Replace square with a blank (otherwise would be a pawn)
				self.board[last_move.end.row, last_move.end.col] = '--'
				# Replace taken piece with a pawn of the appropriate colour
				self.board[last_move.start.row, last_move.end.col] = 'bp' if self.whitetomove else 'wp'
				# Keep track of the en passant
				self.enpassant_allowed = (last_move.end.row, last_move.end.col)

			# Undo a 2 square pawn advance
			if last_move.piece_moved[1] == 'p' and abs(last_move.start.row - last_move.end.row):
				self.enpassant_allowed = False

			# Remove newest castle rights from move we're undoing
			self.castling_rights_log.pop()
			# Reset castle rights to previous
			self.current_castling_rights = self.castling_rights_log[-1]
			# If move was a castle
			if last_move.is_castle:
				# Kingside
				if last_move.end.col - last_move.start.col > 0:
					self.board[last_move.end.row, last_move.end.col + 1] = self.board[last_move.end.row, last_move.end.col - 1]
					self.board[last_move.end.row, last_move.end.col - 1] = '--'
				# Queenside
				else:
					self.board[last_move.end.row, last_move.end.col - 2] = self.board[last_move.end.row, last_move.end.col + 1]
					self.board[last_move.end.row, last_move.end.col + 1] = '--'
		else:
			print('No more moves to undo')

	def square_being_attacked(self, row, col, castle_into_pawn=False):
		# Switch to opponent temporarily
		self.whitetomove = not(self.whitetomove)
		# Calculate their possible moves
		enemy_moves = self.get_possible_moves(castle_into_pawn=castle_into_pawn)
		# Switch back
		self.whitetomove = not(self.whitetomove)

		# If requested square in list of opponent moves, then it's being attacked
		for move in enemy_moves:
			if move.end.row == row and move.end.col == col:
				return True
		# Otherwise it isn't being attacked
		return False



	# Updates castling rights
	def update_castle_rights(self, move):
		# If white king moved, remove white's castling rights
		if move.piece_moved == 'wK':
			self.current_castling_rights.wks = False
			self.current_castling_rights.wqs = False
		# If black king moved, remove black's castling rights
		elif move.piece_moved == 'bK':
			self.current_castling_rights.bks = False
			self.current_castling_rights.bqs = False
		# If white rook moved
		elif move.piece_moved == 'wR':
			# Only call if rook starting on back rank
			if move.start.row == DIMENSION-1:
				# If it's the queen side rook, remove rights
				if move.start.col == 0:
					self.current_castling_rights.wqs = False
				# If it's the king side rook, remove rights
				elif move.start.col == DIMENSION-1:
					self.current_castling_rights.wks = False
		# If black rook moved
		elif move.piece_moved == 'bR':
			# Only call if rook starting on back rank
			if move.start.row == 1:
				# If it's the queen side rook, remove rights
				if move.start.col == 0:
					self.current_castling_rights.bqs = False
				# If it's the king side rook, remove rights
				elif move.start.col == DIMENSION-1:
					self.current_castling_rights.bks = False


		# If a rook is captured, update to not allow castling
		if move.piece_captured == 'wR':
			if move.end.row == DIMENSION-1:
				if move.end.col == 0:
					self.current_castling_rights.wqs = False
				elif move.endCol == DIMENSION-1:
					self.current_castling_rights.wks = False
		elif move.piece_captured == 'bR':
			if move.end.row == 0:
				if move.end.col == 0:
					self.current_castling_rights.bqs = False
				elif move.endCol == DIMENSION-1:
					self.current_castling_rights.bks = False



		# Add move to log
		self.castling_rights_log.append(CastleRights(
												self.current_castling_rights.wks,
												self.current_castling_rights.wqs,
												self.current_castling_rights.bks,
												self.current_castling_rights.bqs
												)
										)

	# Updates kings location for checking checks
	def update_king_location(self, move):
		# Update king location if moved
		if move.piece_moved == 'wK':
			self.wK_location = (move.end.row, move.end.col)
		elif move.piece_moved == 'bK':
			self.bK_location = (move.end.row, move.end.col)

	# Perform rudimentary moving
	def perform_move(self, move):
		# Clears where move started
		self.board[move.start.row,move.start.col] = '--'
		# Overwrites where move ends
		self.board[move.end.row,move.end.col] = move.piece_moved
		# Add to move log
		self.movelog.append(move)
		# Change to opposite side's turn
		self.whitetomove = not(self.whitetomove)

	# Promote pawn if it is appropriate
	def perform_promotion(self, move):
		# If pawn was promoted, get its colour and add a 'Q' to make it a Queen
		if move.is_pawn_promotion:
			self.board[move.end.row, move.end.col] = move.piece_moved[0] + 'Q'

	# En Passant pawn if it is appropriate
	def perform_enpassant(self, move):
		# If move is en passant
		if move.is_enpassant:
			# The capturing pawn will start on same row as captured pawn, so use that as coord to capture
			self.board[move.start.row, move.end.col] = '--'
		# On two square pawn move
		if move.piece_moved[1] == 'p' and np.abs(move.start.row - move.end.row) == 2:
			# Average pawn rows to find square to capture with en passant
			# Average because it works for both white and black
			self.enpassant_allowed = ((move.start.row + move.end.row) // 2, move.start.col)
		# Otherwise reset
		else:
			self.enpassant_allowed = ()

	def perform_castle(self, move):

		colour = 'w' if self.whitetomove else 'b'
		
		# If castling
		if move.is_castle:
			# If moved in positive direction, kingside castling
			if move.end.col - move.start.col > 0:
				# Copy rook to new square
				self.board[move.end.row, move.end.col - 1] = self.board[move.end.row, move.end.col + 1]
				# Clear where rook was
				self.board[move.end.row, move.end.col + 1] = '--'

			# If moved in negative direction, queenside castling
			else:
				# Copy rook to new square
				self.board[move.end.row, move.end.col + 1] = self.board[move.end.row, move.end.col - 2]
				# Clear where rook was
				self.board[move.end.row, move.end.col - 2] = '--'

	# All moves possible after considering check
	def get_valid_moves(self):
		# Store en passant position (if exists)
		temp_enpassant_allowed = self.enpassant_allowed
		temp_castle_rights = CastleRights(	self.current_castling_rights.wks,
											self.current_castling_rights.wqs,
											self.current_castling_rights.bks,
											self.current_castling_rights.bqs
											)
		
		
		moves = []
		self.in_check, self.pins, self.checks = self._check4pins_checks()
		
		# Get the current turn's king position
		if self.whitetomove:
			kr, kc = self.wK_location
		else:
			kr, kc = self.bK_location

		# If in check
		if self.in_check:
			# If no double-check
			if len(self.checks) == 1:
				moves = self.get_possible_moves()
				# Get location and direction of check
				check_row, check_col, check_dir_r, check_dir_c = self.checks[0]
				# Determine the piece that is checking the king
				piece_checking = self.board[check_row, check_col]
				
				valid_squares = []

				# If it's a knight, capturing is the only non-king move that is valid
				if piece_checking == 'N':
					valid_squares = [(check_row, check_col)]
				# Otherwise
				else:
					# Along the LOS
					for i in range(1, DIMENSION):
						# Squares in the direction of the check are valid
						valid_square = (kr+check_dir_r*i, kc+check_dir_c*i)
						valid_squares.append(valid_square)
						# If eached the checking piece, stop searching along this LOS
						if valid_square[0] == check_row and valid_square[1] == check_col:
							break

				# Remove moves that don't block check or move king
				# Working backwards since iterating through list
				for i in range(len(moves)-1, -1, -1):
					# If not moving the king, then it must be a block or capture
					if moves[i].piece_moved[1] != 'K':
						# Removes any moves that don't block or capture
						if not (moves[i].end.row, moves[i].end.col) in valid_squares:
							moves.remove(moves[i])
			# Otherwise, have to move the king
			else:
				self.get_king_moves(kr, kc, moves)
		# Otherwise everything is possible, there's no check
		else:
			moves = self.get_possible_moves()
			self._get_castle_moves(kr, kc, moves)

		if len(moves) == 0:
			if self.in_check:
				self.checkmate = True
			else:
				self.stalemate = True

		# Reset enpassant coordinates to original state after doing checks
		self.enpassant_allowed = temp_enpassant_allowed
		self.current_castling_rights = temp_castle_rights
		return moves

	# All moves possible ignoring check
	def get_possible_moves(self, castle_into_pawn=False):
		#Start with blank move list
		moves = []
		#For each square on the board
		for row in range(len(self.board)):
			for col in range(len(self.board[row])):
				# Get value of what's in that square
				square = self.board[row,col]
				# If it's blank, do nothing
				if square == '--':
					continue
				# If it has a piece on it
				else:
					piece_colour, piece_type = square
					# If it's the current player's piece
					if (piece_colour == 'w' and self.whitetomove) or (piece_colour == 'b' and not(self.whitetomove)):
						# Get possible moves (automatically calls correct function)
						self.move_functions[piece_type](row, col, moves)

					# Bug fix: Kingside rook pawn won't stop king side castle, leading king to end up in check after castling
					# Similarly, Queenside knight pawn wont stop queen side castle
					if castle_into_pawn == True:
						if (square == 'wp' and row == 1):
							if col-1 >= 0:
								moves.append(Move((row, col), (row-1, col-1), self.board))
							if col+1 < DIMENSION:
								moves.append(Move((row, col), (row-1, col+1), self.board))
						if (square == 'bp' and row == DIMENSION-2):
							if col-1 >= 0:
								moves.append(Move((row, col), (row+1, col-1), self.board))
							if col+1 < DIMENSION:
								moves.append(Move((row, col), (row+1, col+1), self.board))
		return moves

	# Common code between all standard moves of any piece. Takes in basis vectors (directions), and
	# length (max_steps), and calculates all possible moves from start_row, start_col
	def _moves_in_direction(self, directions, start_row, start_col, moves, max_step=DIMENSION-1):
		piece_pinned = False
		pin_direction = ()
		# Going backwards because iterating through list and removing
		for i in range(len(self.pins)-1, -1, -1):
			# If the pin matches the piece's position
			if self.pins[i][0] == start_row and self.pins[i][1] == start_col:
				piece_pinned = True
				pin_direction = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break

		# Determine enemy colour
		enemy_colour = 'b' if self.whitetomove else 'w'
		# For each direction
		for dr, dc in directions:
			# For each possible step size
			for i in range(1,max_step+1):
				# Set new x,y coords based off step size 
				end_row = start_row + i*dr
				end_col = start_col + i*dc

				# If still on the board
				if 0<=end_row<DIMENSION and 0<=end_col<DIMENSION:
					if not piece_pinned or pin_direction == (dr, dc) or pin_direction == (-dr, -dc):
						# Find what's at that location
						piece = self.board[end_row, end_col]

						current_piece = self.board[start_row, start_col]

						# If moving the king, make sure not moving into check or into ally
						if current_piece[1] == 'K' and piece[0] != current_piece[0]:
							# Temporarily move the king to run check check
							if self.whitetomove:
								self.wK_location = (end_row, end_col)
							else:
								self.bK_location = (end_row, end_col)
							# Check for checks
							in_check, pins, checks = self._check4pins_checks()
							# If no check
							if not in_check:
								moves.append(Move((start_row, start_col), (end_row, end_col), self.board))
							# Return to original position
							if self.whitetomove:
								self.wK_location = (start_row, start_col)
							else:
								self.bK_location = (start_row, start_col)

						# If nothing, add to valid moves
						elif piece == '--':
							moves.append(Move((start_row, start_col), (end_row, end_col), self.board))
						# If enemy piece, add to valid moves and stop searching in this direction
						elif piece[0] == enemy_colour:
							moves.append(Move((start_row, start_col), (end_row, end_col), self.board))
							break
						# If ally piece, stop searching in this direction
						else:
							break
				# Stop searching in this direction if off board
				else:
					break
	
	# Checks pieces to see if they are pinned (or in check for King)
	def _check4pins_checks(self):
		# Store pins, checks for later reference to minimise search time
		pins = []
		checks = []
		in_check = False

		# Make sure to search for correct pieces
		if self.whitetomove:
			enemy_colour = 'b'
			ally_colour = 'w'
			start_row, start_col = self.wK_location
		else:
			enemy_colour = 'w'
			ally_colour = 'b'
			start_row, start_col = self.bK_location

		# Every direction which king can be attacked from
		directions = KING_DIRECTIONS + KNIGHT_DIRECTIONS


		for dr, dc in directions:
			potential_pin = ()

			for i in range(1, DIMENSION):
				end_row = start_row + i*dr
				end_col = start_col + i*dc

				# If still on the board
				if 0<=end_row<DIMENSION and 0<=end_col<DIMENSION: 
					# Find piece at target location
					end_piece = self.board[end_row, end_col]
					# If it's an ally, it could be pinned
					# King clause to stop king being able to move along check axis
					if end_piece[0] == ally_colour and end_piece[1] != 'K':
						# If nothing stopping piece from being pinned
						if potential_pin == ():
							potential_pin = (end_row, end_col, dr, dc)
						# If there's already an allied piece in the way, then it's not pinned
						else:
							break
					# If there's LOS to an enemy piece
					elif end_piece[0] == enemy_colour:
						piece = end_piece[1]
						direction = (dr, dc)
						# Check if any piece can attack the king
						if (direction in BPAWN_ATTACK_DIRECTIONS and piece == 'p' and i == 1 and enemy_colour == 'w') or \
						   (direction in WPAWN_ATTACK_DIRECTIONS and piece == 'p' and i == 1 and enemy_colour == 'b') or \
						   (direction in ROOK_DIRECTIONS and piece == 'R') or \
						   (direction in BISHOP_DIRECTIONS and piece == 'B') or \
						   (direction in QUEEN_DIRECTIONS and piece == 'Q') or \
						   (direction in KING_DIRECTIONS and piece == 'K' and i == 1):
						   
							# If nothing is blocking, i.e. if in check
							if potential_pin == ():
								in_check = True
								checks.append((end_row, end_col, dr, dc))
								break
							else:
								pins.append(potential_pin)
								break
						# Knight seperate since can't pin anything, attacks king directly
						elif (direction in KNIGHT_DIRECTIONS and piece == 'N' and i == 1):
							in_check = True
							checks.append((end_row, end_col, dr, dc))
						# Else nothing to check
						else:
							break
				# Off the board
				else:
					break

		return in_check, pins, checks

	def _get_pawn_forward_moves(self, row, col, moves, 
								vert_move_direction, 
								start_row, 
								piece_pinned, pin_direction,
								piece_moving_directions):

		# If square in front is blank
		if self.board[row+vert_move_direction,col] == '--':
			# If not pinned, or at least can move in pin direction
			if not piece_pinned or pin_direction in piece_moving_directions:
				# Add to possible moves
				moves.append(Move((row, col), (row+vert_move_direction,col), self.board))
				# If square 2 in front of starting position is also blank
				if row == start_row and self.board[start_row + 2*vert_move_direction,col] == '--':
					# Add to possible moves
					moves.append(Move((row, col), (start_row + 2*vert_move_direction,col), self.board))

	def _get_pawn_diagonal_moves(self, row, col, moves, 
								 vert_move_direction, horz_move_direction, 
								 enemy_colour, 
								 piece_pinned, pin_direction,
								 piece_attack_directions):

		# Checking diagonals
		# If between column bounds
		if 0 <= col + horz_move_direction < DIMENSION:
			# If pawn not pinned, or at least pinned in axis of attack
			if not piece_pinned or (vert_move_direction, horz_move_direction) == pin_direction:
				# Check if there's an enemy to capture there
				print(row, col, self.enpassant_allowed)
				if self.board[row+vert_move_direction,col+horz_move_direction][0] == enemy_colour: 
						# Allowable move
					moves.append(Move((row, col), (row+vert_move_direction,col+horz_move_direction), self.board))
				# If the coordinates of the attack land on the en passant square
				elif (row+vert_move_direction, col+horz_move_direction) == self.enpassant_allowed:
					moves.append(Move(	(row, col), 
										(row+vert_move_direction,col+horz_move_direction), 
										self.board, 
										is_enpassant=self.enpassant_allowed
									)
								)

	def _get_castle_moves(self, row, col, moves):
		# Determine ally colour for modifying castling rights
		ally_colour = 'w' if self.whitetomove else 'b'

		# If in check, do nothing, no castling allowed
		if self.in_check:
			return

		# If white or black can castle kingside
		if self.whitetomove and self.current_castling_rights.wks or \
		   not(self.whitetomove) and self.current_castling_rights.bks:
			self._get_kingside_castle_moves(row, col, moves)
		# If white or black can castle queenside
		if self.whitetomove and self.current_castling_rights.wqs or \
		   not(self.whitetomove) and self.current_castling_rights.bqs:
			self._get_queenside_castle_moves(row, col, moves)

	def _get_kingside_castle_moves(self, row, col, moves):
		# If squares in back rank are clear
		if self.board[row, col+1] == '--' and self.board[row, col+2] == '--':
			# If squares in back rank aren't being attacked
			if not(self.square_being_attacked(row, col+1, castle_into_pawn=True)) and \
			   not(self.square_being_attacked(row, col+2, castle_into_pawn=True)):

			   moves.append(Move((row, col), (row, col+2), self.board, is_castle=True))


	def _get_queenside_castle_moves(self, row, col, moves):
		# If squares in back rank are clear
		if self.board[row, col-1] == '--' and \
		   self.board[row, col-2] == '--' and \
		   self.board[row, col-3] == '--' :
			# If squares in back rank aren't being attacked
			if not(self.square_being_attacked(row, col-1, castle_into_pawn=True)) and \
			   not(self.square_being_attacked(row, col-2, castle_into_pawn=True)):
			   moves.append(Move((row, col), (row, col-2), self.board, is_castle=True))


	# General code modified for both black and white to run off of
	def get_pawn_moves(self, row, col, moves):
		# Prepare variables for parsing into move checkers
		if self.whitetomove:
			vert_move_direction = -1
			start_row = DIMENSION-2
			enemy_colour = 'b'
			piece_moving_directions = WPAWN_MOVING_DIRECTIONS
			piece_attack_directions = WPAWN_ATTACK_DIRECTIONS
		else:
			vert_move_direction = 1
			start_row = 1
			enemy_colour = 'w'
			piece_moving_directions = BPAWN_MOVING_DIRECTIONS
			piece_attack_directions = BPAWN_ATTACK_DIRECTIONS

		#Check for any pins that the pawns might be under
		piece_pinned = False
		pin_direction = ()
		# Going backwards because iterating through list and removing
		for i in range(len(self.pins)-1, -1, -1):
			# If the pin matches the pawns position
			if self.pins[i][0] == row and self.pins[i][1] == col:
				piece_pinned = True
				pin_direction = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break


		# Check ahead of pawn
		self._get_pawn_forward_moves(row, col, moves, 
									 vert_move_direction, 
									 start_row, 
									 piece_pinned, pin_direction,
									 piece_moving_directions)
		# Check the left column
		self._get_pawn_diagonal_moves(row, col, moves, 
									  vert_move_direction, -1, 
									  enemy_colour, 
									  piece_pinned, pin_direction,
									  piece_attack_directions)

		# Check the right column
		self._get_pawn_diagonal_moves(row, col, moves, 
									  vert_move_direction, +1, 
									  enemy_colour, 
									  piece_pinned, pin_direction,
									  piece_attack_directions)

			# print('{},{} - {}'.format(row, col, len(moves)))

	def get_rook_moves(self, row, col, moves):
		# Define movable basis vectors
		self._moves_in_direction(ROOK_DIRECTIONS, row, col, moves)

	def get_knight_moves(self, row, col, moves):
		# Define movable basis vectors
		self._moves_in_direction(KNIGHT_DIRECTIONS, row, col, moves, max_step=1)

	def get_bishop_moves(self, row, col, moves):
		# Define movable basis vectors
		self._moves_in_direction(BISHOP_DIRECTIONS, row, col, moves)

	def get_queen_moves(self, row, col, moves):
		# Define movable basis vectors
		self._moves_in_direction(QUEEN_DIRECTIONS, row, col, moves)

	def get_king_moves(self, row, col, moves):
		# Define movable basis vectors
		self._moves_in_direction(KING_DIRECTIONS, row, col, moves, max_step=1)



class Move:
	# maps keys to values
	# key : value
	ranks2rows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
	files2cols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}

	rows2ranks = {v: k for k, v in ranks2rows.items()}
	cols2files = {v: k for k, v in files2cols.items()}

	# subclass for easier reference to row/cols
	class Position:
		def __init__(self, row, col):
			self.row = row
			self.col = col

	# Stores all info needed to make move
	def __init__(self, start=None, end=None, board=None, is_enpassant=False, is_castle=False):
		self.start = self.Position(start[0], start[1])
		self.end = self.Position(end[0],end[1])
		self.piece_moved = board[self.start.row][self.start.col]
		self.piece_captured = board[self.end.row][self.end.col]
		# Creates a unique ID for each possible move
		self.moveID = self.start.row*1000 + self.start.col*100 + self.end.row*10 + self.end.col

		# Stores boolean flag for if pawn promotion this turn
		self.is_pawn_promotion = self.check_if_pawn_promotion()

		# Stores boolean flag for if enpassant allowed this turn
		self.is_enpassant = is_enpassant

		# Stores boolean flag for if castling allowed this turn
		self.is_castle = is_castle

	#Determines what is '==' to this class
	def __eq__(self, other):
		# If they are the same type of object
		if isinstance(other, Move):
			# Check if the moves are the same
			return self.moveID == other.moveID
		# If not same object, then not equal
		return False

	def check_if_pawn_promotion(self):
		#    If it's white and it reaches the top of the board
		# Or if it's black and it reaches the bottom of the board
		if 	self.piece_moved == 'wp' and self.end.row == 0 or \
			self.piece_moved == 'bp' and self.end.row == DIMENSION-1:
			return True
		# Otherwise it's not pawn promotion
		return False

	# Print out start -> end
	def get_chess_notation(self):
		start_move = self.get_rank_and_file(self.start.row, self.start.col)
		end_move = self.get_rank_and_file(self.end.row, self.end.col)
		return start_move + '->'+ end_move

	# Get position in format e.g. e4
	def get_rank_and_file(self, r, c):
		return self.cols2files[c] + self.rows2ranks[r]

# Keeps track of each of the castling rights
class CastleRights:
	def __init__(self, wks, wqs, bks, bqs):
		self.wks = wks
		self.wqs = wqs
		self.bks = bks
		self.bqs = bqs
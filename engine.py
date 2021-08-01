'''
Stores board state
Determines valid moves
Logs moves
'''

import numpy as np
from constants import *




class GameState:
	def __init__(self):
		self.board = CHESSBOARD
		# self.board = ROOKSONLY
		self.move_functions = {	'p': self.get_pawn_moves,
								'R': self.get_rook_moves,
								'N': self.get_knight_moves,
								'B': self.get_bishop_moves,
								'Q': self.get_queen_moves,
								'K': self.get_king_moves,
								}

		self.whitetomove = True
		self.movelog = []

	# Move a piece from start to end positions
	# Doesn't work for en passant, castling, and pawn promotion
	def make_move(self, move):
		# Clears where move started
		self.board[move.start.row,move.start.col] = '--'
		# Overwrites where move ends
		self.board[move.end.row,move.end.col] = move.piece_moved
		# Add to move log
		self.movelog.append(move)
		# Change to opposite side's turn
		self.whitetomove = not(self.whitetomove)

	# Goes back one move
	def undo_move(self):
		if len(self.movelog) != 0:
			last_move = self.movelog.pop()
			self.board[last_move.end.row,last_move.end.col] = last_move.piece_captured
			self.board[last_move.start.row,last_move.start.col] = last_move.piece_moved
			self.whitetomove = not(self.whitetomove)
		else:
			print('No more moves to undo')

	# All moves possible after considering check
	def get_valid_moves(self):
		pass

	# All moves possible ignoring check
	def get_possible_moves(self):
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
		return moves


	#Calculates all possible moves for pawn at row, col
	def get_pawn_moves(self, row, col, moves):

		if self.whitetomove:
			# If square in front is blank
			if self.board[row-1,col] == '--':
				# Add to possible moves
				moves.append(Move((row, col), (row-1,col), self.board))
				# If square 2 in front of starting position is also blank
				if row == DIMENSION-2 and self.board[row-2,col] == '--':
					# Add to possible moves
					moves.append(Move((row, col), (row-2,col), self.board))

				# print('{},{} - {}'.format(row, col, len(moves)))

			# Checking diagonals
			if col-1 >= 0:
				if self.board[row-1,col-1][0] == 'b':
					moves.append(Move((row, col), (row-1,col-1), self.board))
			if col+1 < DIMENSION:
				if self.board[row-1,col+1][0] == 'b':
					moves.append(Move((row, col), (row-1,col+1), self.board))

			# En Passant
			# if col-1 >= 0:
			# 	if row == 3 and board[row][col-1] == 'b':

			# if col+1 <= 7:
			# 	if row == 3 and board[row][col+1] == 'b':

		#If it's black's turn
		else:
			# If square in front is blank
			if self.board[row+1,col] == '--':
				# Add to possible moves
				moves.append(Move((row, col), (row+1,col), self.board))
				# If square 2 in front of starting position is also blank
				if row == 1 and self.board[row+2,col] == '--':
					# Add to possible moves
					moves.append(Move((row, col), (row+2,col), self.board))

				# print('{},{} - {}'.format(row, col, len(moves)))

			# Checking diagonals
			if col-1 >= 0:
				if self.board[row+1,col-1][0] == 'w':
					moves.append(Move((row, col), (row+1,col-1), self.board))
			if col+1 < DIMENSION:
				if self.board[row+1,col+1][0] == 'w':
					moves.append(Move((row, col), (row+1,col+1), self.board))

			# En Passant
			# if col-1 >= 0:
			# 	if row == 3 and board[row][col-1] == 'b':

			# if col+1 <= 7:
			# 	if row == 3 and board[row][col+1] == 'b':
	
	# Calculates all moves possible in a set of directions
	# directions holds vectors (v)
	# max_step holds coefficient (m)
	# Calculates all possible m*v
	def moves_in_direction(self, directions, row, col, moves, max_step=DIMENSION-1):
		# Determine enemy colour
		enemy_colour = 'b' if self.whitetomove else 'w'
		# For each direction
		for dx, dy in directions:
			# For each possible step size
			for i in range(1,max_step+1):
				# Set new x,y coords based off step size 
				x = row + i*dx
				y = col + i*dy

				# If still on the board
				if 0<=x<DIMENSION and 0<=y<DIMENSION:
					# Find what's at that location
					piece = self.board[x, y]
					# If nothing, add to valid moves
					if piece == '--':
						moves.append(Move((row, col), (x, y), self.board))
					# If enemy piece, add to valid moves and stop searching in this direction
					elif piece[0] == enemy_colour:
						moves.append(Move((row, col), (x, y), self.board))
						break
					# If our piece, stop searching in this direction
					else:
						break
				# Stop searching in this direction if off board
				else:
					break

	def get_rook_moves(self, row, col, moves):
		# Define movable basis vectors
		directions = ((1,0), (0,1), (-1,0), (0,-1))
		self.moves_in_direction(directions, row, col, moves)

	def get_knight_moves(self, row, col, moves):
		# Define movable basis vectors
		directions = ((2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2))
		self.moves_in_direction(directions, row, col, moves, max_step=1)

	def get_bishop_moves(self, row, col, moves):
		# Define movable basis vectors
		directions = ((1,1), (-1,1), (-1,-1), (1,-1))
		self.moves_in_direction(directions, row, col, moves)

	def get_queen_moves(self, row, col, moves):
		# Define movable basis vectors
		directions = ((1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (-1,-1), (1,-1))
		self.moves_in_direction(directions, row, col, moves)

	def get_king_moves(self, row, col, moves):
		# Define movable basis vectors
		directions = ((1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (-1,-1), (1,-1))
		self.moves_in_direction(directions, row, col, moves, max_step=1)







class Move:
	# maps keys to values
	# key : value
	ranks2rows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
	files2cols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}

	rows2ranks = {v: k for k, v in ranks2rows.items()}
	cols2files = {v: k for k, v in files2cols.items()}

	# Stores all info needed to make move
	def __init__(self, start=None, end=None, board=None):
		self.start = self.Position(start[0], start[1])
		self.end = self.Position(end[0],end[1])
		self.piece_moved = board[self.start.row][self.start.col]
		self.piece_captured = board[self.end.row][self.end.col]
		#Creates a unique ID for each possible move
		self.moveID = self.start.row*1000 + self.start.col*100 + self.end.row*10 + self.end.col

	# subclass for easier reference to row/cols
	class Position:
		def __init__(self, row, col):
			self.row = row
			self.col = col

	#Determines what is '==' to this class
	def __eq__(self, other):
		# If they are the same type of object
		if isinstance(other, Move):
			# Check if the moves are the same
			return self.moveID == other.moveID
		# If not same object, then not equal
		return False


	# Print out start -> end
	def get_chess_notation(self):
		start_move = self.get_rank_and_file(self.start.row, self.start.col)
		end_move = self.get_rank_and_file(self.end.row, self.end.col)
		return start_move + '->'+ end_move

	# Get position in format e.g. e4
	def get_rank_and_file(self, r, c):
		return self.cols2files[c] + self.rows2ranks[r]

import random
from constants import *

# Find a random move and return it
def random_move(valid_moves):
	return valid_moves[random.randint(0, len(valid_moves)-1)]

# Score the board by material
def greedy_move_depth1(gs, valid_moves):
	# Flips sign based on who's turn it is
	turn_multiplier = 1 if gs.whitetomove else -1
	# Start at worst possible value
	best_score = -CHECKMATE_VALUE
	best_moves = []
	# For each move in our turn
	for ally_move in valid_moves:
		# Score the board after making a move
		gs.make_move(ally_move)
		
		# Assign the appropriate values if end of game
		if gs.checkmate:
			score = CHECKMATE_VALUE
		elif gs.stalemate:
			score = STALEMATE_VALUE
		# Otherwise tally up everything
		else:
			score = turn_multiplier * score_material(gs.board)

		# If it's a better move
		if score > best_score:
			# Set new reference point and make it the best move
			best_score = score
			best_moves = [ally_move]
		elif score == best_score:
			best_moves.append(ally_move)

		# Reset board 
		gs.undo_move()

	# Return one of the best scoring moves
	print(len(best_moves), score)
	return best_moves[random.randint(0, len(best_moves) - 1)]

# Score the board by material, taking into account the opponents next move
def greedy_move_depth2(gs, valid_moves):
	# Flips sign based on who's turn it is
	turn_multiplier = 1 if gs.whitetomove else -1
	# Start at worst possible value
	opponent_min_maxscore = CHECKMATE_VALUE
	best_moves = []
	# For each move in our turn
	for player_move in valid_moves:
		# Score the board after making a move
		gs.make_move(player_move)
		opponent_moves = gs.get_valid_moves()
		# Assign the appropriate values if end of game
		if gs.checkmate:
			opponent_maxscore = -CHECKMATE_VALUE
		elif gs.stalemate:
			opponent_maxscore = STALEMATE_VALUE
		# Otherwise run through opponents next move
		else:
			opponent_maxscore = -CHECKMATE_VALUE
			for opponent_move in opponent_moves:
				gs.make_move(opponent_move)
				gs.get_valid_moves()
				# Assign the appropriate values if end of game
				if gs.checkmate:
					score = CHECKMATE_VALUE
				elif gs.stalemate:
					score = STALEMATE_VALUE
				# Otherwise tally up everything
				else:
					score = -turn_multiplier * score_material(gs.board)

				# If it's a better move
				if score > opponent_maxscore:
					# Set new reference point and make it the best move
					opponent_maxscore = score

				# Reset board 
				gs.undo_move()

		# If opponents opportunity for score is lesser
		if  opponent_maxscore < opponent_min_maxscore:
			# Set best move
			opponent_min_maxscore = opponent_maxscore
			best_moves = [player_move]
		# If it's equal
		elif opponent_min_maxscore == opponent_maxscore:
			# Add to best moves
			best_moves.append(player_move)

		# Reset board 
		gs.undo_move()

	# Return one of the best scoring moves
	print(len(best_moves), score)
	return best_moves[random.randint(0, len(best_moves) - 1)]

def minmax_move(gs, valid_moves):
	global next_move
	next_move = None
	random.shuffle(valid_moves)
	turn_multiplier = 1 if gs.whitetomove else -1
	negamax_recursion(gs, valid_moves, DEPTH, turn_multiplier)
	return next_move

def negamax_AB_move(gs, valid_moves):
	global next_move
	next_move = None
	random.shuffle(valid_moves)
	print(len(valid_moves))
	turn_multiplier = 1 if gs.whitetomove else -1
	negamax_AB_recursion(gs, valid_moves, DEPTH, -CHECKMATE_VALUE, CHECKMATE_VALUE, turn_multiplier)
	return next_move


###--------------------------------------------------------------------
# Returns a score based solely on how much material there is on the board
def score_material(board):
	score = 0

	#For each square on the board
	for row in board:
		for sq in row:
			# Count up the material sum of whole board
			if sq[0] == 'w':
				score += VALUES[sq[1]]
			elif sq[0] == 'b':
				score -= VALUES[sq[1]]

	return score

# Returns a score with some thought into how valuable a pieces position is
def score_board(gs):
	# If end of game
	if gs.checkmate:
		# If turn lands on white, black won
		if gs.whitetomove:
			return -CHECKMATE_VALUE
		# Otherwise white wins
		else:
			return CHECKMATE_VALUE
	elif gs.stalemate:
		return STALEMATE_VALUE

	score = 0

	#For each square on the board
	for row in gs.board:
		for sq in row:
			# Count up the material sum of whole board
			if sq[0] == 'w':
				score += VALUES[sq[1]]
			elif sq[0] == 'b':
				score -= VALUES[sq[1]]

	return score


def minmax_recursion(gs, valid_moves, depth, white_to_move):
	global next_move

	# If at end of search, return final score
	if depth == 0:
		return score_material(gs.board)

	# If white's turn
	if white_to_move:
		# Set to worst value
		best_score = -CHECKMATE_VALUE

		# For each possible move
		for move in valid_moves:
			# Make the move and find what's possible afterwards
			gs.make_move(move)
			next_moves = gs.get_valid_moves()
			# Search deeper into minmax tree
			score = minmax_recursion(gs, next_moves, depth-1, False)

			if score > best_score:
				best_score = score
				if depth == DEPTH:
					best_moves.append(move)
			gs.undo_move()
		return best_score
	else:
		best_score = CHECKMATE_VALUE
		for move in valid_moves:
			gs.make_move(move)
			next_moves = gs.get_valid_moves()
			score = minmax_recursion(gs, next_moves, depth-1, True)

			if score < best_score:
				best_score = score
				if depth == DEPTH:
					best_moves.append(move)
			gs.undo_move()
			return best_score


def negamax_recursion(gs, valid_moves, depth, turn_multiplier):
	global next_move
	if depth == 0:
		return turn_multiplier * score_board(gs)

	best_score = -CHECKMATE_VALUE

	for move in valid_moves:
		gs.make_move(move)

		next_moves = gs.get_valid_moves()
		score = -negamax_recursion(gs, next_moves, depth-1, -turn_multiplier)

		if score > best_score:
			best_score = score 
			if depth == DEPTH:
				next_move = move
		gs.undo_move()

	return best_score


def negamax_AB_recursion(gs, valid_moves, depth, alpha, beta, turn_multiplier):
	global next_move
	if depth == 0 or depth > len(valid_moves):
		if depth != 0:
			print('in_fn: {} {}'.format(depth, len(valid_moves)))
		return turn_multiplier * score_board(gs)

	# place move ordering here

	best_score = -CHECKMATE_VALUE
	for move in valid_moves:
		gs.make_move(move)

		next_moves = gs.get_valid_moves()
		# Reverse alpha and beta as that is what opponent will aim at
		score = -negamax_AB_recursion(gs, next_moves, depth-1, -beta, -alpha, -turn_multiplier)

		if score > best_score:
			best_score = score 
			if depth == DEPTH:
				next_move = move
		gs.undo_move()

		if best_score > alpha:
			alpha = best_score
		# Prune worse tree
		if alpha >= beta:
			break

	return best_score

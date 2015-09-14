import sys
import random
import copy
import time

column_dict = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8}
direction = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]]
values = [[120, 10, 31, 26, 26, 31, 10, 120], [10, 0, 21, 22, 22, 21, 0, 10], [30, 21, 25, 24, 24, 25, 21, 30], [26, 22, 24, 22, 22, 24, 22, 26], [26, 22, 24, 22, 22, 24, 22, 26], [30, 21, 25, 24, 24, 25, 21, 30], [10, 0, 21, 22, 22, 21, 0, 10], [120, 10, 31, 26, 26, 31, 10, 120]]

#Function to print the board
def print_board(board):
	for i in range(0,9):
		for j in range(0,9):
			print board[i][j],
		print "\n"

#Function to print board after a turn
def print_turn(board, turn_number, current_player):
	print "The current board:"
	print_board(board)
	print "Turn number: %d, Current Player: %s" %(turn_number, current_player)
	print "Current X Value: %d, Current O Value: %d" %(evaluate(board, "X"), evaluate(board, "O"))

#Print values at game end
def end_game(board, human_player):
	print '-----------------------'
	print "GAME OVER"
	print '-----------------------'
	comp_score,human_score = calculate_score(board, human_player)
	print "FINAL SCORE:"
	print "COMPUTER: %d" %comp_score
	print "YOU: %d" %human_score
	print '-----------------------'
	if(comp_score > human_score):
		print "COMPUTER WINS"
	elif(human_score > comp_score):
		print "YOU WIN"
	else:
		print "IT'S A DRAW"

#Reset the board/Returns Board
def reset_board(board):
	board = make_new_board()
	return board

#Make a new board/Returns Board
def make_new_board():
	board = []
	for i in range(0,9):
		board.append(["."] * 9)
	for i in range(1,9):
		board[i-1][0] = i
	board[8][1] = "A"
	board[8][2] = "B"
	board[8][3] = "C"
	board[8][4] = "D"
	board[8][5] = "E"
	board[8][6] = "F"
	board[8][7] = "G"
	board[8][8] = "H"

	board[8][0] = " "

	#Starting position of pieces
	board[4][4] = 'X'
	board[4][5] = 'O'
	board[5][4] = 'O'
	board[5][5] = 'X'
	return board

#Function to change the player
def opposite(current_player):
	if current_player == "X":
		player = "O"
	else:
		player = "X"
	return player

#Change the turn to other player/Returns Turn_numer and current_player
def change_turn(board, turn_number, current_player):
	turn_number += 1 #Change turns
	print "Turn Over."
	print "----------"
	if(current_player == "X"):
		current_player = "O"
	else:
		current_player = "X"
	print_turn(board, turn_number, current_player)

	return turn_number, current_player

#Pass Turn to other player/Returns turn_number, current_player, pass_counter
def pass_turn(board, turn_number, current_player, pass_counter, human_player):
	turn_number += 1
	print "Turn Over."
	print "----------"
	if current_player == "X":
		current_player = "O"
	else:
		current_player = "X"
	pass_counter += 1

	if(pass_counter == 2):
		end_game(board, human_player)
	print_turn(board, turn_number, current_player)

	return turn_number, current_player, pass_counter

#Make move/Returns Board
def make_move(board, row_position, column_position, current_player):
	#Valid move returns the direction of the pieces to be flipped
	x = valid_move(board, row_position, column_position, current_player)
	for i in x:
		row = row_position
		column = column_position
		board[row][column] = "." #Set Current Piece to Blank. It will be changed soon.
		while(on_board(row, column) and board[row][column] != current_player):
			board[row][column] = current_player #Change all pieces in current direction until reaching same color piece
			row += direction[i][0]
			column += direction[i][1]
	return board

#Check if move is on board/Return True or False
def on_board(row_position, column_position):
	if(row_position >= 0 and row_position <= 7 and column_position >= 1 and column_position <= 8):
		return True
	else:
		return False

#Check if move is a valid move/Return possible directions for moving
def valid_move(board, row_position, column_position, current_player):
	#row_position and column_position are original positions which player places
	#row and column are tiles to be flipped, if possible
	possible_directions = []

	if current_player == "O":
		opposite_player = "X"
	else:
		opposite_player = "O"

	#If position is out of board range
	if(row_position < 0 or row_position > 7 or column_position < 1 or column_position > 8):
		return -1
	#If position is not yet filled
	if(board[row_position][column_position] != "."):
		return -1
	#Check to see if there is another piece of same color in any direction
	for row_direction, column_direction in direction:
		#Reset row and column to where the piece was placed
		row = row_position
		column = column_position
		num_piece_between = 0

		row += row_direction
		column += column_direction

		while(on_board(row,column)):
			if(board[row][column] == "."):
				break
			elif(board[row][column] == current_player and num_piece_between == 0):
				break
			elif(board[row][column] == current_player):
				possible_directions.append(direction.index([row_direction, column_direction]))
				break
			else:
				row += row_direction
				column += column_direction
				num_piece_between += 1
	if len(possible_directions) == 0:
		return -1
	else:
		return possible_directions

#Calculate final score/Return computer score and human score
def calculate_score(board, human_player):
	if(human_player == "X"):
		computer_player = "O"
	else:
		computer_player = "X"
	human_score = 0
	comp_score = 0
	for i in range(0,9):
		for j in range(0,9):
			if(board[i][j] == human_player):
				human_score += 1
			elif(board[i][j] == computer_player):
				comp_score += 1
			else:
				continue
	return comp_score, human_score

#Get all possible moves for computer/Return set of all possible moves
def get_computer_moves(board, current_player):
	#Get all possible moves for the computer in this turn
	possible_moves = []
	for x in range(0,8):
		for y in range(1,9):
			if (valid_move(board, x, y, current_player) != -1):
				possible_moves.append([x,y])
	return possible_moves

#Check if it is possible for human to make move/Returns True or False
def possible_to_make_move(board, current_player):
	sum = 0
	for i in range(0,8):
		for j in range(1,9):
			if(valid_move(board, i, j, current_player) == -1):
				sum += 0
			else:
				sum += 1
				break
		if(sum != 0):
			break
	if sum == 0:
		return False
	else:
		return True

#Check if the game is over/Returns True or False
def gameOver(board):
	sum = 0
	for i in range(0,8):
		for j in range(1,9):
			if(valid_move(board, i, j, "O") == -1 and valid_move(board, i, j, "X") == -1):
				sum += 0
			else:
				sum += 1
				break
		if(sum != 0):
			break
	if sum == 0:
		return True
	else:
		return False

#Evaluate the board for a player/Returns Player Value
def evaluate(board, player):
	total_value = 0
	for i in range(0, 9):
		for j in range(0, 9):
			if board[i][j] == player:
				total_value += values[i][j - 1]
	return total_value

#Use the minimax algorithm with alpha-beta pruning to determine best move for computer/Returns best move
def minimax(board, computer_player, current_player, depth, max_depth, alpha, beta):
	moves = get_computer_moves(board, current_player)
	if(gameOver(board) or depth == max_depth or moves == []):
		best_move = [-1,-1]
		return evaluate(board, current_player), best_move
	best_move = [-1,-1]

	if(current_player == computer_player):
		best_score = float("-inf")
		for move in moves:
			new_board = copy.deepcopy(board)
			new_board = make_move(new_board, move[0], move[1], current_player)
			score, the_move = minimax(new_board, computer_player, opposite(current_player), depth + 1, max_depth, alpha, beta)
			best_score = max(best_score, score)
			if score > alpha:
				alpha = score
				best_move = move
			if beta <= alpha: 
				break
		return alpha, best_move
	else:
		best_score = float("inf")
		for move in moves:
			new_board = copy.deepcopy(board)
			new_board = make_move(new_board, move[0], move[1], current_player)
			score, move = minimax(new_board, computer_player, opposite(current_player), depth + 1, max_depth, alpha, beta)
			best_score = max(best_score, score)
			if score < beta:
				beta = score
				best_move = move
			if beta <= alpha:
				break
		return beta, best_move			

#Initially, a greedy algorithm was how the computer chose but I revised it to minimax with alpha-beta pruning.
def greedy_algorithm(board, moves, current_player, human_player):
	comp_score, human_score = calculate_score(board, human_player)
	best_move = []
	for move in moves:
		new_board = copy.deepcopy(board)
		new_board = make_move(new_board, move[0], move[1], current_player)
		new_moves = get_computer_moves(board, current_player)
		new_comp_score, new_human_score = calculate_score(new_board, human_player)

		if(new_comp_score > comp_score):
			comp_score = new_comp_score
			best_move = move
	return best_move

#Play the game
def play_game():
	board = make_new_board() #Make the board
	turn_number = 1 #Set turn number to 1
	current_player = "O" #O always starts
	max_depth = 7 #Max depth for minimax

	human_player = raw_input("Choose a piece, X or O: ") #Get human input for which side they want to be

	if human_player == "X":
		computer_player = "O"
	else:
		computer_player = "X"

	if turn_number % 2 == 1:
		current_player = "O"
	else:
		current_player = "X"

	pass_counter = 0 #If both human and computer pass consecutively, end game

	print_turn(board, turn_number, current_player)

	while(not gameOver(board)):
		if(current_player == computer_player):
			moves = get_computer_moves(board, current_player)

			if len(moves) == 0: #IF NO AVAILABLE MOVES, PASS TO HUMAN
				turn_number, current_player, pass_counter = pass_turn(board, turn_number, current_player, pass_counter, human_player)
			best_score, random_move = minimax(board, computer_player, current_player, 0, max_depth, float("-inf"), float("inf"))
			#random_move = greedy_algorithm(board, moves, current_player, human_player)
			#random_move = random.choice(moves)
			#best_score, random_move = negamax(board, 0, max_depth, current_player, human_player) #Choose a random allowed move for the computer

			row_position = random_move[0]
			column_position = random_move[1]
		else:
			new_piece = raw_input("Place a piece in the format 'A1': ") #Ask user for move
			new_piece = new_piece.lower()
			while new_piece.lower() == "pass": #IF HUMAN PASSES, PASS TURN TO COMPUTER
				if(possible_to_make_move(board, current_player)):
					print "You can make a move, so you cannot pass."
					new_piece = raw_input("Place a piece in the format 'A1': ")
				else:
					turn_number, current_player, pass_counter = pass_turn(board, turn_number, current_player, pass_counter, human_player)
					continue
			new_piece = new_piece.upper()
			row_position = int(new_piece[1]) - 1
			column_position = column_dict[new_piece[0]]

		if(valid_move(board, row_position, column_position, current_player) != -1):
			board = make_move(board, row_position, column_position, current_player)
			turn_number, current_player = change_turn(board, turn_number, current_player)

	if(turn_number == turn_max):
		end_game(board, human_player)

play_game()



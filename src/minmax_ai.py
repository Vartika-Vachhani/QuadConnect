import math
import random

# Importing constants and functions from other modules
from variables import ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE
from functions import is_valid_location, game_over_check, get_next_open_row, drop_piece
from score_ai import score_position

# Getting valid locations for AI
def get_valid_locations(board):
    """
    Returns a list of valid column indices where a piece can be dropped in the current board configuration.
    """
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

# Checking for terminal nodes (end of the game)
def is_terminal_node(board):
    """
    Checks if the game is over by either a player winning or the board being full.
    """
    return game_over_check(board, PLAYER_PIECE) or game_over_check(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Implementing the minimax algorithm
def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Implements the minimax algorithm with alpha-beta pruning for determining the best move for the AI player.
    """
    valid_locations = get_valid_locations(board)

    # Checking if it's a terminal node (end of the game)
    if isTerminal := is_terminal_node(board):
        if game_over_check(board, AI_PIECE):
            return (None, math.inf)  # AI wins, return positive infinity
        elif game_over_check(board, PLAYER_PIECE):
            return (None, -math.inf)  # Player wins, return negative infinity
        else: 
            return (None, 0)  # It's a draw, return 0
    elif depth == 0:  # If maximum depth is reached
        return (None, score_position(board, AI_PIECE))  # Evaluate the board position

    if maximizing_player:
        # Maximizing player (AI)
        value = -math.inf  # Initialize value to negative infinity
        column = random.choice(valid_locations)  # Choose a random column initially

        # Iterate through each valid column
        for c in valid_locations:
            r = get_next_open_row(board, c)  # Get the next available row in the column
            temp_board = board.copy()  # Create a copy of the board
            drop_piece(temp_board, r, c, AI_PIECE)  # Drop AI's piece in the column
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]  # Recur for the next depth with minimizing player

            if new_score > value:
                value = new_score  # Update the value if the new score is higher
                column = c  # Update the column to be chosen
            
            alpha = max(alpha, value)  # Update alpha with the maximum value encountered

            if alpha >= beta:  # Alpha-beta pruning
                break

    else:
        # Minimizing player (Player)
        value = math.inf  # Initialize value to positive infinity
        column = random.choice(valid_locations)  # Choose a random column initially

        # Iterate through each valid column
        for c in valid_locations:
            r = get_next_open_row(board, c)  # Get the next available row in the column
            temp_board = board.copy()  # Create a copy of the board
            drop_piece(temp_board, r, c, PLAYER_PIECE)  # Drop player's piece in the column
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]  # Recur for the next depth with maximizing player

            if new_score < value:
                value = new_score  # Update the value if the new score is lower
                column = c  # Update the column to be chosen

            beta = min(beta, value)  # Update beta with the minimum value encountered

            if alpha >= beta:  # Alpha-beta pruning
                break
            
    return column, value

from Bots.ChessBotList import register_chess_bot
from Bots.Piece_movement import all_move_piece
import time
import copy 
import numpy as np

value_piece = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0,
}

def get_all_possible_moves(player_sequence, board):
    current_player = player_sequence[1]

    all_move = []

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != '' and board[y][x][1] == current_player:
                moves = all_move_piece(y, x, board)

                for i in moves:
                    all_move.append(((y,x), i))

    return all_move

def winner(board): 
    has_white = False 
    has_black = False 
    for row in board: 
        for piece in row: 
            if piece == "kw": 
                has_white = True 
            if piece == "kb": 
                has_black = True 
    
    if not has_white: 
        return "b" 
    
    if not has_black: 
        return "w" 
    
    return None

def evaluate(board, player_sequence):
    score = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != '':
                if board[i][j][1] == player_sequence[1]:
                    score += value_piece[board[i][j][0]]
                else:
                    score -= value_piece[board[i][j][0]]
    return score


def minimax(board, depth, alpha, beta, maximizingplayer, player_sequence, other_player_sequence, start_time, time_budget):
    if time.time() - start_time >= time_budget - 0.1:
        return evaluate(board, player_sequence)
    win = winner(board)
    if win == player_sequence[1]:
        return float('inf')
    elif win == other_player_sequence[1]:
        return -float('inf')
    
    if depth == 0:
        return evaluate(board, player_sequence)
    
    if maximizingplayer:
        current_max = -float('inf')
        moves = get_all_possible_moves(player_sequence, board)

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''

            new_board = np.rot90(new_board, 2)

            score = minimax(new_board, depth-1, alpha, beta, False, player_sequence, other_player_sequence, start_time, time_budget)
            current_max = max(current_max, score)
            alpha = max(alpha, score)

            if beta <= alpha:
                break

        return current_max
    else:
        current_min = float('inf')
        moves = get_all_possible_moves(other_player_sequence, board)

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''

            new_board = np.rot90(new_board, 2)

            score = minimax(new_board, depth-1, alpha, beta, True, player_sequence, other_player_sequence, start_time, time_budget)
            current_min = min(current_min, score)
            beta = min(beta, score)
            if beta <= alpha:
                break

        return current_min

def get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time):
    moves = get_all_possible_moves(player_sequence, board)
    
    best_score = -float('inf')
    best_move = moves[0]
    alpha = -float('inf')
    beta = float('inf')

    for move in moves:
        if time.time() - start_time >= time_budget - 0.1:
            break

        new_board = copy.deepcopy(board)
        new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
        new_board[move[0][0]][move[0][1]] = ''

        new_board = np.rot90(new_board, 2)

        score = minimax(new_board, depth-1, alpha, beta, False, player_sequence, other_player_sequence,start_time, time_budget)

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)

        if (time.time() - start_time >= time_budget - 0.2):
            return best_move

    return best_move

def chess_bot(player_sequence, board, time_budget, **kwargs):

    start_time = time.time()

    other_player_sequence = ""
    if player_sequence == "0w0":
        other_player_sequence = "1b2"
    else:
        other_player_sequence = "0w0"

    piece_count = 0
    for i in board:
        for j in i:
            if j != '':
                piece_count += value_piece[j[0]]
    
    if piece_count >= 40:
        depth = 5
    elif piece_count >= 30:
        depth = 6
    elif piece_count >= 20:
        depth = 7
    else:
        depth = 8

    best_move = get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time)
    return best_move

register_chess_bot("RodFav_Simple_AlphaBeta", chess_bot)
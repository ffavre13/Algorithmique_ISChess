from Bots.ChessBotList import register_chess_bot
from Bots.Piece_movement import move_piece
import time
import random
import numpy as np

value_piece = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 100
}

def get_all_possible_moves(player_sequence, board):
    current_player = player_sequence[1]

    all_move = []

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != '' and board[y][x][1] == current_player:
                moves, eat = move_piece(y, x, board)

                for i in moves:
                    all_move.append(((y,x), i))
                
                for j in eat:
                    all_move.append(((y,x), j))

    return all_move

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


def chess_bot(player_sequence, board, time_budget, **kwargs):

    best_move = (0,0), (0,0)

    def maxi(depth, board):
        nonlocal best_move

        if depth == 0:
            return evaluate(board,player_sequence)
        
        current_max = -float('inf')
        
        all_possible_move = get_all_possible_moves(player_sequence, board)

        for move in all_possible_move:
            new_board = np.copy(board)
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''
            current_score = mini(depth-1, np.copy(new_board))

            if current_score > current_max:
                current_max = current_score
                best_move = move

        return current_max        

    def mini(depth, board):
        if depth == 0:
            return -evaluate(board, player_sequence)
        
        current_min = float('inf')
        
        all_possible_move = get_all_possible_moves(player_sequence, board)

        for move in all_possible_move:
            new_board = np.copy(board)
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''
            current_score = maxi(depth-1, np.copy(new_board))

            if current_score < current_min:
                current_min = current_score

        return current_min 

    maxi(2, board)
    print(best_move)
    return best_move

register_chess_bot("RodFav_Random_MiniMax", chess_bot)
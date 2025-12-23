from Bots.ChessBotList import register_chess_bot
from Bots.Piece_movement import move_piece, all_move_piece
import time
import random

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
                moves = all_move_piece(y, x, board)
                for i in moves:
                    all_move.append(((y,x), i))

    return all_move

def chess_bot(player_sequence, board, time_budget, **kwargs):
    start_time = time.time()
    moves = get_all_possible_moves(player_sequence, board)
    print(moves)

    current_best_move = moves[random.randint(0,len(moves)-1)]
    return current_best_move

register_chess_bot("Naif", chess_bot)
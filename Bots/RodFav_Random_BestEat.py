from Bots.ChessBotList import register_chess_bot
from Bots.Piece_movement import move_piece
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
    all_eat = []

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != '' and board[y][x][1] == current_player:
                moves, eat = move_piece(y, x, board)

                for i in moves:
                    all_move.append(((y,x), i))
                
                for j in eat:
                    all_eat.append(((y,x), j))

    return all_move, all_eat

def chess_bot(player_sequence, board, time_budget, **kwargs):
    start_time = time.time()
    moves, moves_eat = get_all_possible_moves(player_sequence, board)
    if len(moves_eat) != 0:
        move_values = []
        for i in moves_eat:
            y, x = i[1]
            piece = board[y][x][0]
            move_values.append((i, value_piece[piece]))

        best = move_values[0]
        for mv in move_values:
            if mv[1] > best[1]:
                best = mv

        best_move = best[0]
        return best_move
    else:
        current_best_move = moves[random.randint(0,len(moves)-1)]
        return current_best_move

register_chess_bot("RodFav_Random_BestEat", chess_bot)
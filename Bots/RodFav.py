from Bots.ChessBotList import register_chess_bot
import time
import random

def get_all_possible_moves(play_sequence, board):
    moves = []

    print(play_sequence)
    print(board)

    moves.append(((1,0),(2,0)))
    moves.append(((1,1),(2,1)))
    moves.append(((1,2),(2,2)))
    moves.append(((1,3),(2,3)))
    moves.append(((1,4),(2,4)))
    moves.append(((1,5),(2,5)))
    moves.append(((1,6),(2,6)))
    moves.append(((1,7),(2,7)))

    moves.append(((0,0),(1,0)))
    moves.append(((0,1),(1,1)))
    moves.append(((0,2),(1,2)))
    moves.append(((0,3),(1,3)))
    moves.append(((0,4),(1,4)))
    moves.append(((0,5),(1,5)))
    moves.append(((0,6),(1,6)))
    moves.append(((0,7),(1,7)))

    return moves

def chess_bot(player_sequence, board, time_budget, **kwargs):
    start_time = time.time()
    moves = get_all_possible_moves(player_sequence, board)
    current_best_move = moves[random.randint(0,len(moves)-1)]

    while True:
        if (time.time() - start_time >= time_budget - 0.05):
            return current_best_move
        
register_chess_bot("RodFav", chess_bot)
from Bots.ChessBotList import register_chess_bot
import time
import random


def get_move_king(y,x,board):
    possible_positions = []
    return possible_positions

def get_move_queen(y,x,board):
    possible_positions = []
    return possible_positions

def get_move_knight(y,x,board):
    possible_positions = []
    return possible_positions

def get_move_bishop(y,x,board):
    possible_positions = []
    return possible_positions

def get_move_rook(y,x,board):
    possible_positions = []
    return possible_positions

def get_move_pawn(y,x,board):
    possible_positions = []

    try:
        if board[y+1][x] == '':
            possible_positions.append((y+1,x))
    except:
        pass

    try:
        if board[y+1][x+1] != '':
            possible_positions.append((y+1,x+1))
    except:
        pass

    try:
        if board[y+1][x-1] != '':
            possible_positions.append((y+1,x-1))
    except:
        pass

    return possible_positions

def get_all_possible_moves(player_sequence, board):
    moves = []
    current_player = player_sequence[1]

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '':
                if board[i][j].string()[1] == current_player:
                    match board[i][j].string()[0]:
                        case "k":
                            for position in get_move_king(i,j,board):
                                moves.append(((i,j),position))
                        case "q":
                            for position in get_move_queen(i,j,board):
                                moves.append(((i,j),position))
                        case "n":
                            for position in get_move_knight(i,j,board):
                                moves.append(((i,j),position))
                        case "b":
                            for position in get_move_bishop(i,j,board):
                                moves.append(((i,j),position))
                        case "r":
                            for position in get_move_rook(i,j,board):
                                moves.append(((i,j),position))
                        case "p":
                            for position in get_move_pawn(i,j,board):
                                moves.append(((i,j),position))

    return moves

def chess_bot(player_sequence, board, time_budget, **kwargs):
    start_time = time.time()
    moves = get_all_possible_moves(player_sequence, board)
    current_best_move = moves[random.randint(0,len(moves)-1)]

    while True:
        if (time.time() - start_time >= time_budget - 0.05):
            return current_best_move
        
register_chess_bot("RodFav", chess_bot)
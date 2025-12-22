from Bots.ChessBotList import register_chess_bot
from Bots.Piece_movement import all_move_piece
import time
import copy 

value_piece = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k":1000,
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


def minimax(board, depth, maximizingplayer, player_sequence, other_player_sequence):
    if depth == 0 or winner(board) != None:
        return evaluate(board, player_sequence)
    
    if maximizingplayer:
        current_max = -float('inf')
        moves = get_all_possible_moves(player_sequence, board)

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''
            score = minimax(new_board, depth-1, False, player_sequence, other_player_sequence)
            current_max = max(current_max, score)
        return current_max
    else:
        current_min = float('inf')
        moves = get_all_possible_moves(other_player_sequence, board)

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''
            score = minimax(new_board, depth-1, True, player_sequence, other_player_sequence)
            current_min = min(current_min, score)
        return current_min

def get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time):
    best_score = -float('inf')
    best_move = None

    for move in get_all_possible_moves(player_sequence, board):
        new_board = copy.deepcopy(board)
        new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
        new_board[move[0][0]][move[0][1]] = ''

        score = minimax(new_board, depth-1, False, player_sequence, other_player_sequence)

        if score > best_score:
            best_score = score
            best_move = move

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

    best_move = get_best_move(board,5,player_sequence,other_player_sequence, time_budget, start_time)
    return best_move

register_chess_bot("RodFav_Simple_MiniMax", chess_bot)
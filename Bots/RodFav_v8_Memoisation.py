from Bots.ChessBotList import register_chess_bot
from Bots.Piece_movement import all_move_piece, all_move_piece_reverse
import time

value_piece = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0,
}

def board_to_hash(board, player_sequence):
    return ''.join([''.join(row) for row in board]) + player_sequence

def move_score(move, board):
    (y1, x1), (y2, x2) = move
    piece = board[y1][x1]
    target = board[y2][x2]

    score = 0

    if target != '' and target[0] == 'k':
        return 100000

    if piece[0] == 'p' and y2 == 7:
        score += 900

    if target != '':
        score += 10 * value_piece[target[0]] - value_piece[piece[0]]

    return score

def get_all_possible_moves_reverse(player_sequence, board):
    current_player = player_sequence[1]

    all_move = []

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != '' and board[y][x][1] == current_player:
                moves = all_move_piece_reverse(y, x, board)

                for i in moves:
                    all_move.append(((y,x), i))

    return all_move

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

def evaluate(board, player_sequence):
    score = 0

    center_square = [(3,3),(3,4),(4,3),(4,4)]

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != '':
                piece = board[y][x][0]
                color = board[y][x][1]
                val = value_piece[piece]

                if (y,x) in center_square:
                    val += 0.5

                moves = all_move_piece(y, x, board) if color == player_sequence[1] else all_move_piece_reverse(y, x, board)
                
                val = val + 0.01 * len(moves) if len(moves) != 0 else val - 0.01

                if color == player_sequence[1]:
                    moves = all_move_piece(y,x,board)
                else:
                    moves = all_move_piece_reverse(y,x,board)
                    val += 0.05 * len(moves)

                if color == player_sequence[1]:
                    score += val
                else:
                    score -= val
    return score


def minimax(board, depth, alpha, beta, maximizingplayer, player_sequence, other_player_sequence, start_time, time_budget, positions):
    if time.time() - start_time >= time_budget - 0.1:
        return evaluate(board, player_sequence)
    
    key = board_to_hash(board, player_sequence) if maximizingplayer else board_to_hash(board, other_player_sequence)
    if key in positions:
        stored_score, stored_depth = positions[key]
        if stored_depth >= depth:
            return stored_score

    if depth == 0:
        score = evaluate(board, player_sequence)
        positions[key] = (score, depth)
        return score
    
    if maximizingplayer:
        current_max = -float('inf')
        moves = get_all_possible_moves(player_sequence, board)

        moves.sort(key=lambda m: move_score(m, board),reverse=True)

        for move in moves:
            if board[move[1][0]][move[1][1]] == 'k'+str(other_player_sequence[1]):
                score = 10000 + depth
                current_max = max(current_max, score)
                alpha = max(alpha, score)

                if beta <= alpha:
                    break
                
                continue
            
            captured = board[move[1][0]][move[1][1]]
            piece = board[move[0][0]][move[0][1]]

            if move[1][0] == 7 and board[move[0][0]][move[0][1]] == 'p'+str(player_sequence[1]):
                board[move[1][0]][move[1][1]] = 'q'+str(player_sequence[1])
                board[move[0][0]][move[0][1]] = ''
            else:
                board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
                board[move[0][0]][move[0][1]] = ''

            score = minimax(board, depth-1, alpha, beta, False, player_sequence, other_player_sequence, start_time, time_budget, positions)
            current_max = max(current_max, score)
            alpha = max(alpha, score)

            board[move[1][0]][move[1][1]] = captured
            board[move[0][0]][move[0][1]] = piece

            if beta <= alpha:
                break

        positions[key] = (current_max, depth)
        return current_max
    else:
        current_min = float('inf')
        moves = get_all_possible_moves_reverse(other_player_sequence, board)
        moves.sort(key=lambda m: move_score(m, board),reverse=True)

        for move in moves:
            if board[move[1][0]][move[1][1]] == 'k'+str(player_sequence[1]):
                score = -10000 - depth
                current_min = min(current_min, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
                continue
            
            captured = board[move[1][0]][move[1][1]]
            piece = board[move[0][0]][move[0][1]]

            if move[1][0] == 7 and board[move[0][0]][move[0][1]] == 'p'+str(other_player_sequence[1]):
                board[move[1][0]][move[1][1]] = 'q'+str(other_player_sequence[1])
                board[move[0][0]][move[0][1]] = ''
            else:
                board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
                board[move[0][0]][move[0][1]] = ''

            score = minimax(board, depth-1, alpha, beta, True, player_sequence, other_player_sequence, start_time, time_budget, positions)
            current_min = min(current_min, score)
            beta = min(beta, score)

            board[move[1][0]][move[1][1]] = captured
            board[move[0][0]][move[0][1]] = piece

            if beta <= alpha:
                break

        positions[key] = (current_min, depth)
        return current_min

def get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time, positions):
    moves = get_all_possible_moves(player_sequence, board)
    moves.sort(key=lambda m: move_score(m, board),reverse=True)

    best_score = -float('inf')
    best_move = moves[0]
    alpha = -float('inf')
    beta = float('inf')

    for move in moves:
        if time.time() - start_time >= time_budget - 0.1:
            break

        if board[move[1][0]][move[1][1]] == 'k'+str(other_player_sequence[1]):
            score = 10000 + depth

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            continue

        captured = board[move[1][0]][move[1][1]]
        piece = board[move[0][0]][move[0][1]]
        
        if move[1][0] == 7 and board[move[0][0]][move[0][1]] == 'p'+str(player_sequence[1]):
            board[move[1][0]][move[1][1]] = 'q'+str(player_sequence[1])
            board[move[0][0]][move[0][1]] = ''
        else:
            board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
            board[move[0][0]][move[0][1]] = ''

        score = minimax(board, depth-1, alpha, beta, False, player_sequence, other_player_sequence,start_time, time_budget, positions)

        if score > best_score:
            best_score = score
            best_move = move

        board[move[1][0]][move[1][1]] = captured
        board[move[0][0]][move[0][1]] = piece

        alpha = max(alpha, score)

    return best_move

def chess_bot(player_sequence, board, time_budget, **kwargs):

    start_time = time.time()
    positions = {}
    
    depth = 3

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
        depth = 3
    elif piece_count >= 30:
        depth = 3
    elif piece_count >= 20:
        depth = 4
    else:
        depth = 5

    best_move = get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time, positions)
    return best_move

register_chess_bot("RodFav_Memoisation", chess_bot)
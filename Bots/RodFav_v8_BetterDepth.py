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

history = []
history_size = 12
last_move = None

def board_to_hash(board, player_sequence):
    result = ""
    for row in board:
        for c in row:
            if c != '':
                result += c
            else:
                result += "--"
    result += player_sequence
    return result

# Heuristic for sorting moves
def move_score(move, board, maximazing):
    (y1, x1), (y2, x2) = move
    piece = board[y1][x1]
    target = board[y2][x2]

    score = 0

    # the move take the king
    if target != '' and target[0] == 'k':
        return 100000
    
    # promotion
    if maximazing:
        if piece[0] == 'p' and y2 == 7:
            score += 900
    else:
        if piece[0] == 'p' and y2 == 0:
            score += 900

    # capture a piece with a weaker piece
    if target != '':
        score += 10 * value_piece[target[0]] - value_piece[piece[0]]

    return score

# Get all the oponent moves
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

# Get all current player moves
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

# Evaluate the board
def evaluate(board, player_sequence):
    score = 0

    center_square = [(3,3),(3,4),(4,3),(4,4)]

    endgame = False
    material = 0

    king_oponent_position = None

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != '':
                piece = board[y][x][0]
                val = value_piece[piece]
                material += val
                if board[y][x][0] == 'k' and board[y][x][1] != player_sequence[1]:
                    king_oponent_position = (y,x)

    if material < 20:
        endgame = True

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != '':
                piece = board[y][x][0]
                color = board[y][x][1]
                val = value_piece[piece]

                # Bonus if the piece is in the center_square
                if (y,x) in center_square and piece != 'k':
                    val += 0.5

                # Bonus based on possible movements of the piece 
                moves = all_move_piece(y, x, board) if color == player_sequence[1] else all_move_piece_reverse(y, x, board)                
                val += 0.02 * min(len(moves), 8)

                # check the king
                if king_oponent_position in moves:                 
                    val += 20.0

                # Bonus if the piece are advanced on the board
                if piece != 'k':
                    if color == player_sequence[1]:
                        val += 0.05 * y
                    else:
                        val += 0.05 * (7 - y)

                # Bonus if the pawn are advanced on the board
                if piece == 'p':
                    if color == player_sequence[1]:
                        val += 0.2 * y
                    else:
                        val += 0.2 * (7 - y)

                # Malus if the oponent pawn will soon promote
                if piece == 'p' and color != player_sequence[1]:
                    if y == 1:  
                        val += 2.5

                # Malus if the knight, bishop, rook and queen are on the first line
                if piece in ['n', 'b', 'r', 'q']:
                    if color == player_sequence[1]:
                        if y == 0:
                            val -= 0.3
                    else:
                        if y == 7:
                            val -= 0.3

                # Malus if the king is advanced on the board and bonus if the king is active in the endgame phase
                if piece == 'k':
                    if not endgame:
                        if x in [3, 4] and y not in [0,7]:
                            val -= 0.8

                        if color == player_sequence[1]:
                            if y > 1:
                                val -= 0.5
                        else:
                            if y < 6:
                                val -= 0.5
                    else:
                        if (y, x) in [(3,3),(3,4),(4,3),(4,4)]:
                            val += 1.0
                        elif 2 <= y <= 5 and 2 <= x <= 5:
                            val += 0.5
                        else:
                            val -= 0.5

                if color == player_sequence[1]:
                    score += val
                else:
                    score -= val

    return score

# Minimax algorithme
def minimax(board, depth, alpha, beta, maximizingplayer, player_sequence, other_player_sequence, start_time, time_budget):
    if time.time() - start_time >= time_budget - 0.1:
        return evaluate(board, player_sequence)
    
    if depth == 0:
        return evaluate(board, player_sequence)
    
    if maximizingplayer:
        current_max = -float('inf')
        moves = get_all_possible_moves(player_sequence, board)

        moves.sort(key=lambda m: move_score(m, board, True),reverse=True)

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

            score = minimax(board, depth-1, alpha, beta, False, player_sequence, other_player_sequence, start_time, time_budget)
            current_max = max(current_max, score)
            alpha = max(alpha, score)

            board[move[1][0]][move[1][1]] = captured
            board[move[0][0]][move[0][1]] = piece

            if beta <= alpha:
                break

        return current_max
    else:
        current_min = float('inf')
        moves = get_all_possible_moves_reverse(other_player_sequence, board)
        moves.sort(key=lambda m: move_score(m, board, False),reverse=True)

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

            if move[1][0] == 0 and board[move[0][0]][move[0][1]] == 'p'+str(other_player_sequence[1]):
                board[move[1][0]][move[1][1]] = 'q'+str(other_player_sequence[1])
                board[move[0][0]][move[0][1]] = ''
            else:
                board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
                board[move[0][0]][move[0][1]] = ''

            score = minimax(board, depth-1, alpha, beta, True, player_sequence, other_player_sequence, start_time, time_budget)
            current_min = min(current_min, score)
            beta = min(beta, score)

            board[move[1][0]][move[1][1]] = captured
            board[move[0][0]][move[0][1]] = piece

            if beta <= alpha:
                break

        return current_min

def get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time):
    global last_move, history

    moves = get_all_possible_moves(player_sequence, board)
    moves.sort(key=lambda m: move_score(m, board, True),reverse=True)

    allowed_moves = []
    for move in moves:
        if last_move is not None:
            if move[0] == last_move[1] and move[1] == last_move[0]:
                continue

        (y1, x1), (y2, x2) = move
        captured = board[y2][x2]
        piece = board[y1][x1]

        if y2 == 7 and board[y1][x1] == 'p'+str(player_sequence[1]):
            board[y2][x2] = 'q'+str(player_sequence[1])
            board[y1][x1] = ''
        else:
            board[y2][x2] = board[y1][x1]
            board[y1][x1] = ''

        key = board_to_hash(board, other_player_sequence)

        board[y1][x1] = piece
        board[y2][x2] = captured

        if history.count(key) >= 2:
            continue

        allowed_moves.append(move)

    if not allowed_moves:
        allowed_moves = moves


    best_score = -float('inf')
    best_move = allowed_moves[0]

    alpha = -float('inf')
    beta = float('inf')

    for move in allowed_moves:
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

        score = minimax(board, depth-1, alpha, beta, False, player_sequence, other_player_sequence,start_time, time_budget)

        if score > best_score:
            best_score = score
            best_move = move

        board[move[1][0]][move[1][1]] = captured
        board[move[0][0]][move[0][1]] = piece

        alpha = max(alpha, score)

    return best_move

def chess_bot(player_sequence, board, time_budget, **kwargs):
    global history, last_move, history_size
    
    start_time = time.time()

    key = board_to_hash(board, player_sequence)
    history.append(key)
    if len(history) > history_size:
        history.pop(0)

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
        depth = 4
    elif piece_count >= 30:
        depth = 5
    elif piece_count >= 20:
        depth = 6
    else:
        depth = 7

    best_move = get_best_move(board, depth, player_sequence, other_player_sequence, time_budget, start_time)

    last_move = best_move

    return best_move

register_chess_bot("RodFav_BetterDepth", chess_bot)
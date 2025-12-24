from Bots.ChessBotList import register_chess_bot
import time
import random

def get_move_king(y,x,board):
    possible_positions = []

    # en haut a gauche
    posy = y + 1
    posx = x + 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # au mid a gauche
    posy = y
    posx = x + 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en bas a gauche
    posy = y - 1
    posx = x + 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))
    
    # en haut
    posy = y + 1
    posx = x
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en bas
    posy = y - 1
    posx = x
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en haut a droite
    posy = y + 1
    posx = x - 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # au mid a droite
    posy = y
    posx = x - 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en bas a droite
    posy = y - 1
    posx = x - 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    return possible_positions

def get_move_queen(y,x,board):
    possible_positions = []

    ## Cardinales 
    #Haut
    for i in range(1, len(board)-y):
        if board[y+i,x] == '':
            possible_positions.append((y+i,x))
        elif board[y,x][1] != board[y+i,x][1]:
            possible_positions.append((y+i,x))
            break
        else:
            break
    
    #Droite
    for i in range(1, x+1):
        if board[y,x-i] == '':
            possible_positions.append((y,x-i))
        elif board[y,x][1] != board[y,x-i][1]:
            possible_positions.append((y,x-i))
            break
        else:
            break
    
    #Bas
    for i in range(1, y+1):
        if board[y-i,x] == '':
            possible_positions.append((y-i,x))
        elif board[y,x][1] != board[y-i,x][1]:
            possible_positions.append((y-i,x))
            break
        else:
            break
    
    #Gauche
    for i in range(1, len(board)-x):
        if board[y,x+i] == '':
            possible_positions.append((y,x+i))
        elif board[y,x][1] != board[y,x+i][1]:
            possible_positions.append((y,x+i))
            break
        else:
            break

    ## Diagonale
    #Direction en haut a gauche
    for i in range(1,min(len(board)-y,len(board[0])-x)):
        if board[y+i][x+i] == '':
            possible_positions.append((y+i,x+i))
        elif board[y+i][x+i][1] != board[y][x][1]:
            possible_positions.append((y+i,x+i))
            break
        else:
            break


    #Direction en haut a droite
    for i in range(1,min(len(board)-y,x+1)):
        if board[y+i][x-i] == '':
            possible_positions.append((y+i,x-i))
        elif board[y+i][x-i][1] != board[y][x][1]:
            possible_positions.append((y+i,x-i))
            break
        else:
            break

    #Direction en bas a gauche
    for i in range(1,min(y+1,len(board[0])-x)):
        if board[y-i][x+i] == '':
            possible_positions.append((y-i,x+i))
        elif board[y-i][x+i][1] != board[y][x][1]:
            possible_positions.append((y-i,x+i))
            break
        else:
            break

    #Direction en bas a droite
    for i in range(1,min(y+1,x+1)):
        if board[y-i][x-i] == '':
            possible_positions.append((y-i,x-i))
        elif board[y-i][x-i][1] != board[y][x][1]:
            possible_positions.append((y-i,x-i))
            break
        else:
            break

    return possible_positions

def get_move_knight(y,x,board):
    possible_positions = []

    # en haut a gauche
    posy = y + 1
    posx = x + 2
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    posy = y + 2
    posx = x + 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en haut a droite
    posy = y - 1
    posx = x + 2
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))
    
    posy = y + 2
    posx = x - 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en bas a gauche
    posy = y - 2
    posx = x + 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    posy = y + 1    
    posx = x - 2
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    # en bas a droite
    posy = y - 1
    posx = x - 2
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))

    posy = y - 2
    posx = x - 1
    if posx < len(board[0]) and posy < len(board) and posx > 0 and posy > 0:
        if board[posy][posx] == '':
            possible_positions.append((posy,posx))
        elif board[posy][posx][1] != board[y][x][1]:
            possible_positions.append((posy,posx))


    return possible_positions

def get_move_bishop(y,x,board):
    possible_positions = []

    #Direction en haut a gauche
    for i in range(1,min(len(board)-y,len(board[0])-x)):
        if board[y+i][x+i] == '':
            possible_positions.append((y+i,x+i))
        elif board[y+i][x+i][1] != board[y][x][1]:
            possible_positions.append((y+i,x+i))
            break
        else:
            break


    #Direction en haut a droite
    for i in range(1,min(len(board)-y,x+1)):
        if board[y+i][x-i] == '':
            possible_positions.append((y+i,x-i))
        elif board[y+i][x-i][1] != board[y][x][1]:
            possible_positions.append((y+i,x-i))
            break
        else:
            break

    #Direction en bas a gauche
    for i in range(1,min(y+1,len(board[0])-x)):
        if board[y-i][x+i] == '':
            possible_positions.append((y-i,x+i))
        elif board[y-i][x+i][1] != board[y][x][1]:
            possible_positions.append((y-i,x+i))
            break
        else:
            break

    #Direction en bas a droite
    for i in range(1,min(y+1,x+1)):
        if board[y-i][x-i] == '':
            possible_positions.append((y-i,x-i))
        elif board[y-i][x-i][1] != board[y][x][1]:
            possible_positions.append((y-i,x-i))
            break
        else:
            break
        
    return possible_positions

def get_move_rook(y,x,board):
    possible_positions = []

    #Haut
    for i in range(1, len(board)-y):
        if board[y+i,x] == '':
            possible_positions.append((y+i,x))
        elif board[y,x][1] != board[y+i,x][1]:
            possible_positions.append((y+i,x))
            break
        else:
            break
    
    #Droite
    for i in range(1, x+1):
        if board[y,x-i] == '':
            possible_positions.append((y,x-i))
        elif board[y,x][1] != board[y,x-i][1]:
            possible_positions.append((y,x-i))
            break
        else:
            break
    
    #Bas
    for i in range(1, y+1):
        if board[y-i,x] == '':
            possible_positions.append((y-i,x))
        elif board[y,x][1] != board[y-i,x][1]:
            possible_positions.append((y-i,x))
            break
        else:
            break
    
    #Gauche
    for i in range(1, len(board)-x):
        if board[y,x+i] == '':
            possible_positions.append((y,x+i))
        elif board[y,x][1] != board[y,x+i][1]:
            possible_positions.append((y,x+i))
            break
        else:
            break

    return possible_positions

def get_move_pawn(y,x,board):
    possible_positions = []

    try:
        if board[y+1][x] == '':
            possible_positions.append((y+1,x))
    except:
        pass

    try:
        if board[y+1][x+1] != '' and board[y+1][x+1][1] != board[y][x][1]:
            possible_positions.append((y+1,x+1))
    except:
        pass

    try:
        if board[y+1][x-1] != '' and board[y+1][x-1][1] != board[y][x][1]:
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
                if board[i][j][1] == current_player:
                    match board[i][j][0]:
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
    return current_best_move
    
    while True:
        if (time.time() - start_time >= time_budget - 0.1):
            return current_best_move
        
register_chess_bot("RodFav_Random", chess_bot)
king = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]

queen = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]

rook = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1)
]

bishop = [
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]

knight = [
    (2,1),
    (2,-1),
    (-2,1),
    (-2,-1),
    (1,2),
    (-1,2),
    (1,-2),
    (-1,-2)
]

pawn = [
    (1,0),
    (1,1),
    (1,-1)
]


piece_list = {
    "k": king,
    "q": queen,
    "r": rook,
    "b": bishop,
    "n": knight,
    "p": pawn
}

def move_piece(y, x, board):
    piece = board[y][x][0]
    color = board[y][x][1]

    directions = piece_list[piece]

    moves = []
    eat = []

    if piece == 'n':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                if board[posy][posx] == "":
                    moves.append((posy, posx))

                elif board[posy][posx][1] != color:
                    eat.append((posy, posx))

        return moves, eat

    if piece == 'p':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                if dx == 0 and board[posy][posx] == "":
                    moves.append((posy, posx))
                elif dx != 0 and board[posy][posx] != "" and board[posy][posx][1] != color:
                    eat.append((posy, posx))
                
        return moves, eat

    if piece == 'k':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            if posy >= 0 and posy < 8 and posx >= 0 and posx < 8:

                if board[posy][posx] == "":
                    moves.append((posy, posx))
                elif board[posy][posx][1] != color:
                    eat.append((posy, posx))

        return moves, eat
    

    if piece in ['r','b','q']:
        for dy, dx in directions:
            posy, posx = y, x
            while True:
                posy += dy
                posx += dx

                if posy < 0 or posy >= 8 or posx < 0 or posx >= 8:
                    break 

                if board[posy][posx] == "":
                    moves.append((posy, posx))
                else:
                    if board[posy][posx][1] != color:
                        eat.append((posy, posx))
                    break

        return moves, eat
    
    return moves, eat



def all_move_piece(y, x, board):
    piece = board[y][x][0]
    color = board[y][x][1]

    directions = piece_list[piece]

    moves = []

    if piece == 'n':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                if board[posy][posx] == "":
                    moves.append((posy, posx))

                elif board[posy][posx][1] != color:
                    moves.append((posy, posx))

        return moves

    if piece == 'p':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                if dx == 0 and board[posy][posx] == "":
                    moves.append((posy, posx))
                elif dx != 0 and board[posy][posx] != "" and board[posy][posx][1] != color:
                    moves.append((posy, posx))
                
        return moves

    if piece == 'k':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            if posy >= 0 and posy < 8 and posx >= 0 and posx < 8:

                if board[posy][posx] == "":
                    moves.append((posy, posx))
                elif board[posy][posx][1] != color:
                    moves.append((posy, posx))

        return moves
    

    if piece in ['r','b','q']:
        for dy, dx in directions:
            posy, posx = y, x
            while True:
                posy += dy
                posx += dx

                if posy < 0 or posy >= 8 or posx < 0 or posx >= 8:
                    break 

                if board[posy][posx] == "":
                    moves.append((posy, posx))
                else:
                    if board[posy][posx][1] != color:
                        moves.append((posy, posx))
                    break

        return moves
    
    return moves
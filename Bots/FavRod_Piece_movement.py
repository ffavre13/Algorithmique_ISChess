#Movement for the king
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

#Movement for the queen
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

#Movement for the rook
rook = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1)
]

#Movement for the bishop
bishop = [
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]

#Movement for the knight
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

#Movement for the pawn
pawn = [
    (1,0),
    (1,1),
    (1,-1)
]

#Link piece movement with the correct piece
piece_list = {
    "k": king,
    "q": queen,
    "r": rook,
    "b": bishop,
    "n": knight,
    "p": pawn
}

def move_piece(y, x, board):
    """
    Function to get all the legal move for a piece and
    all move a piece can eat an other
    
    :param y: Get the y position of the chess board
    :param x: Get the x position of the chess board
    :param board: Chess board
    :return: Tuple moves: All move without enemy piece
    :return: Tuple eat: All move with enemy team
    """

    #Piece type
    piece = board[y][x][0]

    #Color of the piece
    color = board[y][x][1]

    #Direction of the piece
    directions = piece_list[piece]

    moves = []
    eat = []

    #Knight
    if piece == 'n':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            #Check the limit of the chess board
            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif board[posy][posx][1] != color:
                    eat.append((posy, posx))

        return moves, eat

    #Pawn
    if piece == 'p':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            #Check the limit of the chess board
            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:
                
                #Check if the position is free
                if dx == 0 and board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif dx != 0 and board[posy][posx] != "" and board[posy][posx][1] != color:
                    eat.append((posy, posx))
                
        return moves, eat

    #King
    if piece == 'k':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            #Check the limit of the chess board
            if posy >= 0 and posy < 8 and posx >= 0 and posx < 8:

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif board[posy][posx][1] != color:
                    eat.append((posy, posx))

        return moves, eat
    
    #Rook, bishop and queen
    if piece in ['r','b','q']:
        for dy, dx in directions:
            posy, posx = y, x
            while True:
                posy += dy
                posx += dx
                
                #Check the limit of the chess board
                if posy < 0 or posy >= 8 or posx < 0 or posx >= 8:
                    break 

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))
                else:
                    #Check if the position has an enemy piece
                    if board[posy][posx][1] != color:
                        eat.append((posy, posx))
                    break

        return moves, eat
    
    return moves, eat


def all_move_piece_reverse(y, x, board):
    """
    Function to get all possible moves for a piece for the reverse direction
    
    :param y: Get the y position of the chess board
    :param x: Get the x position of the chess board
    :param board: Chess board
    :return: Tuple moves: All legals moves for all pieces
    """

    #Piece type
    piece = board[y][x][0]

    #Piece color
    color = board[y][x][1]

    #Direction of the piece
    directions = piece_list[piece]

    moves = []

    #Knight
    if piece == 'n':
        for dy, dx in directions:
            posy = y - dy
            posx = x + dx

            #Check the limit of the chess board
            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:
                
                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif board[posy][posx][1] != color:
                    moves.append((posy, posx))

        return moves

    #Pawn
    if piece == 'p':
        for dy, dx in directions:
            posy = y - dy
            posx = x + dx

            #Check the limit of the chess board
            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:
                
                #Check if the position is free
                if dx == 0 and board[posy][posx] == "":
                    moves.append((posy, posx))
                    
                #Check if the position has an enemy piece
                elif dx != 0 and board[posy][posx] != "" and board[posy][posx][1] != color:
                    moves.append((posy, posx))
                
        return moves

    #King
    if piece == 'k':
        for dy, dx in directions:
            posy = y - dy
            posx = x + dx

            #Check the limit of the chess board
            if posy >= 0 and posy < 8 and posx >= 0 and posx < 8:

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif board[posy][posx][1] != color:
                    moves.append((posy, posx))

        return moves
    
    #Rook, bishop and queen
    if piece in ['r','b','q']:
        for dy, dx in directions:
            posy, posx = y, x
            while True:
                posy -= dy
                posx += dx

                #Check the limit of the chess board
                if posy < 0 or posy >= 8 or posx < 0 or posx >= 8:
                    break 
                
                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))
                else:
                    #Check if the position has an enemy piece
                    if board[posy][posx][1] != color:
                        moves.append((posy, posx))
                    break

        return moves
    
    return moves

def all_move_piece(y, x, board):
    """
    Function to get all possible moves for a piece
    
    :param y: Get the y position of the chess board
    :param x: Get the x position of the chess board
    :param board: Chess board
    :return: Tuple moves: All legals moves for all pieces
    """

    #Piece type
    piece = board[y][x][0]

    #Piece color
    color = board[y][x][1]

    #Piece direction
    directions = piece_list[piece]

    moves = []

    #Knight
    if piece == 'n':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            #Check the limit of the chess board
            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif board[posy][posx][1] != color:
                    moves.append((posy, posx))

        return moves

    #Pawn
    if piece == 'p':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            #Check the limit of the chess board
            if posx < len(board[0]) and posy < len(board) and posx >= 0 and posy >= 0:

                #Check if the position is free
                if dx == 0 and board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif dx != 0 and board[posy][posx] != "" and board[posy][posx][1] != color:
                    moves.append((posy, posx))
                
        return moves

    #King
    if piece == 'k':
        for dy, dx in directions:
            posy = y + dy
            posx = x + dx

            #Check the limit of the chess board
            if posy >= 0 and posy < 8 and posx >= 0 and posx < 8:

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))

                #Check if the position has an enemy piece
                elif board[posy][posx][1] != color:
                    moves.append((posy, posx))

        return moves
    
    #Rook, bishop and queen
    if piece in ['r','b','q']:
        for dy, dx in directions:
            posy, posx = y, x
            while True:
                posy += dy
                posx += dx

                #Check the limit of the chess board
                if posy < 0 or posy >= 8 or posx < 0 or posx >= 8:
                    break 

                #Check if the position is free
                if board[posy][posx] == "":
                    moves.append((posy, posx))
                else:
                    #Check if the position has an enemy piece
                    if board[posy][posx][1] != color:
                        moves.append((posy, posx))
                    break

        return moves
    
    return moves
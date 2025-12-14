import sys, os

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Bots import *

class BoardManager:
    BOARD_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "Data", "maps")
    DEFAULT_BOARD = os.path.join(BOARD_DIRECTORY, "default.brd")

    def __init__(self):
        self.board: np.array = np.array([], dtype='O')
        self.player_order: str = "0w01b2"
        self.load_file(self.DEFAULT_BOARD)

    def load_file(self, path: str) -> bool:
        if not os.path.exists(path):
            print(f"File '{path}' not found")
            return False

        with open(path, "r") as f:
            data = f.read()

        lines = data.split("\n")
        self.player_order = lines[0]
        rows = [line.replace('--', '').strip().split(",") for line in lines[1:]]
        self.board = np.array(rows, dtype='O')
        return True

    @staticmethod
    def print_board(board):
        for row in board:
            print(" | ".join([c if c else "  " for c in row]))
        print("\n" + "-"*30 + "\n")

def play_game(player1, player2, board_manager, max_rounds=10):
    board = np.copy(board_manager.board)
    for round_num in range(max_rounds):
            # BoardManager.print_board(board)
            
            move1 = player1("0w0", board, 1)

            if board[move1[1][0]][move1[1][1]] == 'kb':
                return 'player1_wins'
            
            if move1[1][0] == 7 and board[move1[0][0]][move1[0][1]] == 'pw':
                board[move1[1][0]][move1[1][1]] = 'qw'
                board[move1[0][0]][move1[0][1]] = ''
            else:
                board[move1[1][0]][move1[1][1]] = board[move1[0][0]][move1[0][1]]
                board[move1[0][0]][move1[0][1]] = ''

            board = np.rot90(board, 2)
            move2 = player2("0b0", board, 1)

            
            if board[move2[1][0]][move2[1][1]]  == 'kw':
                return 'player2_wins'
            
            if move2[1][0] == 7 and board[move2[0][0]][move2[0][1]] == 'pb':
                board[move2[1][0]][move2[1][1]] = 'qb'
                board[move2[0][0]][move2[0][1]] = ''
            else:
                board[move2[1][0]][move2[1][1]] = board[move2[0][0]][move2[0][1]]
                board[move2[0][0]][move2[0][1]] = ''
            board = np.rot90(board, 2)
        
    return 'draws'

def main():
    all_bots = []
    print("===== Please choose the fist player (Don't select ManualMover) =====")
    for i,bot in enumerate(ChessBotList.CHESS_BOT_LIST):
        print(str(i) + ") " + str(bot))
        all_bots.append(ChessBotList.CHESS_BOT_LIST[bot])

    player1 = all_bots[int(input("First player: "))]
    player2 = all_bots[int(input("Second player: "))]
    max_nb_round = int(input("Enter the maximum number of round per game: "))
    nb_games =  int(input("Enter the number of game to play: "))

    results = {
        'player1_wins': 0,
        'player2_wins': 0,
        'draws': 0
    }

    board_manager = BoardManager()


    for game_num in range(nb_games):
        # print(f"{'='*60}\n")
        # print(f"Game {game_num + 1}/{nb_games}")
        # print(f"{'='*60}\n")
        current_result = play_game(player1, player2, board_manager, max_nb_round)
        results[current_result] += 1

    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"player1 (White): {results['player1_wins']} wins")
    print(f"player2 (Black): {results['player2_wins']} wins")
    print(f"Draws: {results['draws']}")
    print(f"Total games: {nb_games}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
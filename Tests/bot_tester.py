import sys, os
import numpy as np
import matplotlib.pyplot as plt
import csv
import time

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

def play_game(player1, player2, board_manager, max_rounds=10, reflection_time=1):
    board = np.copy(board_manager.board)
    result = [0,0,0,0] # player1_win, player2_win, draws, nb_round
    time_player1 = []
    time_player2 = []
    for round_num in range(max_rounds):

            result[3] += 1
            start_time = time.time()

            move1 = player1("0w0", board, reflection_time)
            
            time_player1.append(time.time()-start_time)

            if board[move1[1][0]][move1[1][1]] == 'kb':
                result[0] += 1
                return result, time_player1, time_player2
            
            if move1[1][0] == 7 and board[move1[0][0]][move1[0][1]] == 'pw':
                board[move1[1][0]][move1[1][1]] = 'qw'
                board[move1[0][0]][move1[0][1]] = ''
            else:
                board[move1[1][0]][move1[1][1]] = board[move1[0][0]][move1[0][1]]
                board[move1[0][0]][move1[0][1]] = ''

            board = np.rot90(board, 2)

            start_time = time.time()

            move2 = player2("0b0", board, reflection_time)

            time_player2.append(time.time()-start_time)
            
            if board[move2[1][0]][move2[1][1]]  == 'kw':
                result[1] += 1
                return result, time_player1, time_player2
            
            if move2[1][0] == 7 and board[move2[0][0]][move2[0][1]] == 'pb':
                board[move2[1][0]][move2[1][1]] = 'qb'
                board[move2[0][0]][move2[0][1]] = ''
            else:
                board[move2[1][0]][move2[1][1]] = board[move2[0][0]][move2[0][1]]
                board[move2[0][0]][move2[0][1]] = ''
            board = np.rot90(board, 2)
        
    result[2] += 1
    return result, time_player1, time_player2

def main():
    all_bots = []
    all_bots_name = []
    all_results = []
    print("===== Please choose the first player (Don't select ManualMover) =====")
    for i,bot in enumerate(ChessBotList.CHESS_BOT_LIST):
        print(str(i) + ") " + str(bot))
        all_bots_name.append(str(bot))
        all_bots.append(ChessBotList.CHESS_BOT_LIST[bot])


    player1_id = int(input("First player: "))
    player2_id = int(input("Second player: "))
    player1 = all_bots[player1_id]
    player2 = all_bots[player2_id]
    max_nb_round = int(input("Enter the maximum number of round per game: "))
    nb_games =  int(input("Enter the number of game to play: "))
    reflection_time = int(input("Enter the reflection time: "))

    number = int(time.time())

    results = {
        'player1_wins': 0,
        'player2_wins': 0,
        'draws': 0
    }

    time_player1 = []
    time_player2 = []

    board_manager = BoardManager()

    with open(f"Tests/data/{all_bots_name[player1_id]}_vs_{str(all_bots_name[player2_id])}_{number}.csv", 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['game_number','player1_win','player2_win','draw','nb_round'])

    for game_num in range(nb_games):
        current_result, current_time_player1, current_time_player2 = play_game(player1, player2, board_manager, max_nb_round, reflection_time)
        results['player1_wins'] += current_result[0]
        results['player2_wins'] += current_result[1]
        results['draws'] += current_result[2]

        for e in current_time_player1:
            time_player1.append(e)

        for e in current_time_player2:
            time_player2.append(e)

        with open(f"Tests/data/{all_bots_name[player1_id]}_vs_{str(all_bots_name[player2_id])}_{number}.csv", 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';')
            filewriter.writerow([game_num+1]+current_result)

        all_results.append([game_num+1]+current_result)

    print(f"{'='*60}")
    print(f"player1 (White): {results['player1_wins']} wins")
    print(f"player2 (Black): {results['player2_wins']} wins")
    print(f"Draws: {results['draws']}")
    print(f"Total games: {nb_games}")
    print(f"Average time for player1 (White) to play a move: {sum(time_player1)/len(time_player1)}, max: {max(time_player1)}, min: {min(time_player1)}")
    print(f"Average time for player2 (Black) to play a move: {sum(time_player2)/len(time_player2)}, max: {max(time_player2)}, min: {min(time_player2)}")
    print(f"{'='*60}")

    plt.bar([f"{all_bots_name[player1_id]}",f"{str(all_bots_name[player2_id])}",'draws'],[results['player1_wins'],results['player2_wins'],results['draws']])
    plt.ylabel("Number of wins")
    plt.title(f"{all_bots_name[player1_id]} vs {str(all_bots_name[player2_id])} - number of wins")
    plt.savefig(f"Tests/data/barplot_{all_bots_name[player1_id]}_vs_{str(all_bots_name[player2_id])}_{number}.svg", format="svg")
    plt.close()

    values = [e[4] for e in all_results]
    plt.hist(values,bins=range(min(values), max(values) + 2))
    plt.xlabel("Number of moves to finish the game")
    plt.ylabel("Number of games")
    plt.title(f"{all_bots_name[player1_id]} vs {str(all_bots_name[player2_id])} - move per game")
    plt.savefig(f"Tests/data/histogram_{all_bots_name[player1_id]}_vs_{str(all_bots_name[player2_id])}_{number}.svg", format="svg")
    plt.close()

if __name__ == "__main__":
    main()
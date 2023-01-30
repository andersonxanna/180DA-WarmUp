# game code for multiplayer rps
# Andrew Fantino
import random

class RockPaperScissors():

    def __init__(self):
        self.player1_move = 0
        self.player2_move = 0

    def get_game_state(self) -> str:
        p1_winstr = 'win lose'
        p2_winstr = 'lose win'

        ret_str = 'tie tie'

        if self.player1_move == 'r' and self.player2_move != 'r':
            ret_str = p1_winstr if self.player2_move == 's' else p2_winstr

        elif self.player1_move == 'p' and self.player2_move != 'p':
            ret_str = p1_winstr if self.player2_move == 'r' else p2_winstr

        elif self.player1_move == 's' and self.player2_move != 's':
            ret_str = p1_winstr if self.player2_move == 'p' else p2_winstr

        return ret_str

    def set_move(self, player_num, move):
        if player_num == 1:
            print('player1 set')
            self.player1_move = move
        elif player_num == 2:
            print('player2 set')
            self.player2_move = move
        else:
            print(f'ERROR: {player_num} is invalid')

    def get_start_message(self):
        return 'Enter r/p/s for Rock, Paper, Scissors respectively'

'''
    def play(self):
        state = self.game_state(self.player_move, self.player2_move)
        if state == 'win':
            print('You win!')
            num_player_wins += 1
        elif state == 'tie':
            print('You tie')
            num_ties += 1
        else:
            print('You lose')
            num_ai_wins += 1
'''
"""
Anna Anderson
UID: 105296576
180DA: Command line rock paper scissors (week 3)
"""
import random
char_map = {'r': 0, 'p':1, 's':2}
int_map = {0:'r', 1:'p', 2:'s'}
rounds = 0
ties = 0
player_score = 0
print('Get ready to play rock, paper, scissors!')
print('Press q to quit')
print('\n')

# r > s, s > p,  p > r
while(True):
    inp = input('Play r, p, or s: ')
    if inp == 'q':
        bot_score = rounds - player_score - ties
        print('Your score: ', player_score)   
        print('Bot score: ', bot_score)  
        if player_score > bot_score:
            print('You win')
        elif player_score < bot_score:
            print('You lose!')
        else:
            print('Tie game!')
        break
    rounds += 1
    print('Round ', rounds)
    print('You input: ', inp)
    player_val = char_map[inp]
    bot_val = random.randint(0, 2)
    print('Bot input: ', int_map[bot_val])
    if abs(bot_val - player_val) == 1:
        winner = max(player_val, bot_val)
    elif abs(bot_val - player_val) == 2:
        winner = min(player_val, bot_val) # btwn rock and scissors
    else:
        winner = 4
    if winner == 4:
        print("Tie!")
        ties += 1
    elif winner == player_val:
        player_score += 1
        print("You win!")
    else:
        print("Bot wins!")
    print('\n')
# Simple pygame program
"""
Referenced:
    https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    https://www.geeksforgeeks.org/python-display-images-with-pygame/
"""

# Import and initialize the pygame library
import pygame
import random
import time
pygame.init()

# Set up the drawing window
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Color values
green = (0, 255, 0)
blue = (0, 0, 128)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Images and image size
rock_img = pygame.image.load("rock.png").convert()
paper_img = pygame.image.load("paper.png").convert()
sciss_img = pygame.image.load("scissors.png").convert()
game_img = pygame.image.load("gameover.png").convert()
DEFAULT_IMAGE_SIZE = (100, 100)
  
# Scale the image to your needed size
rock_img = pygame.transform.scale(rock_img, DEFAULT_IMAGE_SIZE)
paper_img = pygame.transform.scale(paper_img, DEFAULT_IMAGE_SIZE)
sciss_img = pygame.transform.scale(sciss_img, DEFAULT_IMAGE_SIZE)
game_img = pygame.transform.scale(game_img, DEFAULT_IMAGE_SIZE)
imgs = [rock_img, paper_img, sciss_img]
DEFAULT_IMAGE_POSITION = (200,300)
DEFAULT_BOT_POSITION = (600,300)

# Set text
pygame.display.set_caption('Show Text')
font=pygame.font.SysFont('freesansbold.ttf',  20)
text = font.render('Enter r, p, or s', True, blue, (255,255,255))
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
# set the center of the rectangular object.
textRect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2 + SCREEN_HEIGHT//4))

running = True

# Game Values:
char_map = {'r': 0, 'p':1, 's':2}
int_map = {0:'r', 1:'p', 2:'s'}
rounds = 0
ties = 0
player_score = 0
started = False

#Change the text and images on the screen
def change_text(text, textRect, pygame, img, img2):
    screen.blit(img, DEFAULT_IMAGE_POSITION)
    screen.blit(img2, DEFAULT_BOT_POSITION)
    screen.blit(text, textRect)
    pygame.display.flip()

while running:
    # Fill screen with white
    screen.fill((255, 255, 255))
    
    # If the player has not made a move yet, display should be white
    if not started:
        screen.blit(text, textRect)
        pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            started = True
            if event.key == pygame.K_r:
                print("Player input r")
                inp = 'r'
            if event.key == pygame.K_p:
                print("Player input p")
                inp = 'p'
            if event.key == pygame.K_s:
                print("Player input s")
                inp = 's'
            if event.key == pygame.K_q:
                bot_score = rounds - player_score - ties
                print('Your score: ', player_score)   
                print('Bot score: ', bot_score)  
                if player_score > bot_score:
                    text = font.render('You win! Game over! || Player Score {}  || Bot Score {}'.format(player_score, bot_score), True, blue, (255,255,255))
                elif player_score < bot_score:
                    text = font.render('You lose! Game over! || Player Score {} || Bot Score {}'.format(player_score, bot_score), True, blue, (255,255,255))
                else:
                    text = font.render('Tie game! Game over! || Player Score {} || Bot Score {}'.format(player_score, bot_score), True, blue, (255,255,255))
                change_text(text, textRect, pygame, game_img, game_img)
                time.sleep(5.0)
                running = False
            rounds += 1
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
                text = font.render('YOU <-- Tie! Play again! --> BOT', True, blue, (255,255,255))
                ties += 1
            elif winner == player_val:
                player_score += 1
                text = font.render('YOU <-- You win! Play again! --> BOT', True, blue, (255,255,255))
            else:
                text = font.render('YOU <-- You win! Play again! --> BOT', True, blue, (255,255,255))
            change_text(text, textRect, pygame, imgs[char_map[inp]], imgs[bot_val])
            print('\n')

# Done! Time to quit.
pygame.quit()
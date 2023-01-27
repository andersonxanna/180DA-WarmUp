# Simple pygame program
"""
Referenced:
    https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    
"""

# Import and initialize the pygame library
import pygame
pygame.init()

char_map = {'r': 0, 'p':1, 's':2}
int_map = {0:'r', 1:'p', 2:'s'}
rounds = 0
ties = 0
player_score = 0

# Set up the drawing window
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
rock_img = pygame.image.load("rock.png").convert()
paper_img = pygame.image.load("paper.png").convert()
sciss_img = pygame.image.load("scissors.png").convert()
# Run until the user asks to quit

pygame.display.set_caption('Show Text')

Font=pygame.font.SysFont('timesnewroman',  30)

running = True
while running:
    # Did the user click the window close button?
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
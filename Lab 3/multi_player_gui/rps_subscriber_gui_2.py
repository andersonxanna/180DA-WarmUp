# 3 round rps
import paho.mqtt.client as mqtt
import time

import pygame
pygame.init() # init pygame

"""
GUI SETUP **********************************************
"""
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
box_img = pygame.image.load("box.png").convert()
DEFAULT_IMAGE_SIZE = (100, 100)
  
# Scale the image to your needed size
rock_img = pygame.transform.scale(rock_img, DEFAULT_IMAGE_SIZE)
paper_img = pygame.transform.scale(paper_img, DEFAULT_IMAGE_SIZE)
sciss_img = pygame.transform.scale(sciss_img, DEFAULT_IMAGE_SIZE)
box_img = pygame.transform.scale(box_img, DEFAULT_IMAGE_SIZE)
imgs = [rock_img, paper_img, sciss_img]
DEFAULT_IMAGE_POSITION = (200,300)
DEFAULT_BOT_POSITION = (600,300)

# Set text
pygame.display.set_caption('Show Text')
font=pygame.font.SysFont('freesansbold.ttf',  20)
text = font.render('Input r, p, or s, wait for other player to play', True, blue, (255,255,255))
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
# set the center of the rectangular object.
textRect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2 + SCREEN_HEIGHT//4))

running = True
"""
GUI SETUP **********************************************
"""

# used code that the professor/TA posted, modified to be a player in rps
player_num = 2
ROUND_START = "b'8"
RPS_RESULT = "b'0"
"""
Game values for GUI:
    result, p1 move, p2 move
"""
global result #bool to indicate that a result was made
global result_char
global p1 #bool to indicate that p1 made a move
global p1_move
global p2 #bool to indicate that p2 made a move
global p2_move
global started
started = False # have you started the game yet?
result = False
p1 = False
p2 = False
result_char = '' 
p1_move = ''
p2_move = ''
# Game Values:
char_map = {'r': 0, 'p':1, 's':2}
int_map = {0:'r', 1:'p', 2:'s'}

#Change the text and images on the screen
def change_text(text, textRect, pygame, img, img2):
    screen.blit(img, DEFAULT_IMAGE_POSITION)
    screen.blit(img2, DEFAULT_BOT_POSITION)
    screen.blit(text, textRect)
    pygame.display.flip()

# callback definitions
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180/team1/rps", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
# The default message callback.
def on_message(client, userdata, message):
    global result, p1, p2, result_char, p1_move, p2_move, started #use globals
    if str(message.payload)[0:3] == "b'1":
        print("PLAYER 1", str(message.payload))
        p1 = True
        p1_move = str(message.payload)[3]
        #p2_move = p2_move_str[1]
    split_msg = str(message.payload).split()
    if ((split_msg[0]) == ROUND_START):
        started = True
        my_input = input('Choose r, p, or s, for Rock, Paper, or Scissors\n')
        p2_move = my_input
        my_input = str(player_num) + my_input
        client.publish("ece180/team1/rps", my_input, qos=1)
        print('Published message: ', my_input)
        p2 = True
        time.sleep(2)
    elif((split_msg[0]) == RPS_RESULT):
        print("Result: ", split_msg[player_num])

        result_char = split_msg[player_num]
        if (result_char == 'win\'') or (result_char == 'lose\''):
            print("Over")
            result = True

        time.sleep(2)

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

while running: # perhaps add a stopping condition using some break or something
    # Fill screen with white
    # client.loop_start()
    screen.fill((255, 255, 255))
    if not started:
        screen.blit(text, textRect)
        pygame.display.flip()
    else:
        if result:
            text = font.render('Other Player <-- Game over! You {} --> YOU'.format(result_char), True, blue, (255,255,255))
            change_text(text, textRect, pygame, imgs[char_map[p1_move]], imgs[char_map[p2_move]])
            result = False
        elif p1 and not p2:
            text = font.render('Other Player <-- Rock paper scissors --> YOU', True, blue, (255,255,255))
            change_text(text, textRect, pygame, imgs[char_map[p1_move]], box_img)
        elif p2 and not p1:
            text = font.render('Other Player <-- Rock paper scissors --> YOU', True, blue, (255,255,255))
            change_text(text, textRect, pygame, box_img, imgs[char_map[p2_move]])
        elif p2 and p1:
            p1 = False
            p2 = False
        else:
            pass #do nothing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pass # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.
# use publish() to publish messages to the broker.
# use disconnect() to disconnect from the broker.
pygame.quit()
client.loop_stop()
client.disconnect()
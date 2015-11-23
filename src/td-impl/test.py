import sys
from random import randrange
from ale_python_interface import ALEInterface
import numpy as np
from PIL import Image

def get_paddle_pos(screen):
    xStart = -1
    xEnd = -1
    for pos in range(8, 152):
        (r, g, b) = screen[189, pos]
        if (r == 200 and g == 72 and b == 72) or (r == 184 and g == 50 and b == 50):
            xStart = pos
            break
    for pos in range(xStart, 152):
        (r, g, b) = screen[189, pos]
        xEnd = pos
        if ~((r == 200 and g == 72 and b == 72) or (r == 184 and g == 50 and b == 50)):
            break

    paddleX = (xEnd + xStart)/2
    return (paddleX, 189)

def get_ball_pos(screen):
    ballX = -1
    ballY = -1

    for x in range(8, 151):
        for y in range(50, 189):
            (r, g, b) = screen[y, x]
            if(r == 184 and g == 50 and b == 50):
                ballX = x+1
                ballY = y+2
                break
    return (ballX, ballY)

def move_left(ale, legal_actions):
    return ale.act(legal_actions[4])
def move_right(ale, legal_actions):
    return ale.act(legal_actions[3])


ale = ALEInterface()


# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = False
if USE_SDL:
    if sys.platform == 'darwin':
        import pygame
        pygame.init()
        ale.setBool('sound', False) # Sound doesn't work on OSX
    elif sys.platform.startswith('linux'):
        ale.setBool('sound', True)
    ale.setBool('display_screen', True)

# Load the ROM file
ale.loadROM('breakout.bin')

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

screen_width, screen_height = ale.getScreenDims()

i = 0
noBall = 0

ale.act(legal_actions[1])
ale.act(legal_actions[1])

while not ale.game_over():
    screen = ale.getScreenRGB()

    ballX, ballY = get_ball_pos(screen)
    paddleX, paddleY = get_paddle_pos(screen)

    screen[ballY, ballX] = (255, 255, 255)
    screen[paddleY, paddleX] = (255, 255, 255)

    if (not (ballX == -1 or ballY == -1)):
        print str(ballX) + "," + str(ballY)
    if (not (paddleX == -1 or paddleY == -1)):
        print str(paddleX) + "," + str(paddleY)

    image = Image.fromarray(screen)
    image.save("images/" + str(i) + ".png", "png")
    i += 1

    if (noBall > 60):
        ale.act(legal_actions[1])
        noBall = 0
        continue

    if (ballX == -1 or ballY == -1):
        noBall += 1
        ale.act(legal_actions[0])
        continue
    else:
        noBall = 0

    if (paddleX >= 138):
        move_left(ale, legal_actions)
    elif (ballX - paddleX > 5):
        move_right(ale, legal_actions)
    elif (ballX - paddleX < -5):
        move_left(ale, legal_actions)
    else:
        ale.act(legal_actions[0])

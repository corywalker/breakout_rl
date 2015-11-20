import sys
from random import randrange
from ale_python_interface import ALEInterface
import numpy as np
from PIL import Image

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

#screen_height = 210
#screen_width = 160
while not ale.game_over():
    screen = ale.getScreenRGB()

    xStart = -1
    xEnd = -1
    for pos in range(8, 152):
        (r, g, b) = screen[189, pos]
        if (r == 200 and g == 72 and b == 72) or (r == 184 and g == 50 and b == 50):
            xStart = pos
            break
    for pos in range(xStart, 152):
        (r, g, b) = screen[189, pos]
        if ~((r == 200 and g == 72 and b == 72) or (r == 184 and g == 50 and b == 50)):
            xEnd = pos
            break
    paddle = (xEnd + xStart)/2
    screen[189, paddle] = (255, 255, 255)

    ballX = -1
    ballY = -1

    for x in range(8, 151):
        for y in range(50, 189):
            (r, g, b) = screen[y, x]
            if(r == 184 and g == 50 and b == 50):
                ballX = x+1
                ballY = y+2
                screen[ballY, ballX] = (255, 255, 255)
                break

    '''
    for x in range(screen_width):
        for y in range(screen_height):
            (r, g, b) = screen[y, x]
            if r == 200 and g == 72 and b == 72: # row 1
                screen[y, x] = (0, 0, 0)
            if r == 198 and g == 108 and b == 58: # row 2
                screen[y, x] = (0, 0, 0)
            if r == 180 and g == 122 and b == 48: # row 3
                screen[y, x] = (0, 0, 0)
            if r == 162 and g == 162 and b == 42: # row 4
                screen[y, x] = (0, 0, 0)
            if r == 72 and g == 160 and b == 72: # row 5
                screen[y, x] = (0, 0, 0)
            if r == 66 and g == 72 and b == 200: # row 6
                screen[y, x] = (0, 0, 0)
            if r == 66 and g == 158 and b == 130: # bottom left corner
                screen[y, x] = (0, 0, 0)
            (r, g, b) = screen[y, x]
            #if r == 184 and g == 50 and b == 50: # ball
            #    screen[y, x] = (0, 0, 0)
    '''

    image = Image.fromarray(screen)
    image.show()

    a = legal_actions[randrange(len(legal_actions))]
    reward = ale.act(a)
    #raw_input("Press Enter to continue...")

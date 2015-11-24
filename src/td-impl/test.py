import sys
from random import randrange
from ale_python_interface import ALEInterface
import numpy as np
from PIL import Image

class Game:
    def __init__(self, alpha, gamma, epsilon):
        # State values, intiialized arbitrarily
        self.value = np.random.rand(2, 8)

        # Hyperparameters
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # Initialize ALE
        self.ale = ALEInterface()

        self.ballX = self.ballY = -1
        self.paddleX = self.paddleY = -1

    # Run an episode
    def run_episode(self):
        self.ale.loadROM('breakout.bin')
        self.legal_actions = ale.getLegalActionSet()

        i = 0
        noBall = 0
        gameOver = False
        state = newstate = -1
        action = newaction = -1

        # Fire to start the game
        self.ale.act(legal_actions[1])
        self.ale.act(legal_actions[1])

        while not gameOver
            screen = ale.getScreenRGB()

            # Save image for examination
            image = Image.fromarray(screen)
            image.save("images/" + str(i) + ".png", "png")
            i += 1

            self.ballX, self.ballY = self.get_ball_pos(screen)
            self.paddleX, self.paddleY = self.get_paddle_pos(screen)

            # Color in screen for ball position
            screen[self.ballY, self.ballX] = (255, 255, 255)
            screen[self.paddleY, self.paddleX] = (255, 255, 255)

            newstate = get_state(self.ballX - self.paddleX)

            # Whoops, you died.
            if (noBall > 60):
                reward = -10
                newstate = 7
                self.ale.act(legal_actions[1])
                noBall = 0

                self.values[action][state] = self.values[action][state] + self.alpha * (reward + self.gamma * )

                if self.ale.game_over():
                    gameOver = True
                continue

            # Ignore this timestep; can't see ball.
            if (ballX == -1 or ballY == -1):
                noBall += 1
                ale.act(legal_actions[0])
                continue
            else:
                noBall = 0

            # Paddle is out of game area. Ignore timestep and readjust.
            if (paddleX >= 138):
                move_left(ale, legal_actions)

    def get_paddle_pos(self, screen):
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

        self.paddleX = (xEnd + xStart)/2
        self.paddleY = 189
        return (self.paddleX, 189)

    def get_ball_pos(self, screen):
        self.ballX = -1
        self.ballY = -1

        for x in range(8, 151):
            for y in range(50, 189):
                (r, g, b) = screen[y, x]
                if(r == 184 and g == 50 and b == 50):
                    self.ballX = x+1
                    self.ballY = y+2
                    break
        return (self.ballX, self.ballY)

    def move_left(self,):
        self.ale.act(self.legal_actions[4])
        return 0
    def move_right(self,):
        self.ale.act(self.legal_actions[3])
        return 1

    def get_state(self, dist):
        if dist < -7:
            return 0
        if dist in [-7, -6, -5]:
            return 1
        if dist in [-4, -3, -2]:
            return 2
        if dist in [-1, 0, 1]:
            return 3
        if dist in [2, 3, 4]:
            return 4
        if dist in [5, 6, 7]:
            return 5
        return 6

    def get_best_action(self, state):
        return max(self.values[0][state], self.values[1][state])

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return self.values[np.random.randint(2)][state]
        return get_best_action(state)

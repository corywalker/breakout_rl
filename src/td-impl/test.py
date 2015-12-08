import sys
from random import randrange
from ale_python_interface import ALEInterface
import numpy as np
from PIL import Image

class Game:
    def __init__(self, alpha, gamma, lambd, epsilon):
        # State-action values, intiialized arbitrarily
        self.values = np.random.rand(3, 3)

        # Hyperparameters
        self.alpha = alpha
        self.gamma = gamma
        self.lambd = lambd
        self.epsilon = epsilon

        # Initialize ALE
        self.ale = ALEInterface()
        self.ale.loadROM('breakout.bin')
        self.ale.setInt("random_seed", np.random.randint(32767))

        self.ballX = self.ballY = -1
        self.paddleX = self.paddleY = -1

        self.episode_num = 0

    # Run an episode
    def run_episode(self, record):
        self.gameScore = 0
        self.episode_num += 1
        self.legal_actions = self.ale.getLegalActionSet()
        eligibility = np.zeros((3, 3))

        i = 0
        noBall = 0
        gameOver = False
        state = newstate = -1
        action = newaction = -1

        # Fire to start the game
        self.gameScore += self.ale.act(self.legal_actions[1])
        self.gameScore += self.ale.act(self.legal_actions[1])

        while not gameOver:
            reward = 0
            screen = self.ale.getScreenRGB()

            if record:
                self.write_screen(screen, i)
            i += 1

            self.ballX, self.ballY = self.get_ball_pos(screen)
            self.paddleX, self.paddleY = self.get_paddle_pos(screen)

            # Color in screen for ball position
            screen[self.ballY, self.ballX] = (255, 255, 255)
            screen[self.paddleY, self.paddleX] = (255, 255, 255)

            newstate = self.get_state(self.ballX - self.paddleX)

            # Whoops, you died.
            if (noBall > 60):
                reward = -10
                newstate = state
                self.gameScore += self.ale.act(self.legal_actions[1])
                noBall = 0

                delta = reward + self.gamma * self.values[self.get_action(newstate)][newstate] - self.values[action][state]

                eligibility[action][state] += 1
                self.update_etrace(eligibility, state, action, delta)

                state = newstate = -1
                action = newaction = -1

                if self.ale.game_over():
                    gameOver = True
                continue

            # Ignore this timestep; can't see ball.
            if (self.ballX == -1 or self.ballY == -1):
                noBall += 1
                self.gameScore += self.ale.act(self.legal_actions[0])
                continue
            else:
                noBall = 0

            # Paddle is out of game area. Ignore timestep and readjust.
            if (self.paddleX >= 138):
                self.move_left()

            newaction = self.get_action(newstate)

            if state != -1:
                delta = reward + self.gamma * self.values[newaction][newstate] - self.values[action][state]
                eligibility[action][state] += 1
                self.update_etrace(eligibility, state, action, delta)

            if newaction == 0:
                self.move_left()
            elif newaction == 1:
                self.move_right()
            else:
                self.move_noop()

            state = newstate
            action = newaction
        self.ale.reset_game()
        return (i, self.gameScore)

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

        equalpix = np.equal(screen[50:189,8:151], np.array([184,50,50])).all(2)
        if equalpix.any():
            first = (equalpix.nonzero()+np.array([[50+2],[8+2]]))[:,0]
            self.ballY, self.ballX = first

        return (self.ballX, self.ballY)

    def move_left(self):
        self.gameScore += self.ale.act(self.legal_actions[4])
        return 0
    def move_right(self):
        self.gameScore += self.ale.act(self.legal_actions[3])
        return 1
    def move_noop(self):
        self.gameScore += self.ale.act(self.legal_actions[0])
        return 2

    def get_state(self, dist):
        if dist < -5:
            return 0
        if dist > 5:
            return 2
        return 1

    def get_best_action(self, state):
        maxValue = -1
        maxAct = 0
        for i in xrange(0, 3):
            if maxValue == -1 or self.values[i][state] > maxValue:
                maxValue = self.values[i][state]
                maxAct = i
        return maxAct

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(3)
        return self.get_best_action(state)

    def write_screen(self, screen, i):
        # Save image for examination
        image = Image.fromarray(screen)
        image.save("train_frameskip/e" + str(self.episode_num) + "_" + str(i) + ".png", "png")

    def sum_policy(self):
        for i in xrange(0, 3):
            if (self.get_best_action(i) == 0):
                print "left"
            elif (self.get_best_action(i) == 1):
                print "right"
            elif (self.get_best_action(i) == 2):
                print "noop"

    def update_etrace(self, eligibility, state, action, delta):
        for a in xrange(0, 3):
            for s in xrange(0, 3):
                self.values[a][s] += self.alpha * delta * eligibility[a][s]
                eligibility[a][s] *= self.gamma * self.lambd
 

alpha = 0.01
gamma = 0.9
lambd = 0.9
epsilon = 0.01

np.random.seed(0)
np.set_printoptions(precision=3)

for trials in xrange(0, 10):
    i = 50
    breakout = Game(alpha, gamma, lambd, epsilon)
    for j in xrange(0, i):
        print j
        print breakout.values
        print breakout.sum_policy()
        count, score = breakout.run_episode(False)
        print str(j) + " : " + str(count) + " timesteps, " + str(score) + " score"

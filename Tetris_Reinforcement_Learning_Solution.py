import pygame
import random
import time
from copy import deepcopy
import numpy as np
import math

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]
#Initializing Learning Parameters
NUM_BUCKETS = (5,5,5,5,5,5,5,5,5,5,7)
NUM_ACTIONS = 40
q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))

MIN_EXPLORE_RATE = 0.01 #Minimum exploration rate
MIN_LEARNING_RATE = 0.1 #Minimum learning rate


NUM_TRAIN_EPISODES = 1000 #Number of training episodes
NUM_TEST_EPISODES = 100 #Number of test episodes
    
class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # I Block
        [[4, 5, 9, 10], [2, 6, 5, 9]], #Z Block
        [[6, 7, 9, 10], [1, 5, 6, 10]], #S Block
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], #L Block
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #J Block
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], #T Block
        [[1, 2, 5, 6]], #O Block
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 200
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.swap = False
        self.next = Figure(3, 0)
        self.held_block = None

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
        
    def new_figure(self):
        self.figure= Figure(3, 0)

    def intersects(self): #Checks if the blocks are intersecting anything
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height): #Loop through height
            zeros = 0
            for j in range(self.width): #Loop through row
                if self.field[i][j] == 0: #If block in that position is empty
                    zeros += 1 #Assign empty
            if zeros == 0: #If there are no empty blocks in that row
                lines += 1 #Increment line
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j] #Shifts every block starting from i down 1 position (effectively removing that line)
        self.score += lines ** 2 #Increment Score

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self): #Stop the block as it has collided with another block and then generate a new block
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines() #After freezing we need to check if there are any horizontal lines to destroy
        
        #we swap the next block with the current block and generate a new block
        self.figure = self.next #Make next block the current block
        self.next = Figure(3,0) #Generate a new block and make it the next block
        self.swap = False #Allow the player to swap blocks
        if self.intersects(): #Check if the player has lost the game
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def hold_block(self): #Swap the blocks
        if self.swap == False:
            self.swap = True
            temp = self.held_block
            self.held_block = self.figure
            if temp!= None:
                self.figure = temp
                self.figure.x = 3
                self.figure.y = 0
            else:
                self.new_figure()



def get_state(field, figure):
    state_index = []
    for x in range(0,10): #loop through columns
        blockflag = False
        for y in range(0,20): #loop through to find the top-most block in that column (0 is the highest point and 19 is the lowest point)
            if field[y][x] != 0: #if there is a block there
                state_index.append(y%4) #we append the y coordinate of the block in that column
                blockflag = True #Block has been found so we set blockflag to false
                break #we break out of the loop so we don't append any more coordinates
        if blockflag == False: #If there's no block in that column we append 20 to represent no block being there
            state_index.append(4)

    #We then append the shape that we are about to place as that is part of the state
    state_index.append(figure.type)
    return tuple(state_index) #we return our state

def select_action(state, explore_rate): #For actions, the first digit is number of rotations, and the second digit is position. 0-4 is moving left, 5-9 is moving right
    if random.random() < explore_rate:
        action = random.randint(0,39) #if we get our explore rate we choose a random action
    else:
        action = np.argmax(q_table[state]) #if we do not get our explore rate we choose the highest QValue from the QTable
    return action

def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(1, 1.0 - math.log10((t+1)/25))) #Explore rate will increase as number of episodes increases

def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t+1)/25))) #Learning rate will increase as number of episodes increases


def train():
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)
    discount_factor = 0.99

    for episode in range(NUM_TRAIN_EPISODES):
        #Initialize our game
        done = False
        game = Tetris(20, 10)
        counter = 0
        time = 0
        while not done:
            time+=1
            reward = 0
            if game.figure is None:
                game.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            state_0 = get_state(game.field, game.figure)
            reward = 0
            action = select_action(state_0, explore_rate) #select action

            #now we execute the action
            rotation = (action//10)
            movement = (action%10)

            for count in range(0, rotation):
                game.rotate()
            if movement<5:
                game.go_side(-movement) #move left
            else:
                game.go_side(movement-5) #move right

            #We will make a copy of our game state so we can calculate the expected reward from this action
            predictgame = deepcopy(game)
            while not predictgame.intersects(): #We manually place the block down so we can clone it for later and make predictions
                predictgame.figure.y += 1
            predictgame.figure.y -= 1
            predictfigure = deepcopy(predictgame.figure)

            for i in range(4): #manually run the freeze method as we do not want to call the break_lines method
                for j in range(4):
                    if i * 4 + j in predictgame.figure.image():
                        predictgame.field[i + predictgame.figure.y][j + predictgame.figure.x] = predictgame.figure.color                    
    #Reward Calculation

        #Check for Underholes
            underhole = False
            #We first need to get our change in state
            underholecheck = deepcopy(predictgame.field)
            for i in range(0, len(underholecheck)):
               for j in range(0, len(underholecheck[i])):
                   underholecheck[i][j] = underholecheck[i][j] - game.field[i][j]

            #We then loop through our underhole check to find where the block we just placed is and use those coordinates to check if there is a block below
            for i in range(0, len(underholecheck)-1):
                for j in range(0, len(underholecheck[i])):
                    if underholecheck[i][j] != 0: #if a block is there
                        if predictgame.field[i+1][j] == 0: #if the block below it is empty
                            underhole = True

            if underhole == False:
                reward+=1000

        #Clear Rows
            lines = 0
            for i in range(1, predictgame.height): #Loop through height
                zeros = 0
                for j in range(predictgame.width): #Loop through row
                    if predictgame.field[i][j] == 0: #If block in that position is empty
                        zeros += 1 #Assign empty
                if zeros == 0: #If there are no empty blocks in that row
                    reward+= 200

        #Preventing a game over
            for i in range(1, predictgame.height):
                emptyrow = True
                for j in range(predictgame.width):
                    if predictgame.field[i][j] != 0:
                        emptyrow = False
                        
                if emptyrow == True:
                    reward-=i
                    break


    #Encourage building wide
            reward += predictgame.figure.y

            #Execute Action now that we have our reward
            game.go_space()

            if game.state == "gameover":
                reward -=10000
                
            state = get_state(game.field, game.figure) #get our new state

            best_q = np.amax(q_table[state]) #get the best q of the now current state
            q_table[state_0 + (action,)] += learning_rate*(reward + discount_factor*(best_q) - q_table[state_0 + (action,)]) #update the QValue for the previous state
            state_0 = state #prepare for the next timestep by setting our previous state to the current state

            if game.state == "gameover":
                break
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)
        print("Episode %d finished after %f time steps" % (episode, time))

    return q_table


def test(q_table):
    for episode in range(NUM_TEST_EPISODES):
        # Initialize the game engine
        pygame.init()

        # Define some colors
        WHITE = (0, 0, 0)
        BLACK = (255, 255, 255)
        GRAY = (128, 128, 128)

        size = (600, 500)
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Tetris")

        # Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()
        fps = 10
        game = Tetris(20, 10)
        counter = 0

        pressing_down = False
        while not done:
            reward = 0
            if game.figure is None:
                game.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            placeblockflag = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        placeblockflag = True
                    if event.key == pygame.K_ESCAPE:
                        game.__init__(20, 10)



            if placeblockflag == True:
                state_0 = get_state(game.field, game.figure)
                reward = 0
                action = select_action(state_0, 0) #select action

                #now we execute the action
                rotation = (action//10)
                movement = (action%10)

                for count in range(0, rotation):
                    game.rotate()
                if movement<5:
                    game.go_side(-movement) #move left
                else:
                    game.go_side(movement-5) #move right

                game.go_space()
         
            screen.fill(WHITE)

            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, colors[game.field[i][j]],
                                         [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(screen, colors[game.figure.color],
                                             [game.x + game.zoom * (j + game.figure.x) + 1,
                                              game.y + game.zoom * (i + game.figure.y) + 1,
                                              game.zoom - 2, game.zoom - 2])


            for i in range(4): #Held Block
                for j in range(4):
                    r = pygame.Rect(50+game.zoom * j, 150+game.zoom * i, game.zoom, game.zoom)
                    if game.held_block!= None:
                        p = i * 4 + j
                        if p in game.held_block.image():
                            pygame.draw.rect(screen, colors[game.held_block.color], r, 0)
                    pygame.draw.rect(screen, GRAY, r, 1)


            for i in range(4): #Next Block
                for j in range(4):
                    r = pygame.Rect(450+game.zoom *j, 150+game.zoom * i, game.zoom, game.zoom)
                    #check if that block is meant to be colored
                    p = i * 4 + j
                    if p in game.next.image():
                        pygame.draw.rect(screen, colors[game.next.color], r, 0)
                    pygame.draw.rect(screen, GRAY, r, 1)
                    
            font = pygame.font.SysFont('Calibri', 25, True, False)
            font1 = pygame.font.SysFont('Calibri', 65, True, False)
            text = font.render("Score: " + str(game.score), True, BLACK)
            text_game_over = font1.render("Game Over", True, (255, 125, 0))
            text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

            text_held = font.render("HELD:", True, BLACK)
            text_next = font.render("NEXT:", True, BLACK)

            screen.blit(text, [0, 10])
            screen.blit(text_held, [50,100])
            screen.blit(text_next, [450, 100])
            if game.state == "gameover":
                screen.blit(text_game_over, [20, 200])
                screen.blit(text_game_over1, [25, 265])

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()

def getresults():
    colors = [
        (0, 0, 0),
        (120, 37, 179),
        (100, 179, 179),
        (80, 34, 22),
        (80, 134, 22),
        (180, 34, 22),
        (180, 34, 122),
    ]

    q_table = train()

    MIN_EXPLORE_RATE = 0.01 #Minimum exploration rate
    MIN_LEARNING_RATE = 0.1 #Minimum learning rate


    NUM_TRAIN_EPISODES = 1000 #Number of training episodes
    NUM_TEST_EPISODES = 100 #Number of test episodes

    size = (600, 500)


    # Loop until the user clicks the close button.
    done = False
    fps = 10
    game = Tetris(20, 10)
    counter = 0

    pressing_down = False

    graphy = [0]
    while not done:
        reward = 0
        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0




        state_0 = get_state(game.field, game.figure)
        reward = 0
        action = select_action(state_0, 0) #select action

        #now we execute the action
        rotation = (action//10)
        movement = (action%10)

        for count in range(0, rotation):
            game.rotate()
        if movement<5:
            game.go_side(-movement) #move left
        else:
            game.go_side(movement-5) #move right

        game.go_space()
 

        if game.state == "gameover" or len(graphy) > 10000:
            break
    
        graphy.append(game.score)

    return graphy

if __name__=="__main__":
    colors = [
        (0, 0, 0),
        (120, 37, 179),
        (100, 179, 179),
        (80, 34, 22),
        (80, 134, 22),
        (180, 34, 22),
        (180, 34, 122),
    ]
    #Initializing Learning Parameters
    NUM_BUCKETS = (5,5,5,5,5,5,5,5,5,5,7)
    NUM_ACTIONS = 40
    q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))

    MIN_EXPLORE_RATE = 0.01 #Minimum exploration rate
    MIN_LEARNING_RATE = 0.1 #Minimum learning rate


    NUM_TRAIN_EPISODES = 1000 #Number of training episodes
    NUM_TEST_EPISODES = 100 #Number of test episodes


    q_table = train()
    test(q_table)



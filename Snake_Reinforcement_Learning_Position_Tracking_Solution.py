# importing libraries
import pygame
import time
import random
import numpy as np
import math


MIN_EXPLORE_RATE = 0.01
MIN_LEARNING_RATE = 0.1
window_x = 720
window_y = 480

#Reinforcement Learning Parameters
NUM_ACTIONS = int(4) #UP, DOWN, LEFT, RIGHT


NUM_BUCKETS = (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

q_table = np.zeros(tuple(NUM_BUCKETS) + (NUM_ACTIONS,))

MIN_EXPLORE_RATE = 0.01
MIN_LEARNING_RATE = 0.1

NUM_TRAIN_EPISODES = 500
NUM_TEST_EPISODES = 100


def select_action(state, explore_rate):
    if random.random() < explore_rate:
        action = random.randint(0,3)
    else:
        action = np.argmax(q_table[state])
    return action

def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(1, 1.0 - math.log10((t+1)/25))) #Explore rate will increase as number of episodes increases

def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t+1)/25))) #Learning rate will increase as number of episodes increases


def get_state(snake_body, fruit_position, direction):
    head = snake_body[0]
    state_index = []
    #Food is above the snake
    if fruit_position[1] > head[1]:
        state_index.append(1)
    else:
        state_index.append(0)

    #Food is to ther right of the snake
    if fruit_position[0] > head[0]:
        state_index.append(1)
    else:
        state_index.append(0)

    #Food is below the snake
    if fruit_position[1] < head[1]:
        state_index.append(1)
    else:
        state_index.append(0)

    #Food is to the left of the snake
    if fruit_position[0] < head[0]:
        state_index.append(1)
    else:
        state_index.append(0)

    #Hazard Directly above the snake
    for body in snake_body[1:]:
        if body[0] == head[0] and body[1] == head[1] + 10:
            state_index.append(1)
            break
    if len(state_index) == 4: #if no body part above the snake
        if head[1] == window_y-10:
            state_index.append(1)
        else:
            state_index.append(0)

    #Hazard directly to the right
    for body in snake_body[1:]:
        if body[1] == head[1] and body[0] == head[0] - 10:
            state_index.append(1)
            break
    if len(state_index) == 5: #if no body part to the right of the snake
        if head[0] == window_x-10:
            state_index.append(1)
        else:
            state_index.append(0)

    #Hazard directly below the snake
    for body in snake_body[1:]:
        if body[0] == head[0] and body[1] == head[1] + 10:
            state_index.append(1)
            break
    if len(state_index) == 6: #if no body part below the snake
        if head[1] == 0:
            state_index.append(1)
        else:
            state_index.append(0)

    #Hazard directly to the left
    for body in snake_body[1:]:
        if body[1] == head[1] and body[0] == head[0] - 10:
            state_index.append(1)
            break
    if len(state_index) == 7: #if no body part to the left of the snake
        if head[0] == 0:
            state_index.append(1)
        else:
            state_index.append(0)



    #Snake is facing up
    if direction == "UP":
        state_index.append(1)
    else:
        state_index.append(0)
    #Snake is facing right
    if direction == "RIGHT":
        state_index.append(1)
    else:
        state_index.append(0)
    #Snake is facing down
    if direction == "DOWN":
        state_index.append(1)
    else:
        state_index.append(0)
    #Snake is facing left
    if direction == "LEFT":
        state_index.append(1)
    else:
        state_index.append(0)
    return tuple(state_index)
            

def train():
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)
    discount_factor = 0.99

    for episode in range(NUM_TRAIN_EPISODES):
    #initialize our game
        # defining snake default position
        snake_position = [100, 50]

        # defining first 4 blocks of snake body
        snake_body = [[100, 50],
                                [90, 50],
                                [80, 50],
                                [70, 50]
                                ]
        # fruit position
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                        random.randrange(1, (window_y//10)) * 10]

        fruit_spawn = True

        # setting default snake direction towards
        # right
        direction = 'RIGHT'
        change_to = direction

        # initial score
        score = 0        
        state_0 = get_state(snake_body, fruit_position, direction) #get our initial state
        time = 0
        while True:
            time +=1
            reward = 0
            prevpos = snake_body[0]
            action = select_action(state_0, explore_rate) #select action
            #execute action
            if action == 0:
                change_to = "UP"
            if action == 1:
                change_to = "DOWN"
            if action == 2:
                change_to = "LEFT"
            if action == 3:
                change_to = "RIGHT"


            # If two keys pressed simultaneously
            # we don't want snake to move into two
            # directions simultaneously
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10

            currentpos = snake_body[0]
            if math.sqrt( (pow(currentpos[0]-fruit_position[0],2)) + (pow(currentpos[1]-fruit_position[1],2)) ) <= math.sqrt( (pow(prevpos[0]-fruit_position[0],2)) + (pow(prevpos[1]-fruit_position[1],2)) ):
                reward = 1
            else:
                reward = -1

            # Snake body growing mechanism
            # if fruits and snakes collide then scores
            # will be incremented by 10
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 10
                reward = 10
                fruit_spawn = False
            else:
                snake_body.pop()
                    
            if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                                    random.randrange(1, (window_y//10)) * 10]
                    
            fruit_spawn = True

            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x-10:
                reward = -100
            if snake_position[1] < 0 or snake_position[1] > window_y-10:
                reward = -100
            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    reward = -100
                    break

            #get our new state
            state = get_state(snake_body, fruit_position, direction)
            #update Q based on the result
            # Update the Q based on the result
            best_q = np.amax(q_table[state]) #get the best q of the now current state
            pass
            q_table[state_0 + (action,)] += learning_rate*(reward + discount_factor*(best_q) - q_table[state_0 + (action,)]) #update the QValue for the previous state
            state_0 = state #prepare for the next timestep by setting our previous state to the current state
            if reward == -100:
                break
            
        #update parameters for the next episode
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)
        print("Episode %d finished after %f time steps" % (episode, time))

    return q_table

def test(q_table):
    for episode in range(NUM_TEST_EPISODES):
        snake_speed = 15

        # Window size
        window_x = 720
        window_y = 480

        # defining colors
        black = pygame.Color(0, 0, 0)
        white = pygame.Color(255, 255, 255)
        red = pygame.Color(255, 0, 0)
        green = pygame.Color(0, 255, 0)
        blue = pygame.Color(0, 0, 255)

        # Initialising pygame
        pygame.init()

        # Initialise game window
        pygame.display.set_caption('Snake Game')
        game_window = pygame.display.set_mode((window_x, window_y))

        # FPS (frames per second) controller
        fps = pygame.time.Clock()

    #initialize our game
        # defining snake default position
        snake_position = [100, 50]

        # defining first 4 blocks of snake body
        snake_body = [[100, 50],
                                [90, 50],
                                [80, 50],
                                [70, 50]
                                ]
        # fruit position
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                        random.randrange(1, (window_y//10)) * 10]

        fruit_spawn = True

        # setting default snake direction towards
        # right
        direction = 'RIGHT'
        change_to = direction

        # initial score
        score = 0        
        state_0 = get_state(snake_body, fruit_position, direction) #get our initial state


        while True:
            reward = 1
            quitflag = False

            # handling key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0 or event.key == pygame.K_s:
                        snake_speed/=2
                    if event.key == pygame.K_1 or event.key == pygame.K_w:
                        snake_speed*=2

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quitflag = True


            if quitflag:
                break
            
            action = select_action(state_0, 0) #select action
            #execute action
            if action == 0:
                change_to = "UP"
            if action == 1:
                change_to = "DOWN"
            if action == 2:
                change_to = "LEFT"
            if action == 3:
                change_to = "RIGHT"


            
            # If two keys pressed simultaneously
            # we don't want snake to move into two
            # directions simultaneously
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10

            # Snake body growing mechanism
            # if fruits and snakes collide then scores
            # will be incremented by 10
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 10
                fruit_spawn = False
            else:
                snake_body.pop()
                    
            if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                                    random.randrange(1, (window_y//10)) * 10]
                    
            fruit_spawn = True
            game_window.fill(black)

            counter = 0
            for pos in snake_body:
                    if counter==0:
                             pygame.draw.rect(game_window, red,
                                                    pygame.Rect(pos[0], pos[1], 10, 10))
                    else:                    
                            pygame.draw.rect(game_window, green,
                                                    pygame.Rect(pos[0], pos[1], 10, 10))
                    counter+=1
            pygame.draw.rect(game_window, white, pygame.Rect(
                    fruit_position[0], fruit_position[1], 10, 10))

            state_0 = get_state(snake_body, fruit_position, direction)
            
            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x-10:
                game_over(score, red, game_window)
                break
            if snake_position[1] < 0 or snake_position[1] > window_y-10:
                game_over(score, red, game_window)
                break

            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over(score, red, game_window)
                    break

            # displaying score countinuously
            show_score(1, white, 'times new roman', 20, score, game_window)

            # Refresh game screen
            pygame.display.update()

            # Frame Per Second /Refresh Rate
            fps.tick(snake_speed)


def getresults():
    ### Window size
    window_x = 720
    window_y = 480

    #Reinforcement Learning Parameters
    NUM_ACTIONS = int(4) #UP, DOWN, LEFT, RIGHT


    NUM_BUCKETS = (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

    q_table = np.zeros(tuple(NUM_BUCKETS) + (NUM_ACTIONS,))

    MIN_EXPLORE_RATE = 0.01
    MIN_LEARNING_RATE = 0.1

    NUM_TRAIN_EPISODES = 500
    NUM_TEST_EPISODES = 100

    q_table = train()

    snake_speed = 15

    # Window size
    window_x = 720
    window_y = 480

#initialize our game
    # defining snake default position
    snake_position = [100, 50]

    # defining first 4 blocks of snake body
    snake_body = [[100, 50],
                            [90, 50],
                            [80, 50],
                            [70, 50]
                            ]
    # fruit position
    fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                    random.randrange(1, (window_y//10)) * 10]

    fruit_spawn = True

    # setting default snake direction towards
    # right
    direction = 'RIGHT'
    change_to = direction

    # initial score
    score = 0        
    state_0 = get_state(snake_body, fruit_position, direction) #get our initial state

    graphy = [0]
    
    while True:
        gameoverflag = False

        action = select_action(state_0, 0) #select action
        #execute action
        if action == 0:
            change_to = "UP"
        if action == 1:
            change_to = "DOWN"
        if action == 2:
            change_to = "LEFT"
        if action == 3:
            change_to = "RIGHT"


        
        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()
                
        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                                random.randrange(1, (window_y//10)) * 10]
                
        fruit_spawn = True

        counter = 0
        state_0 = get_state(snake_body, fruit_position, direction)
        
        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-10:
            gameoverflag = True
            
        if snake_position[1] < 0 or snake_position[1] > window_y-10:
            gameoverflag = True
            

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                gameoverflag = True
                

        if gameoverflag == True or len(graphy) > 10000:
            break

        graphy.append(score)

    return graphy
    
# displaying Score function
def show_score(choice, color, font, size, score, game_window):

	# creating font object score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

# game over function
def game_over(score, red, game_window):

	# creating font object my_font
	my_font = pygame.font.SysFont('times new roman', 50)
	
	# creating a text surface on which text
	# will be drawn
	game_over_surface = my_font.render(
		'Your Score is : ' + str(score), True, red)
	
	# create a rectangular object for the text
	# surface object
	game_over_rect = game_over_surface.get_rect()
	
	# setting position of the text
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit will draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	
	# after 2 seconds we will quit the program
	#time.sleep(2)
	
	# deactivating pygame library
	pygame.quit()
	

	
if __name__ == "__main__":
    ### Window size
    window_x = 720
    window_y = 480

    #Reinforcement Learning Parameters
    NUM_ACTIONS = int(4) #UP, DOWN, LEFT, RIGHT


    NUM_BUCKETS = (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

    q_table = np.zeros(tuple(NUM_BUCKETS) + (NUM_ACTIONS,))

    MIN_EXPLORE_RATE = 0.01
    MIN_LEARNING_RATE = 0.1

    NUM_TRAIN_EPISODES = 500
    NUM_TEST_EPISODES = 100

    q_table = train()
    test(q_table)

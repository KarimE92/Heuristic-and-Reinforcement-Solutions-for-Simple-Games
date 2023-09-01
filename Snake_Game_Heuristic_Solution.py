# importing libraries
import pygame
import time
import random



# displaying Score function
def show_score(choice, color, font, size):

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
def game_over():

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
	time.sleep(2)
	
	# deactivating pygame library
	pygame.quit()
	
	# quit the program
	quit()

def getresults():
        # Window size
        window_x = 720
        window_y = 480        

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

        #Graph coordinates
        graphy = [0]
        # Main Function
        while True:
            gameoverflag = False
        #we are going to replace the key events since that is what our agent is going to do
        #our goal is to get to the top left corner of the screen and then snake our way up and down repeatedly

            #coding behavior that makes the snake move towards the food
            #if snakex - foodx = +ve, then move left
            if snake_position[1] == fruit_position[1]:
                if snake_position[0] > fruit_position[0]:
                    change_to = "LEFT"
                if snake_position[0] < fruit_position[0]:
                    change_to = "RIGHT"

            #if snakey - foody = +ve, then move down
            if snake_position[0] == fruit_position[0]:
                if snake_position[1] > fruit_position[1]:
                    change_to = "UP"
                if snake_position[1] < fruit_position[1]:
                    change_to = "DOWN"

            #if we are going right and we reach the end of the screen we move towards the fruit
            if direction == "RIGHT" and snake_position[0] == window_x-10:
                if snake_position[1] > fruit_position[1]:
                    change_to = "UP"
                elif snake_position[1] < fruit_position[1]:
                    change_to = "DOWN"
                else:
                    if snake_position[1] > window_y/2:
                        change_to = "UP"
                    else:
                        change_to = "DOWN"

            #if we are going down and we reach the end of the screen we move in the direction of the fruit
            if direction == "DOWN" and snake_position[1] == window_y-10:
                if snake_position[0] > fruit_position[0]:
                    change_to = "LEFT"
                elif snake_position[0] < fruit_position[0]:
                    change_to = "RIGHT"
                else:
                    if snake_position[0] > window_x/2:
                        change_to = "LEFT"
                    else:
                        change_to = "RIGHT"

            #if we are going up and reach the end of the screen we move in the direction of the fruit
            if direction == "UP" and snake_position[1] == 0:
                if snake_position[0] > fruit_position[0]:
                    change_to = "LEFT"
                elif snake_position[0] < fruit_position[0]:
                    change_to = "RIGHT"
                else:
                    if snake_position[0] > window_x/2:
                        change_to = "LEFT"
                    else:
                        change_to = "RIGHT"

            #if we are going up and we are on the far left of the screen we just go right
            if direction == "UP" and snake_position[0] == 0 and snake_position[1] == 0:
                change_to = "RIGHT"
                
            if direction == "UP" and snake_position[0] == window_x-10 and snake_position[1] == 0:
                change_to = "LEFT"

            #if we are going left and we are on the far left of the screen we move in the direction of the fruit
            if direction == "LEFT" and snake_position[0] == 0:
                if snake_position[1] > fruit_position[1]:
                    change_to = "UP"
                elif snake_position[1] < fruit_position[1]:
                    change_to = "DOWN"
                else:
                    if snake_position[1] > window_y/2:
                        change_to = "UP"
                    else:
                        change_to = "DOWN"


            #now we add code to check if the snake is going to collide with its own body
            if change_to == "UP":
                nextpos = [snake_position[0], snake_position[1]-10] #get predicted next position
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:        
                    if direction == "UP":
                        if snake_position[0] > fruit_position[0]:
                            change_to = "LEFT"
                        elif snake_position[0] < fruit_position[0]:
                            change_to = "RIGHT"
                        else:
                            if snake_position[0] > window_x/2:
                                change_to = "LEFT"
                            else:
                                change_to = "RIGHT"
                    else:
                        change_to = "Null"
                        
            if change_to == "DOWN":
                nextpos = [snake_position[0], snake_position[1]+10]
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:  
                    if direction == "DOWN":
                        if snake_position[0] > fruit_position[0]:
                            change_to = "LEFT"
                        elif snake_position[0] < fruit_position[0]:
                            change_to = "RIGHT"
                        else:
                            if snake_position[0] > window_x/2:
                                change_to = "LEFT"
                            else:
                                change_to = "RIGHT"
                    else:
                        change_to = "Null"
                    
            if change_to == "LEFT":
                nextpos = [snake_position[0]-10, snake_position[1]]
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:  
                    if direction == "LEFT":
                        if snake_position[1] > fruit_position[1]:
                            change_to = "UP"
                        elif snake_position[1] < fruit_position[1]:
                            change_to = "DOWN"
                        else:
                            if snake_position[1] > window_y/2:
                                change_to = "UP"
                            else:
                                change_to = "DOWN"
                    else:
                        change_to = "Null"
                    
            if change_to == "RIGHT":
                nextpos = [snake_position[0]+10, snake_position[1]]
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:  
                    if direction == "RIGHT":
                        if snake_position[1] > fruit_position[1]:
                            change_to = "UP"
                        elif snake_position[1] < fruit_position[1]:
                            change_to = "DOWN"
                        else:
                            if snake_position[1] > window_y/2:
                                change_to = "UP"
                            else:
                                change_to = "DOWN"
                    else:
                        change_to = "Null"
                
                
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

            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x-10:
                gameoverflag = True

            if snake_position[1] < 0 or snake_position[1] > window_y-10:
                gameoverflag = True

            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    gameoverflag = True
                    
            if gameoverflag == True:
                break

            graphy.append(score)
            
        return graphy
                



if __name__ == "__main__":
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

        # Main Function
        while True:
            
            # handling key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0 or event.key == pygame.K_s:
                        snake_speed/=2
                    if event.key == pygame.K_1 or event.key == pygame.K_w:
                        snake_speed*=2


        #we are going to replace the key events since that is what our agent is going to do
        #our goal is to get to the top left corner of the screen and then snake our way up and down repeatedly

            #coding behavior that makes the snake move towards the food
            #if snakex - foodx = +ve, then move left
            if snake_position[1] == fruit_position[1]:
                if snake_position[0] > fruit_position[0]:
                    change_to = "LEFT"
                if snake_position[0] < fruit_position[0]:
                    change_to = "RIGHT"

            #if snakey - foody = +ve, then move down
            if snake_position[0] == fruit_position[0]:
                if snake_position[1] > fruit_position[1]:
                    change_to = "UP"
                if snake_position[1] < fruit_position[1]:
                    change_to = "DOWN"

            #if we are going right and we reach the end of the screen we move towards the fruit
            if direction == "RIGHT" and snake_position[0] == window_x-10:
                if snake_position[1] > fruit_position[1]:
                    change_to = "UP"
                elif snake_position[1] < fruit_position[1]:
                    change_to = "DOWN"
                else:
                    if snake_position[1] > window_y/2:
                        change_to = "UP"
                    else:
                        change_to = "DOWN"

            #if we are going down and we reach the end of the screen we move in the direction of the fruit
            if direction == "DOWN" and snake_position[1] == window_y-10:
                if snake_position[0] > fruit_position[0]:
                    change_to = "LEFT"
                elif snake_position[0] < fruit_position[0]:
                    change_to = "RIGHT"
                else:
                    if snake_position[0] > window_x/2:
                        change_to = "LEFT"
                    else:
                        change_to = "RIGHT"

            #if we are going up and reach the end of the screen we move in the direction of the fruit
            if direction == "UP" and snake_position[1] == 0:
                if snake_position[0] > fruit_position[0]:
                    change_to = "LEFT"
                elif snake_position[0] < fruit_position[0]:
                    change_to = "RIGHT"
                else:
                    if snake_position[0] > window_x/2:
                        change_to = "LEFT"
                    else:
                        change_to = "RIGHT"

            #if we are going up and we are on the far left of the screen we just go right
            if direction == "UP" and snake_position[0] == 0 and snake_position[1] == 0:
                change_to = "RIGHT"
                
            if direction == "UP" and snake_position[0] == window_x-10 and snake_position[1] == 0:
                change_to = "LEFT"

            #if we are going left and we are on the far left of the screen we move in the direction of the fruit
            if direction == "LEFT" and snake_position[0] == 0:
                if snake_position[1] > fruit_position[1]:
                    change_to = "UP"
                elif snake_position[1] < fruit_position[1]:
                    change_to = "DOWN"
                else:
                    if snake_position[1] > window_y/2:
                        change_to = "UP"
                    else:
                        change_to = "DOWN"


            #now we add code to check if the snake is going to collide with its own body
            if change_to == "UP":
                nextpos = [snake_position[0], snake_position[1]-10] #get predicted next position
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:        
                    if direction == "UP":
                        if snake_position[0] > fruit_position[0]:
                            change_to = "LEFT"
                        elif snake_position[0] < fruit_position[0]:
                            change_to = "RIGHT"
                        else:
                            if snake_position[0] > window_x/2:
                                change_to = "LEFT"
                            else:
                                change_to = "RIGHT"
                    else:
                        change_to = "Null"
                        
            if change_to == "DOWN":
                nextpos = [snake_position[0], snake_position[1]+10]
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:  
                    if direction == "DOWN":
                        if snake_position[0] > fruit_position[0]:
                            change_to = "LEFT"
                        elif snake_position[0] < fruit_position[0]:
                            change_to = "RIGHT"
                        else:
                            if snake_position[0] > window_x/2:
                                change_to = "LEFT"
                            else:
                                change_to = "RIGHT"
                    else:
                        change_to = "Null"
                    
            if change_to == "LEFT":
                nextpos = [snake_position[0]-10, snake_position[1]]
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:  
                    if direction == "LEFT":
                        if snake_position[1] > fruit_position[1]:
                            change_to = "UP"
                        elif snake_position[1] < fruit_position[1]:
                            change_to = "DOWN"
                        else:
                            if snake_position[1] > window_y/2:
                                change_to = "UP"
                            else:
                                change_to = "DOWN"
                    else:
                        change_to = "Null"
                    
            if change_to == "RIGHT":
                nextpos = [snake_position[0]+10, snake_position[1]]
                #check if that position intersects with a body part
                intersect = False
                for pos in snake_body:
                    if nextpos[0] == pos[0] and nextpos[1] == pos[1]:
                        intersect = True

                if intersect == True:  
                    if direction == "RIGHT":
                        if snake_position[1] > fruit_position[1]:
                            change_to = "UP"
                        elif snake_position[1] < fruit_position[1]:
                            change_to = "DOWN"
                        else:
                            if snake_position[1] > window_y/2:
                                change_to = "UP"
                            else:
                                change_to = "DOWN"
                    else:
                        change_to = "Null"
                
                
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
                if counter == 0:
                    pygame.draw.rect(game_window, red,
                                                        pygame.Rect(pos[0], pos[1], 10, 10))
                    
                else:
                    pygame.draw.rect(game_window, green,
                                                        pygame.Rect(pos[0], pos[1], 10, 10))
                counter+=1
            pygame.draw.rect(game_window, white, pygame.Rect(
                    fruit_position[0], fruit_position[1], 10, 10))

            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x-10:
                game_over()
            if snake_position[1] < 0 or snake_position[1] > window_y-10:
                game_over()

            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over()

            # displaying score countinuously
            show_score(1, white, 'times new roman', 20)

            # Refresh game screen
            pygame.display.update()

            # Frame Per Second /Refresh Rate
            fps.tick(snake_speed)

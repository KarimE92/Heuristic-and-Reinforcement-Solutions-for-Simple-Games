# Heuristic-and-Reinforcement-Solutions-for-Simple-Games
A small project about implementing QLearning into Snake and Tetris and comparing the agent's performance to heuristic solutions.
Snake.py is a fully playable snake game.
Snake_Reinforcement_Learning_Limited_Vision_Solution.py is a reinforcement learning solution for snake that uses the snake's neighbouring blocks in order to get its state. 
Snake_Reinforcement_Learning_Position_Tracking_Solution.py is a reinforcement learning solution for snake that uses the snake's position on the screen in order to get its state.
Tetris.py is a fully playable tetris game
Tetris_Reinforcement_Learning_Solution.py is not an efficient solution for Tetris. This is because there are so many unique states for Tetris that they can not be easily represented using the QLearning algorithm. Instead Deep QLearning will have to be implemented, which is not in the scope of this project. As a result, the state space for Tetris had to be greatly simplified, resulting in the agent not being able to solve Tetris.

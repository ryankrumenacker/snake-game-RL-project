# IMPORTS------------------------------------------------------------------------------------------------------------------------------------
import pygame
import random
pygame.font.init()

# GENERAL CONSTANTS -------------------------------------------------------------------------------------------------------------------------
WIDTH = 750
HEIGHT = 800
BAR_HEIGHT = HEIGHT - WIDTH
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('Snake Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)

FPS = 10

GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)

NUM_TILES = 20 # per row/column
TILE_SIZE = int(720 / NUM_TILES)

GAME_OVER = pygame.USEREVENT + 1

INITIAL_SNAKE_STATE = [0, 9, 11, 10, 9, 12]

# TILE CLASS -------------------------------------------------------------------------------------------------------------------------------  
class Tile:

    def __init__(self, row, column, is_snake, is_food, is_head):
        self.row = row
        self.column = column
        self.is_snake = is_snake
        self.is_food = is_food
        self.is_head = is_head

    def draw_tile(self):
        if self.is_snake:
            color = GREEN
        if self.is_head:
            color = YELLOW
        if self.is_food:
            color = RED

        x_coor = int(15 + self.column * TILE_SIZE)
        y_coor = int(BAR_HEIGHT + 15 + self.row * TILE_SIZE)
           
        rect = pygame.Rect(x_coor, y_coor, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(WIN, color, rect)

# BOARD CLASS ------------------------------------------------------------------------------------------------------------------------------
class Board:
    def __init__(self):
        self.structure = [[0 for _ in range(NUM_TILES)] for _ in range (NUM_TILES)]

    def update(self, game_snake, food_tile):
        self.structure = [[0 for _ in range(NUM_TILES)] for _ in range (NUM_TILES)]
        # adding snake
        for tile in game_snake.body:
            self.structure[tile.row][tile.column] = 1
        # adding food
        self.structure[food_tile.row][food_tile.column] = 2
        
        return np.array(self.structure).astype('intc')

    def create_start_board():
        board = [[0 for _ in range(NUM_TILES)] for _ in range(NUM_TILES)]
        board[10][5:8] = [1, 1, 1]
        board[10][16] = 2

        return np.array(board).astype('intc')

# SNAKE CLASS ------------------------------------------------------------------------------------------------------------------------------
INITIAL_SNAKE_HEAD  = [Tile(10, 7, True, False, True)]
INITIAL_SNAKE_BODY  = [Tile(10, 6, True, False, False), Tile(10, 5, True, False, False)]

# if you are going this direction, you can move in direction...
DIRECTION_KEY = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}

class Snake:
    
    def __init__(self):
        self.body = INITIAL_SNAKE_HEAD + INITIAL_SNAKE_BODY
        self.past_tiles_visited = []
        self.score = 0
        self.direction = 1

    def draw_snake(self):
        for tile in self.body:
            tile.draw_tile()

    def move_forward(self):
        current_snake_head = self.body[0]
        current_snake_head.is_head = False
        if self.direction == 0:
            new_snake_head = Tile(current_snake_head.row - 1, current_snake_head.column, True, False, True)
        elif self.direction == 1:
            new_snake_head = Tile(current_snake_head.row, current_snake_head.column + 1, True, False, True)
        elif self.direction == 2:
            new_snake_head = Tile(current_snake_head.row + 1, current_snake_head.column, True, False, True)
        elif self.direction == 3:
            new_snake_head = Tile(current_snake_head.row, current_snake_head.column - 1, True, False, True)
        
        # creating the new snake body with the new head at the front of the list
        self.body = [new_snake_head] + self.body
        last_tile = self.body.pop()
        self.past_tiles_visited = [(last_tile.row, last_tile.column)] + self.past_tiles_visited
        while len(self.past_tiles_visited) > 5:
            self.past_tiles_visited.pop()

    def change_direction(self, direction):
        if direction in DIRECTION_KEY[self.direction]:
            self.direction = direction

    def is_dead(self):
        current_snake_head = self.body[0]
        
        # left or right wall
        if current_snake_head.column >= 20 or current_snake_head.column <= -1:
            return True
        # top or bottom wall
        if current_snake_head.row >= 20 or current_snake_head.row <= -1:
            return True

        # itself
        for tile in self.body[1:]:
            if current_snake_head.row == tile.row and current_snake_head.column == tile.column:
                return True

        return False

    def is_eating(self, food_tile):
        current_snake_head = self.body[0]
        if current_snake_head.row == food_tile.row and current_snake_head.column == food_tile.column:
            return True
        return False

    # occurs after the snake has eaten a food
    def grow(self):
        last_tile = self.past_tiles_visited[0]
        tail = Tile(last_tile[0], last_tile[1], True, False, False)
        self.body.append(tail)
        self.past_tiles_visited = self.past_tiles_visited[1:]

# GAME FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------
def grow_new_food(game_snake, food_tile):
    all_tiles = [(x, y) for x in range(NUM_TILES) for y in range(NUM_TILES)]
    for tile in game_snake.body:
        all_tiles.remove((tile.row, tile.column))

    
    new_position = random.choice(all_tiles)
    food_tile = Tile(new_position[0], new_position[1], False, True, False)
    return food_tile

def draw_end_text():
    draw_text = GAME_OVER_FONT.render('GAME OVER', 1, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()

def draw_grid():
    for x in range(15, WIDTH - 15, TILE_SIZE):
        for y in range(15 + HEIGHT - WIDTH, HEIGHT - 15, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(WIN, WHITE, rect, 1)

def draw_window(game_snake, food_tile):
    # drawing the background
    WIN.fill(BLACK)

    # drawing the grid
    draw_grid()

    # drawing the score
    score_text = SCORE_FONT.render(f'Score: {game_snake.score}', 1, WHITE)
    WIN.blit(score_text, (15, 5))

    # drawing the snake
    game_snake.draw_snake()

    # drawing the food
    food_tile.draw_tile()

    pygame.display.update()

def main(game_snake, food_tile):
    WIN.fill(BLACK)

    clock = pygame.time.Clock()
    run = True
    # game loop
    while run:
        clock.tick(FPS)
        first_key = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and first_key:
                    game_snake.change_direction(0)
                    first_key = False
                if event.key == pygame.K_RIGHT and first_key:
                    game_snake.change_direction(1) 
                    first_key = False
                if event.key == pygame.K_DOWN and first_key:
                    game_snake.change_direction(2) 
                    first_key = False
                if event.key == pygame.K_LEFT and first_key:
                    game_snake.change_direction(3)
                    first_key = False

        # checking to see if they have ran into a wall or itself
        if (game_snake.is_dead()):
            draw_end_text()
            break

        if (game_snake.is_eating(food_tile)):
            game_snake.score += 1
            game_snake.grow()
            food_tile = grow_new_food(game_snake, food_tile)
            
        game_snake.move_forward()

        draw_window(game_snake, food_tile)

    pygame.time.delay(5000)
    pygame.quit()

# -------------------------------------------------------------------------------------------------------------------------------------------
# REINFORCEMENT LEARNING BEGINS HERE --------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------

# IMPORTS -----------------------------------------------------------------------------------------------------------------------------------
import gym
from gym import Env
from gym.spaces import Discrete, Box

import numpy as np
import random
import os

from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.vec_env import dummy_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor

# SNAKE ENVIRONMENT CLASS ---------------------------------------------------------------------------------------------------------------------
class SnakeEnv(Env):

    def __init__(self, game_snake, food_tile):
        self.action_space = Discrete(4)
        self.observation_space = Box(low=-NUM_TILES, high=NUM_TILES, shape=(6,), dtype=np.intc)
        self.state = np.array(INITIAL_SNAKE_STATE).astype('intc')

        self.game_snake = game_snake
        self.food_tile = food_tile
        
    def step(self, action):
        reward = 0
        done = False

        self.game_snake.change_direction(action)

        info = {}
        # if the snake ran into a wall
        if self.state[2] == 0 or self.state[3] == 0 or self.state[4] == 0 or self.state[5] == 0:
            done = True
            return None, 0, done, info
        # if the snake ran into itself
        for tile in self.game_snake.body[1:]:
            if self.game_snake.body[0].row == tile.row and self.game_snake.body[0].column == tile.column:
                done = True
                return None, 0, done, info

        if self.state[0] == 0 and self.state[1] == 0:
            self.game_snake.score += 1
            self.game_snake.grow()
            self.food_tile = grow_new_food(self.game_snake, self.food_tile)
            reward = 1

        self.game_snake.move_forward()

        rows_from_food = self.food_tile.row - self.game_snake.body[0].row
        columns_from_food = self.food_tile.column - self.game_snake.body[0].column
        rows_from_top_wall = self.game_snake.body[0].row + 1
        rows_from_bottom_wall = NUM_TILES - self.game_snake.body[0].row
        columns_from_left_wall = self.game_snake.body[0].column + 1
        columns_from_right_wall = NUM_TILES - self.game_snake.body[0].column

        obs = np.array([rows_from_food, 
                        columns_from_food, 
                        rows_from_top_wall, 
                        rows_from_bottom_wall, 
                        columns_from_left_wall, 
                        columns_from_right_wall]).astype('intc')

        self.state = obs

        return obs, reward, done, info

    def render(self, arg):
        clock = pygame.time.Clock()
        if arg:
            clock.tick(FPS)
            draw_window(self.game_snake, self.food_tile)

    def reset(self):
        self.game_snake = Snake()
        self.food_tile = Tile(10, 16, False, True, False)
        self.observation_space = Box(low=-NUM_TILES, high=NUM_TILES, shape=(6,), dtype=np.intc)
        self.state = np.array(INITIAL_SNAKE_STATE).astype('intc')
        return np.array(INITIAL_SNAKE_STATE).astype('intc')

    def close(self):
        pygame.quit()

# ACTUAL CODE ----------------------------------------------------------------------------------------------------------------------------
game_snake = Snake()
food_tile = Tile(10, 16, False, True, False)
log_path = os.path.join('Array-Optimization','Training', 'Logs')

env = Monitor(SnakeEnv(game_snake, food_tile))

# episodes = 1
# for episode in range(1, episodes + 1):
#     obs = env.reset()
#     done = False
#     score = 0

#     clock = pygame.time.Clock()
#     while not done:
#         clock.tick(FPS)
#         env.render()
#         action = env.action_space.sample()
#         obs, reward, done, info = env.step(action)
#         print(obs)
#         score += reward
#     print(f'Episode: {episode}, Score: {score}')
# env.close()

# check_env(env)

Model_Path = os.path.join('Array-Optimization', 'Training', 'Saved Models', 'PPO-Model-Snake-1m')
model = PPO.load(Model_Path, env=env)

# model = A2C('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps=1000000)
# model.save(Model_Path)

evaluation = evaluate_policy(model, model.get_env(), n_eval_episodes=2, render=True)
print(evaluation)

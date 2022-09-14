# IMPORTS------------------------------------------------------------------------------------------------------------------------------------
import struct
from threading import currentThread
import pygame
import random
import numpy as np
pygame.font.init()

# GENERAL CONSTANTS -------------------------------------------------------------------------------------------------------------------------
WIDTH = 750
HEIGHT = 800
BAR_HEIGHT = HEIGHT - WIDTH
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

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
        self.past_tiles_visited = [self.body.pop()] + self.past_tiles_visited
        self.past_tiles_visited[0].is_snake = False

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
        tail = self.past_tiles_visited[0]
        tail.is_snake = True
        self.body.append(tail)
        self.past_tiles_visited = self.past_tiles_visited[1:]

# GAME FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------
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

def main():
    WIN.fill(BLACK)

    game_snake = Snake()
    food_tile = Tile(10, 16, False, True, False)

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

if __name__ == '__main__':
     main()
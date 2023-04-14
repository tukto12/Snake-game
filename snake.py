import pygame
import sys
import random
from pygame.math import Vector2


# all classes that we need for snake game
# ========================================================================
class Snake(object):
    def __init__(self):
        self.body = [Vector2(9, 9), Vector2(8, 9)]
        self.move_direction = Vector2(1, 0)
        self.grow = False

    def draw_snake(self):
        # creating each snake body element
        for elements in self.body:
            snake_rect = pygame.Rect(
                elements.x * cell_size, elements.y * cell_size, cell_size, cell_size)

            pygame.draw.rect(window, (0, 255, 0), snake_rect)

    def move_snake(self):
        if self.grow:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.move_direction)
            self.body = body_copy[:]
            self.grow = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.move_direction)
            self.body = body_copy[:]

    def grow_snake(self):
        self.grow = True


class Food(object):
    def __init__(self):
        self.random_food_position()

    def draw_food(self):
        # creating the food
        food_rect = pygame.Rect(self.food_position.x * cell_size,
                                self.food_position.y * cell_size, cell_size, cell_size)
        # draw the food
        pygame.draw.rect(window, (255, 0, 0), food_rect)
        pass

    def random_food_position(self):
        self.x = random.randint(0, cell_numbers - 1)
        self.y = random.randint(0, cell_numbers - 1)
        self.food_position = Vector2(self.x, self.y)


class MainGame(object):
    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def draw_elements(self):
        self.snake.draw_snake()
        self.food.draw_food()

    def update(self):
        self.snake.move_snake()
        self.check_food_collision()

    def check_food_collision(self):
        # if snake took the food
        if self.food.food_position == self.snake.body[0]:
            print('Food')
            # spawning new food
            self.food.random_food_position()
            self.snake.grow_snake()


# ========================================================================
pygame.init()

cell_size = 30
cell_numbers = 20
window_size = cell_numbers * cell_size

window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = MainGame()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()

        # checking if a arrow key has been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # if snake is moving down he can not move up
                if game.snake.move_direction.y != 1:
                    game.snake.move_direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                # if snake is moving up he can not move down
                if game.snake.move_direction.y != -1:
                    game.snake.move_direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                # if snake is moving right he can not move left
                if game.snake.move_direction.x != 1:
                    game.snake.move_direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                # if snake is moving left he can not move right
                if game.snake.move_direction.x != -1:
                    game.snake.move_direction = Vector2(1, 0)

    # background-color -> black
    window.fill((0, 0, 0))
    game.draw_elements()
    pygame.display.update()
    # framerate of the game
    clock.tick(60)

# ========================================================================

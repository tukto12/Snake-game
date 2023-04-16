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
        for element in self.body:
            snake_rect = pygame.Rect(
                element.x * cell_size, element.y * cell_size, cell_size, cell_size)

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
    def __init__(self, points=0):
        self.snake = Snake()
        self.food = Food()
        self.points = points

    def draw_elements(self):
        self.snake.draw_snake()
        self.food.draw_food()

    def update(self):
        self.snake.move_snake()
        self.check_food_collision()
        self.check_snake_collision()

    def check_food_collision(self):
        # if snake took the food
        if self.food.food_position == self.snake.body[0]:
            print('Food')
            self.points += 1
            # spawning new food
            self.food.random_food_position()
            self.snake.grow_snake()

    def check_snake_collision(self):
        # checking if the snake head hits his body
        for element in self.snake.body[1:]:
            if element == self.snake.body[0]:
                print('Game Over!')
                pygame.quit()
                sys.exit()

        # checking if the snake hits the screen edge
        if not 0 <= self.snake.body[0].x <= cell_numbers or not 0 <= self.snake.body[0].y <= cell_numbers:
            print('Game Over!')
            pygame.quit()
            sys.exit()

    def display_points(self):
        font = pygame.font.Font("arial.ttf", 20)
        score = font.render(f'Score: {game.points}', True, (0, 255, 0))
        window.blit(score, (1, 1))

    def pause(self):
        paused = True
        large_font = pygame.font.Font("arial.ttf", 40)
        small_font = pygame.font.Font("arial.ttf", 20)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            window.fill((255, 255, 255))
            message_one = large_font.render('Paused', True, (0, 255, 0))
            message_two = small_font.render(
                'Click c to unpause', True, (0, 255, 0))
            message_three = small_font.render(
                'Click q to quit', True, (0, 255, 0))
            window.blit(message_one, (250, 230))
            window.blit(message_two, (238, 300))
            window.blit(message_three, (238, 330))
            pygame.display.update()
            clock.tick(15)


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

            if event.key == pygame.K_p:
                game.pause()

    # background-color -> black
    window.fill((0, 0, 0))
    game.draw_elements()
    game.display_points()
    pygame.display.update()
    # framerate of the game
    clock.tick(60)

# ========================================================================

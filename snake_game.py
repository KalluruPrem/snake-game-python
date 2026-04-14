import pygame
import random
import sys

pygame.init()

# Setting up the screen size and title
width, height = 600, 600
cell = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25)

# Adding colors to the Game
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
red = (200, 0, 0)

# Snake setup
snake = [(10, 10)]
direction = (1, 0)
next_direction = direction

# Food
food = (random.randint(0, (width//cell)-1), random.randint(0, (height//cell)-1))

score = 0
speed = 10
game_over = False
paused = False

while True:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Pause the game
            if event.key == pygame.K_p and not game_over:
                paused = not paused
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)
            else:
                if event.key == pygame.K_r:
                    # reset everything
                    snake = [(10, 10)]
                    direction = (1, 0)
                    next_direction = direction
                    food = (random.randint(0, (width//cell)-1), random.randint(0, (height//cell)-1))
                    score = 0
                    speed = 10
                    game_over = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    if not game_over and not paused:
        direction = next_direction

        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)

        # Wall collision
        if head_x < 0 or head_x >= width//cell or head_y < 0 or head_y >= height//cell:
            game_over = True

        # Self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            # Eat food
            if new_head == food:
                score += 1
                food = (random.randint(0, (width//cell)-1), random.randint(0, (height//cell)-1))
                if speed < 20:
                    speed += 1
            else:
                snake.pop()

    # Drawing the screen
    screen.fill(black)

    # Draw snake parts
    for part in snake:
        pygame.draw.rect(screen, green, (part[0]*cell, part[1]*cell, cell, cell))

    # Draw food part
    pygame.draw.rect(screen, red, (food[0]*cell, food[1]*cell, cell, cell))

    # Score text
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))


    # Paused text
    if paused and not game_over:
        pause_text = font.render("Paused (Press P)", True, blue)
        screen.blit(pause_text, (200, 280))


    # Game over text and restart
    if game_over:
        text1 = font.render("Game Over!", True, red)
        text2 = font.render("Press R to Restart", True, white)
        screen.blit(text1, (220, 250))
        screen.blit(text2, (180, 300))

    pygame.display.update()
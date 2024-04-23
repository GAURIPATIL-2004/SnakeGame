import pygame
import time
import random

pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Window size
dis_width = 800
dis_height = 600

# Snake size
snake_block = 20
snake_speed = 10

# Font
font_style = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

# Load snake images
head_img = pygame.image.load("snake_head.png")
body_img = pygame.image.load("snake_body.png")
tail_img = pygame.image.load("snake_tail.png")

# Load sounds
eat_sound = pygame.mixer.Sound("eat.mp3")
crash_sound = pygame.mixer.Sound("crash.mp3")

# Background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Score display
def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# Snake
def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            dis.blit(head_img, (x[0], x[1]))
        elif i == 0:
            dis.blit(tail_img, (x[0], x[1]))
        else:
            dis.blit(body_img, (x[0], x[1]))

# Message
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

# Mode selection
def mode_selection():
    mode_selected = False
    selected_mode = "easy"
    while not mode_selected:
        dis.fill(blue)
        message("Select Mode", black, -50)
        message("Easy (E)", green, -10)
        message("Medium (M)", yellow, 30)
        message("Hard (H)", red, 70)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    selected_mode = "easy"
                    mode_selected = True
                elif event.key == pygame.K_m:
                    selected_mode = "medium"
                    mode_selected = True
                elif event.key == pygame.K_h:
                    selected_mode = "hard"
                    mode_selected = True
    return selected_mode

# Welcome Screen
def welcome():
    welcome = True
    while welcome:
        dis.fill(blue)
        message("Welcome to Snake Game", black, -50)
        message("Press S to Start, Q to Quit", black, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    welcome = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Game loop
def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    mode = mode_selection()
    if mode == "easy":
        snake_speed = 10
    elif mode == "medium":
        snake_speed = 15
    else:
        snake_speed = 20

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            crash_sound.play()
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                crash_sound.play()
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            eat_sound.play()
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Game window
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")

# Game clock
clock = pygame.time.Clock()

welcome()
gameLoop()

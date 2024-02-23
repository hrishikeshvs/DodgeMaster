import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player
player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

# Obstacle
obstacle_size = 50
obstacle_pos = [random.randint(0, WIDTH-obstacle_size), 0]
obstacle_list = [obstacle_pos]

# Other variables
speed = 10
score = 0

# Set up fonts
font = pygame.font.SysFont(None, 50)

def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 8
    elif score < 60:
        speed = 12
    else:
        speed = 15
    return speed

def drop_obstacles(obstacle_list):
    delay = random.random()
    if len(obstacle_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-obstacle_size)
        y_pos = 0
        obstacle_list.append([x_pos, y_pos])

def draw_obstacles(obstacle_list):
    for obstacle_pos in obstacle_list:
        pygame.draw.rect(screen, RED, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))

def update_obstacle_positions(obstacle_list, score):
    for idx, obstacle_pos in enumerate(obstacle_list):
        if obstacle_pos[1] >= 0 and obstacle_pos[1] < HEIGHT:
            obstacle_pos[1] += speed
        else:
            obstacle_list.pop(idx)
            score += 1
    return score

def collision_check(obstacle_list, player_pos):
    for obstacle_pos in obstacle_list:
        if detect_collision(player_pos, obstacle_pos):
            return True
    return False

def detect_collision(player_pos, obstacle_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    o_x = obstacle_pos[0]
    o_y = obstacle_pos[1]

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obstacle_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obstacle_size)):
            return True
    return False

# Game loop
game_over = False
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            player_pos = [x, y]

    screen.fill(WHITE)

    # Drop and move obstacles
    drop_obstacles(obstacle_list)
    score = update_obstacle_positions(obstacle_list, score)
    speed = set_level(score, speed)

    # Display score
    score_text = "Score: " + str(score)
    score_display = font.render(score_text, True, RED)
    screen.blit(score_display, (10, 10))

    # Check for collision
    if collision_check(obstacle_list, player_pos):
        game_over = True
        break

    # Draw obstacles
    draw_obstacles(obstacle_list)

    # Draw player
    pygame.draw.rect(screen, (0, 0, 0), (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)
    pygame.display.update()

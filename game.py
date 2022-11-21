import sys
import os
import pygame
from goal import Goal
from player import Player
import numpy as np
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 94, 230, 130
RED = 230, 94, 94
BLUE = 94, 173, 230
BLOCK_SIZE = 20, 20
NUM_OBSTACLES = 100
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
font_size = 36
margin = 100

EPISODES = 24000
SHOW_EVERY = 3000
MOVE_PENALTY = 1
GOAL_REWARD = 25
OUT_OF_BOUNDS_PENALTY = 200
OBSTACLE_HIT_PENALTY = 300
EPS_DECAY = 0.9999
LEARNING_RATE = 0.1
DISCOUNT = 0.95
Q_TABLE_SIZE =  (SCREEN_WIDTH // BLOCK_SIZE[0] + 2, SCREEN_HEIGHT // BLOCK_SIZE[1] + 2, 4)
epsilon = 0.5
q_table = np.zeros(Q_TABLE_SIZE)

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, font_size)

goal = Goal(SCREEN_WIDTH, SCREEN_HEIGHT, GREEN)
goal_rect = goal.get_rect()
obstacle_rects = [pygame.Rect((random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE[0]), random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE[1])), BLOCK_SIZE) for i in range(NUM_OBSTACLES)]
while goal_rect in obstacle_rects:
    goal.change_pos(SCREEN_WIDTH, SCREEN_HEIGHT)
    goal_rect = goal.get_rect()

def gameInit():
    global player 
    global player_rect
    global goal_reached 
    global out_of_bounds

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    player_rect = player.get_rect()
    goal_reached = False
    out_of_bounds = False


def check_boundaries(head):
    if head.left < 0 or head.right > SCREEN_WIDTH or head.top < 0 or head.bottom > SCREEN_HEIGHT:
        return True
    return False


def setSpeedFromAction(action):
    if action == 0:
        player.set_speed([20, 0]) 
    elif action == 1:
        player.set_speed([-20, 0])
    elif action == 2:
        player.set_speed([0, 20])
    elif action == 3:
        player.set_speed([0, -20])
    
        
def coordsToState(coords):
    return coords[0] // 20 + 1, coords[1] // 20 + 1


def check_reached_goal(player_rect, goal_rect):
    if player_rect.colliderect(goal_rect):
            return True
    return False


def check_hit_obstacle(player_rect, obstacle_rects):
    if player_rect.collidelist(obstacle_rects):
            return True
    return False


for episode in range(EPISODES):
    if episode % SHOW_EVERY == 0:
        show = True
    else:
        show = False

    gameInit()

    for i in range(200):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        current_state = coordsToState(player.get_coords())
        
        if np.random.random() > epsilon:
            action =  np.argmax(q_table[current_state])
        else:
            action = np.random.randint(0, 4)
            
        setSpeedFromAction(action)
        player.move()
        player_rect = player.get_rect()
        player_coords = player.get_coords()
        out_of_bounds = check_boundaries(player_rect)
        goal_reached = check_reached_goal(player_rect, goal_rect)
        obstacle_hit = check_hit_obstacle(player_rect, obstacle_rects)

        if out_of_bounds:
            q_table[current_state + (action,)] = -OUT_OF_BOUNDS_PENALTY
            break
        elif goal_reached:
            reward = GOAL_REWARD
        elif obstacle_hit:
            reward = -OBSTACLE_HIT_PENALTY
        else:
            reward = -MOVE_PENALTY
        
        new_state = coordsToState(player_coords)
        max_future_q = np.max(q_table[new_state])
        current_q = q_table[current_state + (action,)]

        if goal_reached:
            new_q = reward
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        q_table[current_state + (action,)] = new_q

        if show:
            screen.fill(BLACK)
            pygame.draw.rect(screen, goal.color, goal_rect)
            pygame.draw.rect(screen, player.color, player_rect)
            for i in range(NUM_OBSTACLES):
                pygame.draw.rect(screen, RED, obstacle_rects[i])
            visited_rects = player.get_visited_rects()
            for i in range(len(visited_rects)):
                pygame.draw.rect(screen, BLUE, visited_rects[i])
            pygame.display.update()
            clock.tick(100)
        
        if reward == GOAL_REWARD:
            break

    # print(f'Episode: {episode}          Epsilon: {epsilon}')

    epsilon *= EPS_DECAY

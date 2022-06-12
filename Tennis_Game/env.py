# NOTES: 
# The observation space is continuous because the action space is described by real-valued coordinates
# The action space is discrete, you can only define the actions but not quantify them. This is, if you choose left, the agent goes left, but he cant go faster
# or slower than his speed.

import gym
import lib
import numpy as np
import pygame

# Declare vars
# Define some colors
BLACK = (0, 0, 0)
OUT = (193, 58, 34)
COURT = (69, 150, 81)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SKIN = (232, 214, 162)
YELLOW = (255, 0, 255)

def reset(point, screen, bottom_player, top_player, bottom_player_score, top_player_score):

    # bottom player won
    if point == 1: 
        bottom_player_score += 1
        lib.restart_player_position_bs(top_player, bottom_player)

    # top player won
    elif point == 2:
        top_player_score += 1
        lib.restart_player_position_ts(top_player, bottom_player)
    
    # Update scoreboards
    font = pygame.font.Font('freesansbold.ttf', 30)
    scorebox = font.render(str(top_player_score), True, WHITE, BLACK)
    scoreRect = scorebox.get_rect()
    scoreRect.center = (670, 50)
    screen.blit(scorebox, scoreRect)
    scorebox2 = font.render(str(bottom_player_score), True, WHITE, BLACK)
    scoreRect2 = scorebox2.get_rect()
    scoreRect2.center = (670, 50)
    screen.blit(scorebox2, scoreRect2)

    return True

# actions space is:
# Move: Up, Down, Left, Right
# Hit: straight, left, right
# Also: Serve

def get_serve():
    return {0:'Top Serve', 1:'Bottom Serve'}

def get_movement():
    return {0:'Up', 1:'Down', 2:'Left', 3:'Right'}

def get_stroke_direction():
    return {0:'Straigh', 1:'Left', 2:'Right'}


# step substitutyes the ball.update
def step_bp(serve_flag, bottom_player, top_player, ball, mode):
    
    if mode == 'random':
        if serve_flag == True:
            action = get_serve()[np.random.choice(list(get_serve().keys()))]
            print(action)
            if action == 'Bottom Serve':
                ball.update(serve_flag, bottom_player, action)
            if action == 'Top Serve':
                ball.update(serve_flag, top_player, action)

        else:
            if ball.rect.colliderect(bottom_player):
                action = get_stroke_direction()[np.random.choice(list(get_stroke_direction().keys()))]
                #print("cont", action)
                ball.update(serve_flag, bottom_player, action)

            else:
                action = get_movement()[np.random.choice(list(get_movement().keys()))]
                #print("no cont", action)
                bottom_player.update(action)
                ball.update(serve_flag, bottom_player)
    

def step_tp(serve_flag, bottom_player, top_player, ball, mode):
    
    point = 0
    if mode == 'random':
        if ball.rect.colliderect(top_player):
            action = get_stroke_direction()[np.random.choice(list(get_stroke_direction().keys()))]
            ball.update(serve_flag, top_player, action)

        else:
            action = get_movement()[np.random.choice(list(get_movement().keys()))]
            top_player.update(action)
            point = ball.update(serve_flag, top_player)
    
    return point
    



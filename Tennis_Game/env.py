# NOTES: 
# The observation space is continuous because the action space is described by real-valued coordinates
# The action space is discrete, you can only define the actions but not quantify them. This is, if you choose left, the agent goes left, but he cant go faster
# or slower than his speed.
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

AIR_RESISTANCE = 0.99


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

def get_movement():
    return {0:'Up', 1:'Down', 2:'Left', 3:'Right', 4:'Stay'}

def get_stroke_direction():
    return {0:'Straight', 1:'Left', 2:'Right'}

# it should only have one positive value
def only_postive_values(l):
    for i in l:
        if i > 0:
            return i
    return -1

# get x value when ball gets to players y
def get_x_of_ball(ball, player):

    # calculate how long till ball is at players y
    # using Y = Yo + Voby.t + 0.5at^2 
    p=[AIR_RESISTANCE/2, ball.speedy, ball.rect.y - player.rect.y]
    roots = np.roots(p)
    time = only_postive_values(roots)
    if time == -1:
        return 1000

    # now calculate x of the ball at time
    x_final = ball.rect.x + ball.speedx*time + 0.5*time**2

    return x_final


# step substitutyes the ball.update
def step_bp(player_to_strike, bottom_player, top_player, ball, mode):

    if mode == "random":
        # It is bottom's turn to hit the ball and it hits it
        if player_to_strike == bottom_player and ball.rect.colliderect(bottom_player):
            action = get_stroke_direction()[np.random.choice(tuple(get_stroke_direction().keys()))]
            print("Bot strike", action)
            # HIT
            return ball.strike(bottom_player, action)
        
        else:
            action = get_movement()[np.random.choice(tuple(get_movement().keys()))]
            bottom_player.update(action)
            print("Bot action", action)
            return None

    # Walks to ball x
    if mode == "beginner":
        # Bottom player turn
        if player_to_strike == bottom_player:
            # Bottom player hits the ball
            if ball.rect.colliderect(bottom_player):
                action = get_stroke_direction()[np.random.choice(list(get_stroke_direction().keys()))]
                print("Bot strike", action)
                # HIT
                return ball.strike(bottom_player, action)
           
            else:
                if bottom_player.rect.x > get_x_of_ball(ball, bottom_player):
                    action = 'Left'                
                elif bottom_player.rect.x < get_x_of_ball(ball, bottom_player):
                    action = 'Right'
                else:
                    action = 'Stay'
                print("Bot action", action)
                bottom_player.update(action)
                # None
                return None

        # Not its turn to hit the ball
        else:
            action = 'Stay'
            print("Bot action", action)
            bottom_player.update(action)
            # None
            return None

    # knows how to play, goes to the ball and knows where he should hit it
    if mode == "expert":
        # Bottom's turn to strike
        if player_to_strike == bottom_player:
            # Player stroke
            if ball.rect.colliderect(bottom_player):
                # gets the other player place on the court
                if (top_player.rect.x > 300 and top_player.rect.x < 225) or (top_player.rect.x < 300 and top_player.rect.x > 475):
                    action = 'Straight'
                else:
                    if top_player.rect.x < 300:
                        action = 'Right'
                    else:
                        action = 'Left'
                print("Bot strike", action)
                # HIT
                return ball.strike(bottom_player, action)
            # Did not hit the ball
            else:
                if bottom_player.rect.x > get_x_of_ball(ball, bottom_player):
                    action = 'Left'                
                elif bottom_player.rect.x < get_x_of_ball(ball, bottom_player):
                    action = 'Right'
                else:
                    action = 'Stay'
                print("Bot action", action)
                bottom_player.update(action)
                return None
        
        # Top's turn to play          
        else:
            action = 'Stay'
            # Does nothing
            bottom_player.update(action)
            # None
            return None


# Function to compute top side step
def step_tp(player_to_strike, bottom_player, top_player, ball, mode):
    
    # Random mode
    if mode == "random":
        # It is top's turn to hit the ball and it hits it
        if player_to_strike == top_player and ball.rect.colliderect(top_player):
            action = get_stroke_direction()[np.random.choice(tuple(get_stroke_direction().keys()))]
            # HIT
            return ball.strike(top_player, action)

        else:
            action = get_movement()[np.random.choice(tuple(get_movement().keys()))]
            top_player.update(action)
            print("Top action", action)
            return None
    
    # Walks to ball x
    if mode == "beginner":
        
        # Top player turn
        if player_to_strike == top_player:
            # Bottom player hits the ball
            if ball.rect.colliderect(top_player):
                action = get_stroke_direction()[np.random.choice(list(get_stroke_direction().keys()))]
                # HIT
                return ball.strike(top_player, action)
           
            else:
                if top_player.rect.x > get_x_of_ball(ball, top_player):
                    action = 'Left'                
                elif top_player.rect.x < get_x_of_ball(ball, top_player):
                    action = 'Right'
                else:
                    action = 'Stay'
                print("Top action", action)
                top_player.update(action)
                return None

        # Not its turn to hit the ball
        else:
            action = 'Stay'
            print("Top action", action)
            top_player.update(action)
            return None

    # knows how to play, goes to the ball and knows where he should hit it
    if mode == "expert":
        # Top's turn to strike
        if player_to_strike == top_player:
            
            # Player stroke
            if ball.rect.colliderect(top_player):
                # gets the other player place on the court
                if (bottom_player.rect.x > 300 and bottom_player.rect.x < 225) or (bottom_player.rect.x < 300 and bottom_player.rect.x > 475):
                    action = 'Straight'
                else:
                    if bottom_player.rect.x < 300:
                        action = 'Right'
                    else:
                        action = 'Left'
                print("Top action", action)
                # HIT
                return ball.strike(top_player, action)
            
            # Did not hit the ball
            else:
                if top_player.rect.x > get_x_of_ball(ball, top_player):
                    action = 'Left'                
                elif top_player.rect.x < get_x_of_ball(ball, top_player):
                    action = 'Right'
                else:
                    action = 'Stay'
                print("Top action", action)
                top_player.update(action)
                return None
        
        # Top's turn to play          
        else:
            action = 'Stay'
            # Does nothing
            top_player.update(action)
            return None
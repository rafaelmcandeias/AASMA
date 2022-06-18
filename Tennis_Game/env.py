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

LIMIT_LEFT_NET  = 175
LIMIT_RIGHT_NET  = 525

LIMIT_TOP_FIELD = 78
LIMIT_BOT_FIELD = 571

LIMIT_TOP_NET = 320
LIMIT_BOTTOM_NET  = 330
MIDDLE_X = LIMIT_LEFT_NET + ((LIMIT_RIGHT_NET - LIMIT_LEFT_NET) / 2) - 40
MIDDLE_Y_TOP = LIMIT_TOP_FIELD + ((LIMIT_TOP_NET - LIMIT_TOP_FIELD) / 2) - 40
MIDDLE_Y_BOT = LIMIT_BOTTOM_NET + ((LIMIT_BOT_FIELD - LIMIT_BOTTOM_NET) / 2) - 40

# ---------------------------------------------------------------------------

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
            # HIT
            return ball.strike(bottom_player, action)
        
        else:
            action = get_movement()[np.random.choice(tuple(get_movement().keys()))]
            bottom_player.update(action)
            return None


    # Walks to ball x
    if mode == "beginner":
        # Bottom player turn
        if player_to_strike == bottom_player:
            # Bottom player hits the ball
            if ball.rect.colliderect(bottom_player):
                action = get_stroke_direction()[np.random.choice(list(get_stroke_direction().keys()))]
                # HIT
                return ball.strike(bottom_player, action)
           
            else:
                if bottom_player.rect.x > get_x_of_ball(ball, bottom_player):
                    action = 'Left'                
                elif bottom_player.rect.x < get_x_of_ball(ball, bottom_player):
                    action = 'Right'
                else:
                    action = 'Stay'
                bottom_player.update(action)
                # None
                return None

        # Not its turn to hit the ball
        else:
            action = 'Stay'
            bottom_player.update(action)
            # None
            return None


    # Goes to the ball and knows where it should send it.
    # Does not waste stamina for balls going OFB
    if mode == "expert":
        action = None
        # Bottom's turn to strike
        if player_to_strike == bottom_player:
            
            # Player stroke
            if ball.rect.colliderect(bottom_player):
                # gets the other player place on the court
                if (top_player.rect.x > 300 and bottom_player.rect.x < 225) or (top_player.rect.x < 300 and bottom_player.rect.x > 475):
                    action = 'Straight'
                else:
                    if top_player.rect.x < 300:
                        action = 'Right'
                    else:
                        action = 'Left'

                # HIT
                return ball.strike(bottom_player, action)
            
            # Did not hit the ball
            else:
                # Ball might hit the ground Outside Of Bounds
                # It is wise to save stamina
                if ball.ground == 0:
                    # Is outside of x field
                    if ball.rect.x < LIMIT_LEFT_NET or ball.rect.x > LIMIT_RIGHT_NET:
                        action = 'Stay'
        
                    # Is outside of y field
                    elif ball.rect.y > LIMIT_BOT_FIELD:
                        action = 'Stay'
        
                
                # Ball inside limits
                if action == None:
                    # Will move sideways because
                    # player's X is further away than player's y to ball
                    # OR cant go pass the net -> irrelevant moving on y 
                    if (bottom_player.rect.y == LIMIT_BOTTOM_NET and ball.rect.y <= LIMIT_BOTTOM_NET) or (abs(bottom_player.rect.x - ball.rect.x) >= abs(bottom_player.rect.y - ball.rect.y)):
                        if bottom_player.rect.x < ball.rect.x:
                            action = 'Right'
                        elif bottom_player.rect.x > ball.rect.x:
                            action = 'Left'
                        else:
                            action = 'Stay'

                    # Will move frontways if ball passed the net
                    elif ball.rect.y > LIMIT_BOTTOM_NET:
                        if bottom_player.rect.y < ball.rect.y:
                            action = 'Down' 
                        elif bottom_player.rect.y > ball.rect.y:
                            action = 'Up'
                        else:
                            action = 'Stay'
                

                bottom_player.update(action)
                return None
        
        # Top's turn to play          
        else:
            action = 'Stay'
            # Does nothing
            bottom_player.update(action)
            return None
    

    # Goes to the ball and knows where it should send it.
    # Does not waste stamina for balls going OFB
    # Walks to middle of field for repositioning
    if mode == "pro":
        action = None
        # Bottom's turn to strike
        if player_to_strike == bottom_player:
            
            # Player stroke
            if ball.rect.colliderect(bottom_player):
                # gets the other player place on the court
                if (top_player.rect.x > 300 and bottom_player.rect.x < 225) or (top_player.rect.x < 300 and bottom_player.rect.x > 475):
                    action = 'Straight'
                else:
                    if top_player.rect.x < 300:
                        action = 'Right'
                    else:
                        action = 'Left'

                # HIT
                return ball.strike(bottom_player, action)
            
            # Did not hit the ball
            else:
                 # Ball might hit the ground Outside Of Bounds
                # It is wise to save stamina
                if ball.ground == 0:
                    # Is outside of x field
                    if ball.rect.x < LIMIT_LEFT_NET or ball.rect.x > LIMIT_RIGHT_NET:
                        action = 'Stay'
        
                    # Is outside of y field
                    elif ball.rect.y > LIMIT_BOT_FIELD:
                        action = 'Stay'
        
                
                # Ball inside limits
                if action == None:
                    # Will move sideways because
                    # player's X is further away than player's y to ball
                    # OR cant go pass the net -> irrelevant moving on y 
                    if (bottom_player.rect.y == LIMIT_BOTTOM_NET and ball.rect.y <= LIMIT_BOTTOM_NET) or (abs(bottom_player.rect.x - ball.rect.x) >= abs(bottom_player.rect.y - ball.rect.y)):
                        if bottom_player.rect.x < ball.rect.x:
                            action = 'Right'
                        elif bottom_player.rect.x > ball.rect.x:
                            action = 'Left'
                        else:
                            action = 'Stay'

                    # Will move frontways if ball passed the net
                    elif ball.rect.y > LIMIT_BOTTOM_NET:
                        if bottom_player.rect.y < ball.rect.y:
                            action = 'Down' 
                        elif bottom_player.rect.y > ball.rect.y:
                            action = 'Up'
                        else:
                            action = 'Stay'
                

                bottom_player.update(action)
                return None
        
        # Top's turn to play          
        else:
            # Bot x not in x middle interval
            if not (MIDDLE_X - 5 <= bottom_player.rect.x <= MIDDLE_X + 5):
                # It is left from interval
                if bottom_player.rect.x < MIDDLE_X - 5:
                    action = 'Right'
                # It is right from interval
                elif bottom_player.rect.x > MIDDLE_X + 5:
                    action = 'Left'
            
            # Bot x in correct place but y not in interval
            elif not (MIDDLE_Y_BOT - 5 <= bottom_player.rect.y <= MIDDLE_Y_BOT + 5):
                # It is up from interval
                if bottom_player.rect.y < MIDDLE_Y_BOT:
                    action = 'Down'
                # it is down from interval
                elif bottom_player.rect.y > MIDDLE_Y_BOT:
                    action = 'Up'
            
            bottom_player.update(action)
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
            return None
    

    # Walks to ball x and sends randomly
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
                top_player.update(action)
                return None

        # Not its turn to hit the ball
        else:
            action = 'Stay'
            top_player.update(action)
            return None


    # Goes to the ball and knows where it should send it.
    # Does not waste stamina for balls going OFB
    if mode == "expert":
        action = None
        # Top's turn to strike
        if player_to_strike == top_player:
            
            # Player stroke
            if ball.rect.colliderect(top_player):
                # gets the other player place on the court
                if (bottom_player.rect.x > 300 and top_player.rect.x < 225) or (bottom_player.rect.x < 300 and top_player.rect.x > 475):
                    action = 'Straight'
                else:
                    if bottom_player.rect.x < 300:
                        action = 'Right'
                    else:
                        action = 'Left'

                # HIT
                return ball.strike(top_player, action)
            
            # Did not hit the ball
            else:
                # Ball might hit the ground Outside Of Bounds
                # It is wise to save stamina
                if ball.ground == 0:
                    # Is outside of x field
                    if ball.rect.x < LIMIT_LEFT_NET or ball.rect.x > LIMIT_RIGHT_NET:
                        action = 'Stay'
        
                    # Is outside of y field
                    elif ball.rect.y < LIMIT_TOP_FIELD:
                        action = 'Stay'
        
                
                # Ball inside limits
                if action == None:
                    # Will move sideways because
                    # player's X is further away than player's y to ball
                    # OR cant go pass the net -> irrelevant moving on y 
                    if (top_player.rect.y == LIMIT_TOP_NET and ball.rect.y >= LIMIT_TOP_NET) or (abs(top_player.rect.x - ball.rect.x) >= abs(top_player.rect.y - ball.rect.y)):
                        if top_player.rect.x < ball.rect.x:
                            action = 'Right'
                        elif top_player.rect.x > ball.rect.x:
                            action = 'Left'
                        else:
                            action = 'Stay'
                    
                    # Will move Y if ball passed the net
                    elif ball.rect.y < LIMIT_TOP_NET:
                        if top_player.rect.y < ball.rect.y:
                            action = 'Down' 
                        elif top_player.rect.y > ball.rect.y:
                            action = 'Up'
                        else:
                            action = 'Stay'
                

                top_player.update(action)
                return None
        
        # Bottom's turn to play          
        else:
            action = 'Stay'
            # Does nothing
            top_player.update(action)
            return None
    

    # Goes to the ball and knows where it should send it.
    # Does not waste stamina for balls going OFB
    if mode == "pro":
        action = None
        # Top's turn to strike
        if player_to_strike == top_player:
            
            # Player stroke
            if ball.rect.colliderect(top_player):
                # gets the other player place on the court
                if (bottom_player.rect.x > 300 and top_player.rect.x < 225) or (bottom_player.rect.x < 300 and top_player.rect.x > 475):
                    action = 'Straight'
                else:
                    if bottom_player.rect.x < 300:
                        action = 'Right'
                    else:
                        action = 'Left'

                # HIT
                return ball.strike(top_player, action)
            
            # Did not hit the ball
            else:
                # Ball might hit the ground Outside Of Bounds
                # It is wise to save stamina
                if ball.ground == 0:
                    # Is outside of x field
                    if (top_player.rect.y == LIMIT_TOP_NET and ball.rect.y >= LIMIT_TOP_NET) or ball.rect.x > LIMIT_RIGHT_NET:
                        action = 'Stay'
        
                    # Is outside of y field
                    elif ball.rect.y < LIMIT_TOP_FIELD:
                        action = 'Stay'
        
                
                # Ball inside limits
                if action == None:
                    # Will move sideways because
                    # player's X is further away than player's y to ball
                    # OR cant go pass the net -> irrelevant moving on y 
                    if ball.rect.y >= LIMIT_TOP_NET or (abs(top_player.rect.x - ball.rect.x) >= abs(top_player.rect.y - ball.rect.y)):
                        if top_player.rect.x < ball.rect.x:
                            action = 'Right'
                        elif top_player.rect.x > ball.rect.x:
                            action = 'Left'
                        else:
                            action = 'Stay'
                    
                    # Will move Y if ball passed the net
                    elif ball.rect.y < LIMIT_TOP_NET:
                        if top_player.rect.y < ball.rect.y:
                            action = 'Down' 
                        elif top_player.rect.y > ball.rect.y:
                            action = 'Up'
                        else:
                            action = 'Stay'
                

                top_player.update(action)
                return None
        
        # Bottom's turn to play          
        else:
            # Top x not in x middle interval
            if not (MIDDLE_X - 5 <= top_player.rect.x <= MIDDLE_X + 5):
                # It is left from interval
                if top_player.rect.x < MIDDLE_X - 5:
                    action = 'Right'
                # It is right from interval
                elif top_player.rect.x > MIDDLE_X + 5:
                    action = 'Left'
            
            # Top x in correct place but y not in interval
            elif not (MIDDLE_Y_TOP - 5 <= top_player.rect.y <= MIDDLE_Y_TOP + 5):
                # It is up from interval
                if top_player.rect.y < MIDDLE_Y_TOP:
                    action = 'Down'
                # it is down from interval
                elif top_player.rect.y > MIDDLE_Y_TOP:
                    action = 'Up'
                
            top_player.update(action)
            return None
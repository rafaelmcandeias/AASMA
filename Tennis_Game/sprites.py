import pygame
import images
import numpy as np
import numpy.random as rnd

# ------------------------------------------------------------

# Vars to limit the field size
LIMIT_LEFT = LIMIT_TOP = 0
LIMIT_TOP_NET = 255
LIMIT_BOTTOM_NET  = 300
LIMIT_BOT = 587
LIMIT_RIGHT = 648

# Vars for starting positions
BOTTOM_POS = (442, 524)
TOP_POS = (202, 40)

# Vars to declare zones in the field
LEFT_FIELD = (175, 274.999)
MIDDLE_FIELD = (275, 474.999)
RIGHT_FIELD = (475, 575)

# ------------------------------------------------------------

# Player Class Super class for top and bottom players
class Player(pygame.sprite.Sprite):

    def __init__(self, speed, force, stamina, image):
        pygame.sprite.Sprite.__init__(self)
        # Image for the agent
        self.image = image
        # Used for hit boxing. An agent is a rectangule in pixels
        self.rect = image.get_rect()
        # Agent's speed through x
        self.speedx = speed
        # Agent's speed through y
        self.speedy = speed
        # Agent's force apllied to the ball
        self.force = force
        # Agent's amount of energy that can be used
        self.stamina = stamina


# Class for Top player
class Top_player(Player):

    def __init__(self, speed, forcex, forcey):
        super().__init__(speed, forcex, forcey, images.camden)
        # Position the image -> agent
        self.rect.center = TOP_POS
    
    # Function to update a player's position
    def update(self):
        # Get key pressed
        keyState = pygame.key.get_pressed()

        # Left arrow
        if keyState[pygame.K_a] and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx
        # Right arrow
        if keyState[pygame.K_d] and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx
        # Up arrow
        if keyState[pygame.K_w] and self.rect.y > LIMIT_TOP:
            self.rect.y -= self.speedy
        # Down arrow
        if keyState[pygame.K_s] and self.rect.y < LIMIT_TOP_NET:
            self.rect.y += self.speedy   


# Class for Top player
class Bottom_player(Player):

    def __init__(self, speed, forcex, forcey):
        # Initializes Bottom Agent with it's pos, speed and image
        super().__init__(speed, forcex, forcey, images.robert)
        # Position the image -> agent
        self.rect.center = BOTTOM_POS
    
    # Function to update a player's position
    def update(self):
        # Get key pressed
        keyState = pygame.key.get_pressed()

        # Left arrow
        if keyState[pygame.K_LEFT] and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx
        # Right arrow
        if keyState[pygame.K_RIGHT] and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx
        # Up arrow
        if keyState[pygame.K_UP] and self.rect.y > LIMIT_BOTTOM_NET:
            self.rect.y -= self.speedy
        # Down arrow
        if keyState[pygame.K_DOWN] and self.rect.y < LIMIT_BOT:
            self.rect.y += self.speedy


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tennisBall.png")
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 0
        self.serve_flag = True
    
    def get_stroke_speed(self, keyState, player):
    # bottom players stroke
        if isinstance(player, Bottom_player):
            # region 1 of the court
            speedy = -player.force
            if LEFT_FIELD[0] <= self.rect.x <= LEFT_FIELD[1]:
                if keyState[pygame.K_n]:
                    return (-rnd.uniform(0,1), speedy)
                elif keyState[pygame.K_m]:
                    return (rnd.uniform(4,6), speedy)
                else:
                    return (0, speedy)
            # region 2 of the court
            if MIDDLE_FIELD[0] <= self.rect.x <= MIDDLE_FIELD[1]:
                if keyState[pygame.K_n]:
                    return (-rnd.uniform(2,3), speedy)
                elif keyState[pygame.K_m]:
                    return (rnd.uniform(2,3), speedy)
                else:
                    return (0, speedy)
            # region 3 of the court
            if RIGHT_FIELD[0] <= self.rect.x <= RIGHT_FIELD[1]:
                if keyState[pygame.K_n]:
                    return (-rnd.uniform(4,6), speedy)
                elif keyState[pygame.K_m]:
                    return (rnd.uniform(0,1), speedy)
                else:
                    return (0, speedy)
        
        # top players stroke
        else:
            speedy = player.force
            if LEFT_FIELD[0] <= self.rect.x < 275:
                if keyState[pygame.K_r]:
                    return (-rnd.uniform(0,1), speedy)
                elif keyState[pygame.K_t]:
                    return (rnd.uniform(4,6), speedy)
                else:
                    return (0, speedy)
            # region 2 of the court
            if MIDDLE_FIELD[0] <= self.rect.x <= MIDDLE_FIELD[1]:
                if keyState[pygame.K_r]:
                    return (-rnd.uniform(2,3), speedy)
                elif keyState[pygame.K_t]:
                    return (rnd.uniform(2,3), speedy)
                else:
                    return (0, speedy)
            # region 3 of the court
            if RIGHT_FIELD[0] <= self.rect.x <= RIGHT_FIELD[1]:
                if keyState[pygame.K_r]:
                    return (-rnd.uniform(4,6), speedy)
                elif keyState[pygame.K_t]:
                    return (rnd.uniform(0,1), speedy)
                else:
                    return (0, speedy)

    def update(self, bottom_player, top_player):

        keyState = pygame.key.get_pressed()

        # check if point over and who won
        # the bottom side won
        if (self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y < LIMIT_TOP) or (not self.serve_flag and abs(self.speedy) < 0.5 and self.rect.y < LIMIT_BOTTOM_NET):
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            self.serve_flag = True
            return 1
        
        # top side won
        if (self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y > LIMIT_BOT) or (not self.serve_flag and abs(self.speedy) < 0.5 and self.rect.y > LIMIT_BOTTOM_NET):   
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            self.serve_flag = True
            return 2

        # checks if player served
        if (keyState[pygame.K_PERIOD] and bottom_player.rect.y > 520) or (keyState[pygame.K_TAB] and top_player.rect.y < 20):
            self.serve_flag = True
        
        # checks to see if ball has passed the net after player served
        if self.serve_flag:
            if 300 < self.rect.y < 350:
                self.serve_flag = False

        # bottom player serves
        if self.serve_flag and keyState[pygame.K_PERIOD]:
            bottom_player.image = images.robert_serve
            self.rect.center = (bottom_player.rect.x + 15, bottom_player.rect.y)
            self.speedy = -rnd.uniform(6,9)
            # serves to the left
            if bottom_player.rect.x < 350:
                self.speedx = rnd.uniform(2,5)
            # serves to the right
            else: 
                self.speedx = -rnd.uniform(2,5)
        
        # top player serves
        if self.serve_flag and keyState[pygame.K_TAB]:
            self.rect.center = (top_player.rect.x, top_player.rect.y + 40)
            top_player.image = images.camden_serve
            self.speedy = rnd.uniform(6,9)   
            #serves to the right
            if top_player.rect.x < 350:
                self.speedx = rnd.uniform(2,5)
            # serves to the left              
            else:
                self.speedx = -rnd.uniform(2,5)
        
        # bottom player hits the ball
        if self.rect.colliderect(bottom_player) and not self.serve_flag:
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            self.speedx, self.speedy = self.get_stroke_speed(keyState, bottom_player)
            # forehand animation
            if self.rect.colliderect(bottom_player) and self.rect.x > bottom_player.rect.x + 10:
                bottom_player.image = images.robert_forehand
            #backhand animation
            if self.rect.colliderect(bottom_player) and self.rect.x < bottom_player.rect.x - 10:
                bottom_player.image = images.robert_backhand
        
        # top player hits the ball
        if self.rect.colliderect(top_player) and not self.serve_flag:
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            self.speedx, self.speedy = self.get_stroke_speed(keyState, top_player)
            # forehand animation
            if self.rect.colliderect(top_player) and self.rect.x > top_player.rect.x + 10:
                top_player.image = images.camden_forehand
            #backhand animation
            if self.rect.colliderect(top_player) and self.rect.x < top_player.rect.x - 10:
                top_player.image = images.camden_backhand

        #Make the ball slow down
        self.speedy *=  0.99
        self.rect = self.rect.move(self.speedx, self.speedy)

        # say no one has won yet
        return 0

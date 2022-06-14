import pygame
import images
import numpy as np
import numpy.random as rnd
import random
from datetime import datetime

# ------------------------------------------------------------

# Vars to limit the field size
LIMIT_LEFT = LIMIT_TOP = 0
LIMIT_TOP_NET = 255
LIMIT_BOTTOM_NET  = 300
LIMIT_BOT = 587
LIMIT_RIGHT = 648

# Vars for starting positions
BOTTOM_POS = (450, 524)
TOP_POS = (300, 40)

# Vars to declare zones in the field
LEFT_FIELD = 0.99175
MIDDLE_FIELD = (275, 475)

# Vars to divide stamina status
# These divisions are universal.
# Different players can be in different fractions
NO_STAMINA = 0
LOW_STAMINA = 0.25
MID_STAMINA = 0.75
HIGH_STAMINA = 1

# Vars to define net height
NET_HEIGHT = 1.07

# Vars for physichs
AIR_RESISTANCE = 0.99
GRAVITY = 9.8

# ------------------------------------------------------------

# Player Class Super class for top and bottom players
class Player(pygame.sprite.Sprite):

    def __init__(self, name, speed, force, energy, image):
        pygame.sprite.Sprite.__init__(self)
        # Agent's identifier
        self.name = name
        # Image for the agent
        self.image = image
        # Used for hit boxing. An agent is a rectangule in pixels
        self.rect = image.get_rect()
        # Agent's speed through x
        self.speedx = speed
        # Agent's speed through y
        self.speedy = speed
        # Agent's max force
        self.force = force
        #  ]0, 1]
        if energy <= 0 or energy > 1:
            raise Exception("Invalid energy value")
        else:
            # Agent's energy value when started the game
            self.energy = energy
            # Agent's current amount of energy
            self.stamina = energy
    
    # Function to reduce amount of stamina given applied force
    def lose_stamina(self, force):
        self.stamina -= (force / self.force) * 0.005

    # Function that returns the force choosen.
    # Choosing a force depends on stamina
    def choose_force(self):
        force = self.force
        # Has no more stamina
        if self.stamina == NO_STAMINA:
            return NO_STAMINA

        # Below 25% of energy
        if self.stamina < LOW_STAMINA * self.energy:
            force *= random.uniform(0.1, LOW_STAMINA)

        # Below of 75% of energy
        elif self.stamina < MID_STAMINA * self.energy:
            force *= random.uniform(LOW_STAMINA, MID_STAMINA)

        # Below 100% of energy
        elif self.stamina < HIGH_STAMINA * self.energy:
            force *= random.uniform(MID_STAMINA, HIGH_STAMINA)
        
        self.lose_stamina(force)
        return force
        

# Class for Top player
class Top_player(Player):

    def __init__(self, info):
        super().__init__(info[0], info[1], info[2], info[3], images.camden)
        # Position the image -> agent
        self.rect.center = TOP_POS
    
    # Function to update a player's position
    def update(self, action):
        # Get key pressed
        keyState = pygame.key.get_pressed()
        pressed = False

        # Left
        if action == 'Left' and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx * (self.stamina / self.energy)
            pressed = True
        # Right
        if action == 'Right' and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Up
        if action == 'Up' and self.rect.y > LIMIT_TOP:
            self.rect.y -= self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Down
        if action == 'Down' and self.rect.y < LIMIT_TOP_NET:
            self.rect.y += self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Stay
        if action == 'Saty':
            # Do nothing
            pass    

# Class for Top player
class Bottom_player(Player):

    def __init__(self, info):
        # Initializes Bottom Agent with it's pos, speed and image
        super().__init__(info[0], info[1], info[2], info[3], images.robert)
        # Position the image -> agent
        self.rect.center = BOTTOM_POS
    
    # Function to update a player's position
    def update(self, action):
        # Get key pressed
        keyState = pygame.key.get_pressed()
        pressed = False

        # New rec pos adds the amount of speed * the percentage of energy still has
        # Left
        if action == 'Left' and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx * (self.stamina / self.energy)
            pressed = True
            self.stamina *= 0.9999999999
        # Right
        if action == 'Right' and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Up
        if action == 'Up' and self.rect.y > LIMIT_BOTTOM_NET:
            self.rect.y -= self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Down
        if action == 'Down' and self.rect.y < LIMIT_BOT:
            self.rect.y += self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Stay
        if action == 'Saty':
            # Do nothing
            pass 


# Ball class
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tennisBall.png")
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 0
        #self.speedz = 0
        # Ball height.
        #self.z = NET_HEIGHT
    

    def get_stroke_speed(self, player, action):
        
        speedx = 0
        speedy = 0

        # bottom players stroke
        if isinstance(player, Bottom_player):
            # region 1 of the court
            if LEFT_FIELD <= self.rect.x < MIDDLE_FIELD[0]:
                if action == 'Left':
                    speedx = -rnd.uniform(0,1)
                elif action == 'Right':
                    speedx = rnd.uniform(3,4)
                elif action == 'Straight':
                    speedx = 0
            
            # region 2 of the court
            elif MIDDLE_FIELD[0] <= self.rect.x < MIDDLE_FIELD[1]:
                if action == 'Left':
                    speedx = -rnd.uniform(1,2)
                elif action == 'Right':
                    speedx = rnd.uniform(1,2)
                elif action == 'Straight':
                    speedx = 0
            
            # region 3 of the court
            else:
                if action == 'Left':
                    speedx = -rnd.uniform(3,4)
                elif action == 'Right':
                    speedx = rnd.uniform(0,1)
                elif action == 'Straight':
                    speedx = 0

        
        # top players stroke
        elif isinstance(player, Top_player):
            if LEFT_FIELD <= self.rect.x < MIDDLE_FIELD[0]:
                if action == 'Left':
                    speedx = -rnd.uniform(0,1)
                elif action == 'Right':
                    speedx = rnd.uniform(3,4)
                elif action == 'Straight':
                    speedx = 0

            # region 2 of the court
            elif MIDDLE_FIELD[0] <= self.rect.x < MIDDLE_FIELD[1]:
                if action == 'Left':
                    speedx = -rnd.uniform(1,2)
                elif action == 'Right':
                    speedx = rnd.uniform(1,2)
                elif action == 'Straight':
                    speedx = 0
            
            # region 3 of the court
            else:
                if action == 'Left':
                    speedx = -rnd.uniform(3,4)
                elif action == 'Right':
                    speedx = rnd.uniform(0,1)
                elif action == 'Straight':
                    speedx = 0
            
        speedy = speedy = abs(player.choose_force()) * rnd.uniform(0.75, 0.95)
        if isinstance(player, Bottom_player):
            speedy = -speedy

        return (speedx, speedy)

    # Updates ball movement
    def update(self, serve_flag, player, action='None'):
        start = datetime.now()
        keyState = pygame.key.get_pressed()

        # check if point over and who won
        # the bottom side won
        if (self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y < LIMIT_TOP) or (not serve_flag and abs(self.speedy) < 0.7 and self.rect.y < LIMIT_BOTTOM_NET) or (self.rect.y == 350 and (self.rect.x > 525 or self.rect.x < 175) and self.speedy > 0):
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            return 1
        
        # top side won
        if (self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y > LIMIT_BOT) or (not serve_flag and abs(self.speedy) < 0.7 and self.rect.y > LIMIT_BOTTOM_NET) or (self.rect.y == 350 and (self.rect.x > 525 or self.rect.x < 175) and self.speedy < 0):   
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            return 2

        # player hits the ball        
        if action != 'None':
            if action != 'Top Serve' and action != 'Bottom Serve':
                self.speedx, self.speedy = self.get_stroke_speed(player, action)
            else:
                if action == 'Bottom Serve':
                    self.rect.center = (BOTTOM_POS[0], BOTTOM_POS[1] - 100)
                    if player.rect.x < 350:
                        self.speedx = rnd.uniform(1,3)
                    else:
                        self.speedx = -rnd.uniform(1,3)
                    self.speedy = -8
                if action == 'Top Serve':
                    self.rect.center = (TOP_POS[0], TOP_POS[1] + 100)
                    if player.rect.x < 350:
                        self.speedx = rnd.uniform(1,3)           
                    else:
                        self.speedx = -rnd.uniform(1,3)
                    self.speedy = 8 
            
        elif action == 'None':
            # Calculate time 
            #end = datetime.now()
            #time = end - start
            #seconds = time.total_seconds()
            #Make the ball slow down
            self.speedy *= AIR_RESISTANCE
            #self.z += (self.speedz * seconds) - ((GRAVITY/2) * (seconds**2))
        self.rect = self.rect.move(self.speedx, self.speedy)

        # say no one has won yet
        return 0
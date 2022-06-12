import pygame
import images
import numpy as np
import numpy.random as rnd
import random

# ------------------------------------------------------------

# Vars to limit the field size
LIMIT_LEFT = LIMIT_TOP = 0
LIMIT_TOP_NET = 255
LIMIT_BOTTOM_NET  = 300
LIMIT_BOT = 587
LIMIT_RIGHT = 648
# Vars to declare zones in the field
LEFT_FIELD = 0.99175
MIDDLE_FIELD = (275, 475)

# Vars for starting positions
BOTTOM_POS = (442, 524)
TOP_POS = (202, 40)
# Vars for point winners
BOT_WON = 1
TOP_WON = 2
HIT = 3

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
GRAVITY = 9.8e-6
# Assume constant time passes between frames in milliseconds
TIME = 2.9

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
    def update(self):
        # Get key pressed
        keyState = pygame.key.get_pressed()
        pressed = False

        # Left arrow
        if keyState[pygame.K_a] and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx * (self.stamina / self.energy)
            pressed = True
        # Right arrow
        if keyState[pygame.K_d] and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Up arrow
        if keyState[pygame.K_w] and self.rect.y > LIMIT_TOP:
            self.rect.y -= self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Down arrow
        if keyState[pygame.K_s] and self.rect.y < LIMIT_TOP_NET:
            self.rect.y += self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
    
    # Puts agent in starting position
    def restart_position(self):
        self.rect.x = TOP_POS[0]
        self.rect.y = TOP_POS[1]


# Class for Top player
class Bottom_player(Player):

    def __init__(self, info):
        # Initializes Bottom Agent with it's pos, speed and image
        super().__init__(info[0], info[1], info[2], info[3], images.robert)
        # Position the image -> agent
        self.rect.center = BOTTOM_POS
    
    # Function to update a player's position
    def update(self):
        # Get key pressed
        keyState = pygame.key.get_pressed()
        pressed = False

        # New rec pos adds the amount of speed * the percentage of energy still has
        # Left arrow
        if keyState[pygame.K_LEFT] and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx * (self.stamina / self.energy)
            pressed = True
            self.stamina *= 0.9999999999
        # Right arrow
        if keyState[pygame.K_RIGHT] and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Up arrow
        if keyState[pygame.K_UP] and self.rect.y > LIMIT_BOTTOM_NET:
            self.rect.y -= self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Down arrow
        if keyState[pygame.K_DOWN] and self.rect.y < LIMIT_BOT:
            self.rect.y += self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
    
    # Puts agent in starting position
    def restart_position(self):
        self.rect.x = BOTTOM_POS[0]
        self.rect.y = BOTTOM_POS[1]


# Ball class
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tennisBall.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(TOP_POS[0] - 30, TOP_POS[1] + 10)
        self.speedx = 0
        self.speedy = 0
        self.speedz = 0
        # Ball height.
        self.z = NET_HEIGHT

    # Method to place ball next to server
    def restart_position(self, server):
        if isinstance(server, Top_player):
            self.rect = self.rect.move(TOP_POS[0] - 30, TOP_POS[1] + 10)
        else:
            self.rect = self.rect.move(BOTTOM_POS[0] + 10, BOTTOM_POS[1] + 10)
    
    def get_stroke_speed(self, keyState, player):
    # bottom players stroke
        if isinstance(player, Bottom_player):
            # region 1 of the court
            if LEFT_FIELD <= self.rect.x < MIDDLE_FIELD[0]:
                if keyState[pygame.K_n]:
                    speedx = -rnd.uniform(0,1)
                elif keyState[pygame.K_m]:
                    speedx = rnd.uniform(4,6)
                else:
                    speedx = rnd.uniform(0, 0.5)
            
            # region 2 of the court
            elif MIDDLE_FIELD[0] <= self.rect.x < MIDDLE_FIELD[1]:
                if keyState[pygame.K_n]:
                    speedx = -rnd.uniform(2,3)
                elif keyState[pygame.K_m]:
                    speedx = rnd.uniform(2,3)
                else:
                    speedx = rnd.uniform(-0.5, 0.5)
            
            # region 3 of the court
            else:
                if keyState[pygame.K_n]:
                    speedx = -rnd.uniform(4,6)
                elif keyState[pygame.K_m]:
                    speedx = rnd.uniform(0,1)
                else:
                    speedx = rnd.uniform(-0.5, 0)

            force = -player.choose_force()
        
        # top players stroke
        else:
            if LEFT_FIELD <= self.rect.x < MIDDLE_FIELD[0]:
                if keyState[pygame.K_r]:
                    speedx = -rnd.uniform(0,1)
                elif keyState[pygame.K_t]:
                    speedx = rnd.uniform(4,6)
                else:
                    speedx = rnd.uniform(0, 0.5)

            # region 2 of the court
            elif MIDDLE_FIELD[0] <= self.rect.x < MIDDLE_FIELD[1]:
                if keyState[pygame.K_r]:
                    speedx = -rnd.uniform(2,3)
                elif keyState[pygame.K_t]:
                    speedx = rnd.uniform(2,3)
                else:
                    speedx = rnd.uniform(-0.5, 0.5)
            
            # region 3 of the court
            else:
                if keyState[pygame.K_r]:
                    speedx = -rnd.uniform(4,6)
                elif keyState[pygame.K_t]:
                    speedx = rnd.uniform(0,1)
                else:
                    speedx = rnd.uniform(-0.5, 0)
            
            force = player.choose_force()
        
        speedy = (abs(force) - abs(speedx)) * rnd.uniform(0.75, 0.95)
        if isinstance(player, Bottom_player):
            speedy = -speedy
        speedz = abs(force) - abs(speedx) - abs(speedy)
        return (speedx, speedy, speedz)


    # Method to update the ball position
    def update_position(self):
        # Updates the ball position
        posx, posy = 0, 0

        # Movement requires update only if it is not stopped
        if self.speedx != 0:
            self.speedx *= AIR_RESISTANCE
            posx += self.speedx * TIME
        
        # Updates posy ball
        if self.speedy != 0:
            self.speedy *= AIR_RESISTANCE            
            posy += self.speedy * TIME 
        
        # Updates posz ball
        # Gravity is always reducing z
        if self.speedz != 0 and self.z > 0:
            self.speedz -= (GRAVITY/2) * (TIME**2)
            self.z += self.speedz * TIME

        # Updates rect only if it is moving
        if self.speedx != 0 or self.speedy != 0:
            print("SPEED2:", self.speedx, self.speedy, self.speedz)
            print("POS:", posx, posy, self.z)
            self.rect = self.rect.move(posx, posy)


    # Method to make a service
    def serve(self, server):
        keyState = pygame.key.get_pressed()
        
        # Waits for serve command
        if (isinstance(server, Bottom_player) and keyState[pygame.K_PERIOD]) or (isinstance(server, Top_player) and keyState[pygame.K_TAB]):
            # Top player pressed its serving button
            if keyState[pygame.K_TAB]:
                server.image = images.camden_serve
            else:
                server.image = images.robert_serve
            
            if isinstance(server, Top_player):
                self.speedx = rnd.uniform(1.5, 2.25)
            else:
                self.speedx = rnd.uniform(-2.25, -1.5)
            
            force = server.choose_force()
            print("FORCE", force)
            self.speedy = (abs(force) - abs(self.speedx)) * 0.85
            if isinstance(server, Bottom_player):
                self.speedy = -self.speedy
            self.speedz = abs(force) - abs(self.speedx) - abs(self.speedy)
            print("SPEED:", self.speedx, self.speedy, self.speedz)
            
            self.update_position()
            return 1
        
        return 0


    # Updates ball movement
    def update(self, player_to_strike):
        keyState = pygame.key.get_pressed()

        # check if point over and who won
        # the bottom side won
        if (self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y < LIMIT_TOP) or (abs(self.speedy) < 0.5 and self.rect.y < LIMIT_BOTTOM_NET):
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            return BOT_WON
        
        # top side won
        if (self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y > LIMIT_BOT) or (abs(self.speedy) < 0.5 and self.rect.y > LIMIT_BOTTOM_NET):   
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            return TOP_WON
        
        # Player to strike hits the ball
        if self.rect.colliderect(player_to_strike):
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            # Reset ball's height
            self.z = NET_HEIGHT
            # Get ball speeds
            self.speedx, self.speedy, self.speedz = self.get_stroke_speed(keyState, player_to_strike)
            
            # Get the correct image
            if isinstance(player_to_strike, Bottom_player):
                image_forehand = images.robert_forehand
                image_backhand = images.robert_backhand
            else:
                image_forehand = images.camden_forehand
                image_backhand = images.camden_backhand
            
            # forehand animation
            if self.rect.x > player_to_strike.rect.x + 10:
                player_to_strike.image = image_forehand
            #backhand animation
            elif self.rect.x < player_to_strike.rect.x - 10:
                player_to_strike.image = image_backhand

            self.update_position()
                
            # To tell that the player stiked the ball
            return HIT

        # Updates ball position, given it's speed
        self.update_position()

        # say no one has won yet
        return 0
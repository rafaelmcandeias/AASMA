import pygame
import images
import numpy.random as rnd


# ------------------------------------------------------------

# Vars to limit the field size
LIMIT_LEFT = LIMIT_TOP = 0.99175
LIMIT_BOT = 587
LIMIT_RIGHT = 648

# Vars for net limits
LIMIT_TOP_NET = 320
LIMIT_BOTTOM_NET  = 330
LIMIT_LEFT_NET  = 175
LIMIT_RIGHT_NET  = 525

# Vars to declare zones in the field
LIMIT_TOP_FIELD = 78
LIMIT_BOT_FIELD = 571
LEFT_FIELD = 0.99175
CENTER_X = LIMIT_LEFT_NET + ((LIMIT_RIGHT_NET - LIMIT_LEFT_NET) / 2)
MIDDLE_FIELD = (CENTER_X - 50, CENTER_X + 50)

# Vars for starting positions
BOTTOM_POS = (450, 524)
TOP_POS = (200, 15)
# Vars for point winners
BOT_WON = 1
TOP_WON = 2
HIT = 3
FAULT = 4
POINT = 5

# Vars to divide stamina status
# These divisions are universal.
# Different players can be in different fractions
NO_STAMINA = 0
LOW_STAMINA = 0.25
MID_STAMINA = 0.75
HIGH_STAMINA = 1

# Vars to define net height
NET_HEIGHT = 0.2
HIT_HEIGHT = 1.5

# Vars for physichs m/s²
AIR_RESISTANCE = 0.99
GRAVITY = 9.8
# Assume constant time passes between frames in seconds
TIME = 16e-3

BLACK = (0, 0, 0)

# ------------------------------------------------------------

# Player Class Super class for top and bottom players
class Player(pygame.sprite.Sprite):

    def __init__(self, name, speed, force, energy, mode, image):
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
        # Agent's energy value when started the game
        self.energy = energy
        # Agent's current amount of energy
        self.stamina = energy
        # Agent's play strategy
        self.mode = mode

    
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
            force *= 0.5

        # Below of 75% of energy
        elif self.stamina < MID_STAMINA * self.energy:
            force *= 0.65

        # Below 100% of energy
        elif self.stamina < HIGH_STAMINA * self.energy:
            force *= 0.9
        
        self.lose_stamina(force)
        return force
    

    def control_force(self, ball, speedy, speedz):
        if LIMIT_TOP_NET - 150 <= self.rect.y <= LIMIT_BOTTOM_NET + 150:
            return speedz * 0.5
        return speedz
        

# Class for Top player
class Top_player(Player):

    def __init__(self, info):
        super().__init__(info[0], info[1], info[2], info[3], info[4], images.camden)
        # Position the image -> agent
        self.rect.center = TOP_POS
    
    # Function to update a player's position
    def update(self, action):
        # Get key pressed
        pressed = False

        # Left
        if action == 'Left' and self.rect.x > LIMIT_LEFT:
            self.rect.x -= self.speedx * (self.stamina / self.energy)
            pressed = True
        # Right
        elif action == 'Right' and self.rect.x < LIMIT_RIGHT:
            self.rect.x += self.speedx * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Up
        elif action == 'Up' and self.rect.y > LIMIT_TOP:
            self.rect.y -= self.speedy * (self.stamina / self.energy)
            if not pressed:
                self.stamina *= 0.9999999999
        # Down
        elif action == 'Down' and self.rect.y < LIMIT_TOP_NET:
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
        super().__init__(info[0], info[1], info[2], info[3], info[4], images.robert)
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
        self.z = HIT_HEIGHT
        # Number of bounces
        self.ground = 0

    # Method to place ball next to server
    def restart_position(self, server):
        if isinstance(server, Top_player):
            self.rect.x, self.rect.y = TOP_POS[0] - 30, TOP_POS[1] + 10
        else:
            self.rect.x, self.rect.y = BOTTOM_POS[0] + 10, BOTTOM_POS[1] + 10
    
    
    def get_stroke_speed(self, player, action):
    # bottom players stroke
        if LEFT_FIELD <= self.rect.x < MIDDLE_FIELD[0]:
            if action == 'Left':
                speedx = -rnd.uniform(0, 0.5)
            elif action == 'Right':
                speedx = rnd.uniform(1.75, 2)
            elif action == 'Straight':
                speedx = rnd.uniform(0.2, 0.5)

        # region 2 of the court
        elif MIDDLE_FIELD[0] <= self.rect.x < MIDDLE_FIELD[1]:
            if action == 'Left':
                speedx = -rnd.uniform(0.75, 1)
            elif action == 'Right':
                speedx = rnd.uniform(0.75, 1)
            elif action == 'Straight':
                speedx = rnd.uniform(-0.5, 0.5)
        
        # region 3 of the court
        else:
            if action == 'Left':
                speedx = -rnd.uniform(1.75, 2)
            elif action == 'Right':
                speedx = rnd.uniform(0.2, 0.5)
            elif action == 'Straight':
                speedx = rnd.uniform(-0.5, 0)
        
        force = player.choose_force()
        
        speedy = (abs(force) - abs(speedx)) * 0.7

        if isinstance(player, Bottom_player):
            speedy = -speedy
        speedz = (abs(force) - abs(speedx) - abs(speedy)) * 0.8
        
        if player.mode == "pro":
            speedz = player.control_force(self, speedy, speedz)
        
        return (speedx, speedy, speedz)


    # Method to update the ball position
    def update_position(self, screen):
        desloc_x, desloc_y = 0, 0

        # Movement requires update only if it is not stopped
        if self.speedx != 0:
            self.speedx -= (AIR_RESISTANCE/2) * (TIME**2)
            desloc_x += self.speedx * TIME * 100
        
        # Updates desloc_y ball
        if self.speedy != 0:
            self.speedy -= (AIR_RESISTANCE/2) * (TIME**2)        
            desloc_y += self.speedy * TIME * 100 
        
        # Updates posz ball
        # Gravity is always reducing z
        if self.z > 0:
            self.speedz -= (GRAVITY/2) * (TIME**2) * 40
            self.z += self.speedz * TIME
            if self.z < 0:
                self.z = 0
    
        # Ball left the board without touching the ground
        if self.z > 0 and self.ground == 0:
            # Top player hitted the ball
            if self.speedy > 0 and self.rect.y > LIMIT_BOT:
                    return FAULT
            # Bot player hitted the ball
            if self.speedy < 0 and self.rect.y < LIMIT_TOP:
                return FAULT
            # Ball left the x limits
            if self.rect.x <= LIMIT_LEFT or self.rect.x >= LIMIT_RIGHT:
                return FAULT

        # z <= 0 -> Bounce on the ground
        if self.z <= 0 and self.ground == 0:
            # Ball touched out of bounds x
            if (LEFT_FIELD <= self.rect.x <= LIMIT_LEFT_NET) or (LIMIT_RIGHT_NET <= self.rect.x <= LIMIT_RIGHT):
                return FAULT
            
            # Ball touched out of bounds y
            if self.rect.y < LIMIT_TOP_FIELD or self.rect.y > LIMIT_BOT_FIELD:
                return FAULT
            
            # Ball touched player's side first
            # Top player hitted the ball
            if self.speedy > 0 and self.rect.y < LIMIT_TOP_NET:
    
                return FAULT
            # Bot player hitted the ball
            if self.speedy < 0 and self.rect.y > LIMIT_BOTTOM_NET:
    
                return FAULT
    
            # Calculate rebounce
            self.speedx *= 0.66
            self.speedy *= 0.66
            self.speedz *= -0.66
            self.ground = 1
            self.speedz -= (GRAVITY/2) * (TIME**2)
            self.z += self.speedz * TIME

        # z <= 0 and Second bounce -> Point
        if self.z <= 0 and self.ground == 1:
            self.speedx, self.speedy, self.speedz = 0, 0, 0
            self.ground = 2
            return POINT
        
        if self.ground == 1:
            # Ball left x
            if self.rect.x <= LIMIT_LEFT or self.rect.x >= LIMIT_RIGHT:
                return POINT
            
            # Ball left Y
            if self.rect.y <= LIMIT_TOP or self.rect.y >= LIMIT_BOT:
                return POINT

        # Updates rect only if it is moving
        if self.speedx != 0 or self.speedy != 0:
            self.rect = self.rect.move(desloc_x, desloc_y)
            self.compute_shadow(screen)

        # Ball could not pass the net
        if (LIMIT_LEFT_NET <= self.rect.x <= LIMIT_RIGHT_NET) and (LIMIT_TOP_NET <= self.rect.y <= LIMIT_BOTTOM_NET) and self.z <= NET_HEIGHT:
            return FAULT
        
        return None


    # Method to put a shadow where the ball will land
    def compute_shadow(self, screen):
        if self.z == 0:
            radius = 1/0.1
        else:
            radius = 1/self.z * 2
        
        if radius > 5:
            radius = 5
        
        pygame.draw.circle(screen, BLACK, (self.rect.x + 3, self.rect.y + 3), radius)


    # Method to make a service
    def serve(self, server, screen):
        effect = pygame.mixer.Sound('tennisserve.wav')
        effect.play(0)

        self.z = HIT_HEIGHT
        if isinstance(server, Top_player):
            self.speedx = rnd.uniform(1.25, 1.5)
            server.image = images.camden_serve

        else:
            self.speedx = rnd.uniform(-1.5, -1.25)
            server.image = images.robert_serve
        
        force = server.choose_force()
        self.speedy = (abs(force) - abs(self.speedx)) * 0.9
        if isinstance(server, Bottom_player):
            self.speedy = -self.speedy
        self.speedz = abs(force) - abs(self.speedx) - abs(self.speedy)


        # Updates ball position, given it's speed
        self.update_position(screen)

        self.ground = 0


    # Method to see if there was a point score
    def scored_point(self, player_to_strike, hit):
        # Ball on net => Point for the one to strike
        if hit == FAULT:
            if isinstance(player_to_strike, Top_player):
                return TOP_WON
            return BOT_WON
        
        # Ball touched the ground twice => point for who stroke before
        if hit == POINT:
            if isinstance(player_to_strike, Top_player):
                return BOT_WON
            return TOP_WON

        # the bottom side won
        if self.rect.x > LIMIT_RIGHT or self.rect.x < LIMIT_LEFT or self.rect.y < LIMIT_TOP or self.rect.y > LIMIT_BOT:
            self.speedx = 0
            self.speedy = 0
            self.rect.x = 0
            self.rect.y = 0
            
            if self.ground >= 1:
                if isinstance(player_to_strike, Top_player):
                    return BOT_WON
                return TOP_WON
            
            if isinstance(player_to_strike, Top_player):
                return TOP_WON
            return BOT_WON
        
        # No one scored
        return 0


    # Updates ball movement when an agent hits the ball
    def strike(self, player_to_strike, action):
        effect = pygame.mixer.Sound('tennisserve.wav')
        effect.play(0)
        
        # Reset ball's height
        self.z = HIT_HEIGHT
        # Get ball speeds
        self.speedx, self.speedy, self.speedz = self.get_stroke_speed(player_to_strike, action)
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

        self.ground = 0

        return HIT
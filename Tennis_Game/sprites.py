import pygame
import images


# Vars to limit the field size
LIMIT_LEFT = LIMIT_TOP = 0
LIMIT_TOP_NET = 255
LIMIT_BOTTOM_NET  = 300
LIMIT_BOT = 587
LIMIT_RIGHT = 648


# Player Class Super class for top and bottom players
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, speedx, speedy, image):
        pygame.sprite.Sprite.__init__(self)
        # Image for the agent
        self.image = image
        # Used for hit boxing. An agent is a rectangule in pixels
        self.rect = image.get_rect()
        # Position the image -> agent
        self.rect.center = (x, y)
        # Agent's speed through x
        self.speedx = speedx
        # Agent's speed through y
        self.speedy = speedy


# Class for Top player
class Bottom_player(Player):

    def __init__(self, x, y, speedx, speedy):
        # Initializes Bottom Agent with it's pos, speed and image
        super().__init__(x, y, speedx, speedy, images.robert)
    
    # Function to move a player
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


# Class for Top player
class Top_player(Player):

    def __init__(self, x, y, speedx, speedy):
        super().__init__(x, y, speedx, speedy, images.camden)
    
    # Function to move a player
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


# Class for the tennis ball
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tennisBall.png")
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 0

    def update(self, top_player, bottom_player):
        #top_player's forehand
        if self.rect.colliderect(top_player) and self.rect.x > top_player.rect.x + 10:
            top_player.image = images.robert_forehand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            top_player.rect.y -5
            self.speedy = -13
            self.speedx = 3

        #top_player's backhand
        if self.rect.colliderect(top_player) and self.rect.x < top_player.rect.x - 10:
            top_player.image = images.robert_backhand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            top_player.rect.y -5
            self.speedy = -12
            self.speedx = -2

        #top_player's forehand volley
        if self.rect.colliderect(top_player) and self.rect.x > top_player.rect.x + 10 and 325 < top_player.rect.y < 450:
            top_player.image = images.robert_forehand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            top_player.rect.y -5
            self.speedy = -5

        #top_player's backhand volley
        if self.rect.colliderect(top_player) and self.rect.x < top_player.rect.x - 10 and 325 < top_player.rect.y < 450:
            top_player.image = images.robert_backhand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            top_player.rect.y -5
            self.speedy = -4.5

        #bottom_player's forehand
        if self.rect.colliderect(bottom_player) and self.rect.x < bottom_player.rect.x -10:
            bottom_player.image = images.camden_forehand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            bottom_player.rect.y -5
            self.speedy = 14
            self.speedx = 2

        #bottom_player's backhand
        if self.rect.colliderect(bottom_player) and self.rect.x > bottom_player.rect.x + 10:
            bottom_player.image = images.camden_backhand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            bottom_player.rect.y -5
            self.speedy = 13
            self.speedx = 2

        #bottom_player's forehand volley
        if self.rect.colliderect(bottom_player) and self.rect.x < bottom_player.rect.x -10 and 200 < bottom_player.rect.y < 325:
            bottom_player.image = images.camden_forehand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            bottom_player.rect.y -5
            self.speedy = 3.75

        #bottom_player's backhand volley
        if self.rect.colliderect(bottom_player) and self.rect.x > bottom_player.rect.x + 10 and 200 < bottom_player.rect.y < 325:
            bottom_player.image = images.camden_backhand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            bottom_player.rect.y -5
            self.speedy = 3.75

        keyState = pygame.key.get_pressed()

        #top_player's deuce side serve
        if keyState[pygame.K_PERIOD] and 350 < top_player.rect.x < 575 and top_player.rect.y > 449:
            top_player.image = images.robert_serve
            self.rect.center = (top_player.rect.x + 15, top_player.rect.y)
            self.speedx = -7
            self.speedy = -10

        #top_player's add side serve
        if keyState[pygame.K_PERIOD] and 175 < top_player.rect.x < 350 and top_player.rect.y > 449:
            top_player.image = images.robert_serve
            self.rect.center = (top_player.rect.x + 15, top_player.rect.y)
            self.speedx = 7
            self.speedy = -10

        #bottom_player's deuce side serve
        if keyState[pygame.K_TAB] and 175 < bottom_player.rect.x < 350 and bottom_player.rect.y < 78:
            bottom_player.image = images.camden_serve
            self.rect.center = (bottom_player.rect.x, bottom_player.rect.y + 40)
            self.speedx = 7
            self.speedy = 14

        #bottom_player's add side serve
        if keyState[pygame.K_TAB] and 350 < bottom_player.rect.x < 575 and bottom_player.rect.y < 78:
            bottom_player.image = images.camden_serve
            self.rect.center = (bottom_player.rect.x, bottom_player.rect.y + 40)
            self.speedx = -7
            self.speedy = 14

        #Make the ball slow down
        self.speedy = self.speedy * .98
        self.speedx = self.speedx * .98
        self.rect = self.rect.move(self.speedx, self.speedy)
import pygame
import images
import numpy as np
import numpy.random as rnd


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


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tennisBall.png")
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 0
    
    def get_stroke_speed(self, position, keyState):
    # bottom players stroke
        if position == "bottom":
            # region 1 of the court
            speedy = -rnd.uniform(5,8)
            if 175 <= self.rect.x < 275:
                if keyState[pygame.K_n]:
                    return (-rnd.uniform(0,1), speedy)
                elif keyState[pygame.K_m]:
                    return (rnd.uniform(2,4), speedy)
                else:
                    return (0, speedy)
            # region 2 of the court
            if 275 <= self.rect.x < 475:
                if keyState[pygame.K_n]:
                    return (-rnd.uniform(2,3), speedy)
                elif keyState[pygame.K_m]:
                    return (rnd.uniform(2,3), speedy)
                else:
                    return (0, speedy)
            # region 3 of the court
            if 475 <= self.rect.x <= 575:
                if keyState[pygame.K_n]:
                    return (-rnd.uniform(0,1), speedy)
                elif keyState[pygame.K_m]:
                    return (rnd.uniform(2,4), speedy)
                else:
                    return (0, speedy)
        
        # top players stroke
        else:
            speedy = rnd.uniform(5,8)
            if 175 <= self.rect.x < 275:
                if keyState[pygame.K_r]:
                    return (-rnd.uniform(0,1), speedy)
                elif keyState[pygame.K_t]:
                    return (rnd.uniform(2,4), speedy)
                else:
                    return (0, speedy)
            # region 2 of the court
            if 275 <= self.rect.x < 475:
                if keyState[pygame.K_r]:
                    return (-rnd.uniform(2,3), speedy)
                elif keyState[pygame.K_t]:
                    return (rnd.uniform(2,3), speedy)
                else:
                    return (0, speedy)
            # region 3 of the court
            if 475 <= self.rect.x <= 575:
                if keyState[pygame.K_r]:
                    return (-rnd.uniform(2,4), speedy)
                elif keyState[pygame.K_t]:
                    return (rnd.uniform(0,1), speedy)
                else:
                    return (0, speedy)

    def update(self, bottom_player, top_player):
        
        keyState = pygame.key.get_pressed()

        # bottom player hits the ball
        if self.rect.colliderect(bottom_player):
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            self.speedx, self.speedy = self.get_stroke_speed("bottom", keyState)
            # forehand animation
            if self.rect.colliderect(bottom_player) and self.rect.x > bottom_player.rect.x + 10:
                bottom_player.image = images.robert_forehand
            #backhand animation
            elif self.rect.colliderect(bottom_player) and self.rect.x < bottom_player.rect.x - 10:
                bottom_player.image = images.robert_backhand                
        
        # top player hits the ball
        elif self.rect.colliderect(top_player):
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            self.speedx, self.speedy = self.get_stroke_speed("top", keyState)
            # forehand animation
            if self.rect.colliderect(top_player) and self.rect.x > top_player.rect.x + 10:
                top_layer.image = images.camden_forehand
            #backhand animation
            elif self.rect.colliderect(top_player) and self.rect.x < top_player.rect.x - 10:
                top_layer.image = images.camden_backhand

        # Bottom player's deuce side serve
        if keyState[pygame.K_PERIOD] and 350 < bottom_player.rect.x < 575 and bottom_player.rect.y > 449:
            bottom_player.image = images.robert_serve
            self.rect.center = (bottom_player.rect.x + 15, bottom_player.rect.y)
            self.speedx = -7
            self.speedy = -10

        # Bottom's add side serve
        if keyState[pygame.K_PERIOD] and 175 < bottom_player.rect.x < 350 and bottom_player.rect.y > 449:
            bottom_player.image = images.robert_serve
            self.rect.center = (bottom_player.rect.x + 15, bottom_player.rect.y)
            self.speedx = 7
            self.speedy = -10

        #top_player's deuce side serve
        if keyState[pygame.K_TAB] and 175 < top_player.rect.x < 350 and top_player.rect.y < 78:
            top_player.image = images.camden_serve
            self.rect.center = (top_player.rect.x, top_player.rect.y + 40)
            self.speedx = 7
            self.speedy = 14

        #top_player's add side serve
        if keyState[pygame.K_TAB] and 350 < top_player.rect.x < 575 and top_player.rect.y < 78:
            top_player.image = images.camden_serve
            self.rect.center = (top_player.rect.x, top_player.rect.y + 40)
            self.speedx = -7
            self.speedy = 14

        #Make the ball slow down
        self.speedy = self.speedy * 0.99
        self.speedx = self.speedx * 0.99
        self.rect = self.rect.move(self.speedx, self.speedy)
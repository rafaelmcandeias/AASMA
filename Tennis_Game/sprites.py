import pygame
import images

# Player Sprites
# Bottom 2.5 4.4
# Top 3.5 3.3
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, is_bot, speedx_rate, speedy_rate):
        pygame.sprite.Sprite.__init__(self)
        if is_bot:
            self.image = images.robert
        else:
            self.image = images.camden
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 0
        self.speedy = 0
        self.speedx_rate = speedx_rate
        self.speedy_rate = speedy_rate

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_LEFT]:
            self.speedx = -self.speedx_rate
        if keyState[pygame.K_RIGHT]:
            self.speedx = self.speedx_rate
        self.rect.x += self.speedx
        if self.rect.right > 700:
            self.rect.right = 700
        if self.rect.left < 0:
            self.rect.left = 0
        if keyState[pygame.K_UP]:
            self.speedy = -self.speedy_rate
        if keyState[pygame.K_DOWN]:
            self.speedy = self.speedy_rate
        self.rect.y += self.speedy
        if self.rect.y < 325:
            self.rect.y = 325
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 587:
            self.rect.y = 587

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
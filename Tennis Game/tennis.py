import pygame
import images

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
OUT = (193, 58, 34)
COURT = (69, 150, 81)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SKIN = (232, 214, 162)

#Create the screen
windowSize = (700, 650)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('Clinton Tennis Tour')

#Start screen
startGame = False
while startGame == False:
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 60)
    font2 = pygame.font.Font('freesansbold.ttf', 36)
    startLabel = font.render('Clinton Tennis Tour', 1, (WHITE))
    label2 = font2.render('Press SHIFT to start!', 1, (WHITE))
    for event in pygame.event.get():
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_RSHIFT] or keyState[pygame.K_LSHIFT]:
            startGame = True
        screen.blit(startLabel, (65, 225))
        screen.blit(label2, (170, 450))
        pygame.display.flip()

# Player Sprites
class Robert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.robert
        self.rect = self.image.get_rect()
        self.rect.center = (400, 575)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_LEFT]:
            self.speedx = -2.4
        if keyState[pygame.K_RIGHT]:
            self.speedx = 2.4
        self.rect.x += self.speedx
        if self.rect.right > 700:
            self.rect.right = 700
        if self.rect.right < 0:
            self.rect.left = 0
        if keyState[pygame.K_UP]:
            self.speedy = -4.25
        if keyState[pygame.K_DOWN]:
            self.speedy = 2.6
        self.rect.y += self.speedy
        if self.rect.y < 325:
            self.rect.y = 325
        if self.rect.y < 0:
            self.rect.y = 0

class Camden(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.camden
        self.rect = self.image.get_rect()
        self.rect.center = (260, 80)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_a]:
            self.speedx = -3.5
        if keyState[pygame.K_d]:
            self.speedx = 3.5
        self.rect.x += self.speedx
        if self.rect.right > 700:
            self.rect.right = 700
        if self.rect.right < 0:
            self.rect.left = 0
        if keyState[pygame.K_w]:
            self.speedy = -3.3
        if keyState[pygame.K_s]:
            self.speedy = 4.75
        self.rect.y += self.speedy
        if self.rect.y > 250:
            self.rect.y = 250
        if self.rect.y < 0:
            self.rect.y = 0

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tennisBall.png")
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 0

    def update(self):
        #Robert's forehand
        if tennisBall.rect.colliderect(robert) and tennisBall.rect.x > robert.rect.x + 10:
            robert.image = images.robert_forehand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            robert.rect.y -5
            self.speedy = -13
            self.speedx = 3

        #Robert's backhand
        if tennisBall.rect.colliderect(robert) and tennisBall.rect.x < robert.rect.x - 10:
            robert.image = images.robert_backhand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            robert.rect.y -5
            self.speedy = -12
            self.speedx = -2

        #Robert's forehand volley
        if tennisBall.rect.colliderect(robert) and tennisBall.rect.x > robert.rect.x + 10 and 325 < robert.rect.y < 450:
            robert.image = images.robert_forehand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            robert.rect.y -5
            self.speedy = -5

        #Robert's backhand volley
        if tennisBall.rect.colliderect(robert) and tennisBall.rect.x < robert.rect.x - 10 and 325 < robert.rect.y < 450:
            robert.image = images.robert_backhand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            robert.rect.y -5
            self.speedy = -4.5

        #Camden's forehand
        if tennisBall.rect.colliderect(camden) and tennisBall.rect.x < camden.rect.x -10:
            camden.image = images.camden_forehand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            camden.rect.y -5
            self.speedy = 14
            self.speedx = 2

        #Camden's backhand
        if tennisBall.rect.colliderect(camden) and tennisBall.rect.x > camden.rect.x + 10:
            camden.image = images.camden_backhand
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            camden.rect.y -5
            self.speedy = 13
            self.speedx = 2

        #Camden's forehand volley
        if tennisBall.rect.colliderect(camden) and tennisBall.rect.x < camden.rect.x -10 and 200 < camden.rect.y < 325:
            camden.image = images.camden_forehand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            camden.rect.y -5
            self.speedy = 3.75

        #Camden's backhand volley
        if tennisBall.rect.colliderect(camden) and tennisBall.rect.x > camden.rect.x + 10 and 200 < camden.rect.y < 325:
            camden.image = images.camden_backhand_volley
            effect = pygame.mixer.Sound('tennisserve.wav')
            effect.play(0)
            camden.rect.y -5
            self.speedy = 3.75

        keyState = pygame.key.get_pressed()

        #Robert's deuce side serve
        if keyState[pygame.K_PERIOD] and 350 < robert.rect.x < 575 and robert.rect.y > 449:
            robert.image = images.robert_serve
            self.rect.center = (robert.rect.x + 15, robert.rect.y)
            self.speedx = -7
            self.speedy = -10

        #Robert's add side serve
        if keyState[pygame.K_PERIOD] and 175 < robert.rect.x < 350 and robert.rect.y > 449:
            robert.image = images.robert_serve
            self.rect.center = (robert.rect.x + 15, robert.rect.y)
            self.speedx = 7
            self.speedy = -10

        #Camden's deuce side serve
        if keyState[pygame.K_TAB] and 175 < camden.rect.x < 350 and camden.rect.y < 78:
            camden.image = images.camden_serve
            self.rect.center = (camden.rect.x, camden.rect.y + 40)
            self.speedx = 7
            self.speedy = 14

        #Camden's add side serve
        if keyState[pygame.K_TAB] and 350 < camden.rect.x < 575 and camden.rect.y < 78:
            camden.image = images.camden_serve
            self.rect.center = (camden.rect.x, camden.rect.y + 40)
            self.speedx = -7
            self.speedy = 14

        #Make the ball slow down
        self.speedy = self.speedy * .98
        self.speedx = self.speedx * .98
        self.rect = self.rect.move(self.speedx, self.speedy)

#Add people
all_sprites = pygame.sprite.Group()
robert = Robert()
camden = Camden()
tennisBall = Ball()
all_sprites.add(robert)
all_sprites.add(tennisBall)
all_sprites.add(camden)

carryOn = True
clock = pygame.time.Clock()

#Declare global scoring variables so that they can be used within the loop
global score
score = 0
global score2
score2 = 0
global setScore
setScore = 0
global setScore2
setScore2 = 0

stops = 0
ball_is_stopped = False
stops2 = 0
ball_is_stopped2 = False

#Main game loop
while carryOn:
    font = pygame.font.Font('freesansbold.ttf', 32)
    screen.fill(OUT)

    camden.update()
    robert.update()
    tennisBall.update()

    epsilonComp = .2
    #Checks to see if the top player's shot made it over the net
    if tennisBall.rect.y > 325:
        #Checks to make sure it's in bounds
        if 175 < tennisBall.rect.x < 575:
            if abs(tennisBall.speedx) > epsilonComp and abs(tennisBall.speedy) > epsilonComp:
                ball_is_stopped = False
            elif abs(tennisBall.speedx) < epsilonComp and abs(tennisBall.speedy) < epsilonComp:
                if not ball_is_stopped:
                    stops += 1
                ball_is_stopped = True
                if stops == 2:
                    score = 15
                if stops == 3:
                    score = 30
                if stops == 4:
                    score = 40
                if stops == 5:
                    score = 0
                    score2 = 0
                    stops = 1
                    setScore += 1
                    stops2 = 0

        else:
            #If the shot was not in bounds, the bottom player scores a point
            if abs(tennisBall.speedx) > epsilonComp and abs(tennisBall.speedy) > epsilonComp:
                ball_is_stopped2 = False
            elif abs(tennisBall.speedx) < epsilonComp and abs(tennisBall.speedy) < epsilonComp:
                if not ball_is_stopped2:
                    stops2 += 1
                ball_is_stopped2 = True
                if stops2 == 1:
                    score2 = 15
                if stops2 == 2:
                    score2 = 30
                if stops2 == 3:
                    score2 = 40
                if stops2 == 4:
                    score2 = 0
                    score = 0
                    setScore2 += 1
                    stops2 = 0
                    stops = 1

    #Checks to see if the bottom player's shot made it over the net
    elif tennisBall.rect.y < 325:
        if 175 < tennisBall.rect.x < 575:
            if abs(tennisBall.speedx) > epsilonComp and abs(tennisBall.speedy) > epsilonComp:
                ball_is_stopped2 = False
            elif abs(tennisBall.speedx) < epsilonComp and abs(tennisBall.speedy) < epsilonComp:
                if not ball_is_stopped2:
                    stops2 += 1
                ball_is_stopped2 = True
                if stops2 == 1:
                    score2 = 15
                if stops2 == 2:
                    score2 = 30
                if stops2 == 3:
                    score2 = 40
                if stops2 == 4:
                    score2 = 0
                    score = 0
                    setScore2 += 1
                    stops2 = 0
                    stops = 1

        else:
            #If the shot was not in bounds, the top player scores a point
            if abs(tennisBall.speedx) > epsilonComp and abs(tennisBall.speedy) > epsilonComp:
                ball_is_stopped = False
            elif abs(tennisBall.speedx) < epsilonComp and abs(tennisBall.speedy) < epsilonComp:
                if not ball_is_stopped:
                    stops += 1
                ball_is_stopped = True
                if stops == 2:
                    score = 15
                if stops == 3:
                    score = 30
                if stops == 4:
                    score = 40
                if stops == 5:
                    score = 0
                    score2 = 0
                    setScore += 1
                    stops = 1
                    stop2 = 0

    #Render both scoreboards
    scorebox = font.render(str(score), True, WHITE, BLACK)
    scoreRect = scorebox.get_rect()
    scoreRect.center = (625, 50)
    screen.blit(scorebox, scoreRect)
    scorebox2 = font.render(str(score2), True, WHITE, BLACK)
    scoreRect2 = scorebox2.get_rect()
    scoreRect2.center = (625, 600)
    screen.blit(scorebox2, scoreRect2)

    setbox = font.render(str(setScore), True, WHITE, BLACK)
    setrect = setbox.get_rect()
    setrect.center = (625, 175)
    screen.blit(setbox, setrect)
    setbox2 = font.render(str(setScore2), True, WHITE, BLACK)
    setrect2 = setbox2.get_rect()
    setrect2.center = (625, 475)
    screen.blit(setbox2, setrect2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False

    all_sprites.update()

    #All the court lines drawn here in the main loop

    #Draw the court
    pygame.draw.rect(screen, COURT, [175, 75, 350, 500])
    #outer left line
    pygame.draw.line(screen, WHITE, (175,574), (175,75), 7)
    #outer right line
    pygame.draw.line(screen, WHITE, (525,574), (525,75), 7)
    #top center line
    pygame.draw.line(screen, WHITE, (175, 200), (525,200), 7)
    #top outer line
    pygame.draw.line(screen, WHITE, (175, 78), (525,78), 7)
    #bottom outer line
    pygame.draw.line(screen, WHITE, (175, 571), (525,571), 7)
    #bottom center line
    pygame.draw.line(screen, WHITE, (175, 450), (525,450), 7)
    #center white line
    pygame.draw.line(screen, WHITE, (350,200), (350,450), 7)
    #net
    pygame.draw.line(screen, BLACK, (175,325), (525,325), 10)
    #bottom serve line
    pygame.draw.line(screen, WHITE, (350,574), (350,584), 7)
    #top serve line
    pygame.draw.line(screen, WHITE, (350,65), (350,75), 7)

    #Update
    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

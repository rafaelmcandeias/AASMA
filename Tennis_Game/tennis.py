import pygame
import images
import numpy as np
import numpy.random as rnd
from sprites import Top_player, Bottom_player, Ball

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
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('AASMA OPEN')

#Start screen
startGame = False
while startGame == False:
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 60)
    font2 = pygame.font.Font('freesansbold.ttf', 36)
    startLabel = font.render('    AASMA OPEN', 1, (WHITE))
    label2 = font2.render('Press SHIFT to start!', 1, (WHITE))
    for event in pygame.event.get():
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_RSHIFT] or keyState[pygame.K_LSHIFT]:
            startGame = True
        screen.blit(startLabel, (65, 225))
        screen.blit(label2, (170, 450))
        pygame.display.flip()


#Add players
bottom_player = Bottom_player(442, 524, 2.5, 4.2)
top_player = Top_player(202, 40, 3.3, 3.5)

# Tennis ball
tennisBall = Ball()

# Adds all objects into a group
all_sprites = pygame.sprite.Group()
all_sprites.add(bottom_player)
all_sprites.add(tennisBall)
all_sprites.add(top_player)

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

    top_player.update()
    bottom_player.update()
    tennisBall.update(bottom_player, top_player)

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
            if event.key == pygame.K_ESCAPE:
                carryOn = False

    bottom_player.update()
    top_player.update()
    tennisBall.update(bottom_player, top_player)

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

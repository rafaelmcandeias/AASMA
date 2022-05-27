import pygame
import images
import numpy as np
import numpy.random as rnd
from sprites import Top_player, Bottom_player, Ball


# Start game
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


# Adds bars to show stamina of each agent
# (font, size bold)
font = pygame.font.SysFont("comicsans", 30, True)


# Add players
# Speed, Force, Energy
top_player = Top_player(5, 10, 1)
bottom_player = Bottom_player(5, 10, 1)

# Tennis ball
tennisBall = Ball()

# Adds all objects into a group
all_sprites = pygame.sprite.Group()
all_sprites.add(bottom_player)
all_sprites.add(tennisBall)
all_sprites.add(top_player)

carryOn = True
clock = pygame.time.Clock()

# init scores
bottom_player_score = 0
top_player_score = 0

def restart_player_position():
    bottom_player.rect.x = 442
    bottom_player.rect.y = 524
    top_player.rect.x = 202
    top_player.rect.y = 40
    pygame.time.wait(750)

#Main game loop
while carryOn:

    font = pygame.font.Font('freesansbold.ttf', 32)
    screen.fill(OUT)

    # has someone won?
    if bottom_player_score == 15 or top_player_score == 15:
        carryOn = False

    # update 
    top_player.update()
    bottom_player.update()
    point = tennisBall.update(bottom_player, top_player)

    # bottom player won
    if point == 1: 
        bottom_player_score += 1
        restart_player_position()

    # top player won
    if point == 2:
        top_player_score += 1
        restart_player_position()

    
    #Render both scoreboards
    scorebox = font.render(str(top_player_score), True, WHITE, BLACK)
    scoreRect = scorebox.get_rect()
    scoreRect.center = (625, 50)
    screen.blit(scorebox, scoreRect)
    scorebox2 = font.render(str(bottom_player_score), True, WHITE, BLACK)
    scoreRect2 = scorebox2.get_rect()
    scoreRect2.center = (625, 600)
    screen.blit(scorebox2, scoreRect2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                carryOn = False

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

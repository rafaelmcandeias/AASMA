import pygame
import operator
from sprites import Top_player, Bottom_player, Ball
from env import reset, step_bp, step_tp

# Define some colors
BLACK = (0, 0, 0)
OUT = (193, 58, 34)
COURT = (69, 150, 81)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SKIN = (232, 214, 162)
YELLOW = (255, 0, 255)

# Stamina Box Position Values
TOP_INFO_POS = (75, 20)
BOT_INFO_POS = (300, 300)


#Create the screen
def create_screen():
    windowSize = (700, 650)
    screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
    pygame.display.set_caption('AASMA OPEN')
    return screen


#Start screen
def start_screen(screen):
    startGame = False
    while not startGame:
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

def draw_court(screen, bottom_player_score, top_player_score):

    font = pygame.font.Font('freesansbold.ttf', 30)
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

    # init scoreboard
    top_player_box = font.render("TOP", True, WHITE, BLACK)
    top_player_rect = top_player_box.get_rect()
    top_player_rect.center = (625,50)
    bottom_player_box = font.render("BOT", True, WHITE, BLACK)
    bottom_player_rect = bottom_player_box.get_rect()
    bottom_player_rect.center = (625,80)
    screen.blit(top_player_box, top_player_rect)
    screen.blit(bottom_player_box, bottom_player_rect)

    scorebox = font.render(str(top_player_score), True, WHITE, BLACK)
    scoreRect = scorebox.get_rect()
    scoreRect.center = (670, 50)
    screen.blit(scorebox, scoreRect)
    scorebox2 = font.render(str(bottom_player_score), True, WHITE, BLACK)
    scoreRect2 = scorebox2.get_rect()
    scoreRect2.center = (670, 80)
    screen.blit(scorebox2, scoreRect2)

# Function to replace the agent's at the serving position 
def restart_player_position_ts(top_player, bottom_player):
    bottom_player.rect.x = 442
    bottom_player.rect.y = 524
    top_player.rect.x = 202
    top_player.rect.y = 40
    pygame.time.wait(250)

def restart_player_position_bs(top_player, bottom_player):
    bottom_player.rect.x = 442
    bottom_player.rect.y = 524
    top_player.rect.x = 202
    top_player.rect.y = 40
    pygame.time.wait(250)


# Reads two lines from Agents.txt and gets info from it
def read_file():
    agents_file = open("Agents.txt", "r")
    agents = {}
    for line in agents_file:
        if line[0] != '#':
            # Name, Speed, Force, Energy
            info = line.split(" ")
            name, speed, force, energy = info[0], info[1], info[2], info[3]
            # agents = {'Rodrigo':('Rodrigo', 4, 3, 4), ...}
            agents[name] = (name, float(speed), float(force), float(energy))
    return agents


# Creates all objects in the game
def create_objects(agents, name, name2):
    # Add players
    top_player = Top_player(agents[name])
    bottom_player = Bottom_player(agents[name2])

    # Tennis ball
    tennisBall = Ball()

    # Adds all objects into a group
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bottom_player)
    all_sprites.add(tennisBall)
    all_sprites.add(top_player)

    return top_player, bottom_player, tennisBall, all_sprites


#Main game loop
def play(screen, top_player, bottom_player, tennisBall, all_sprites, mode):
    # init scores
    bottom_player_score = 0
    top_player_score = 0
    
    serve_flag = True

    carryOn = True
    clock = pygame.time.Clock()

    # draw the court
    draw_court(screen, bottom_player_score, top_player_score)

    while carryOn:

        font = pygame.font.Font('freesansbold.ttf', 32)
        screen.fill(OUT)
        point = 0

        draw_court(screen, bottom_player_score, top_player_score)

        # has someone won?
        if bottom_player_score == 15 or top_player_score == 15:
            break

        # update
        step_bp(serve_flag, bottom_player, top_player, tennisBall, mode)
        point = step_tp(serve_flag, bottom_player, top_player, tennisBall, mode)
        serve_flag = False
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)

        # bottom player won
        if point == 1: 
            bottom_player_score += 1
            serve_flag = reset(1, screen, bottom_player, top_player, bottom_player_score, top_player_score)

        # top player won
        elif point == 2:
            top_player_score += 1
            # reset always returns True, which resets the serve flag
            serve_flag = reset(2, screen, bottom_player, top_player, bottom_player_score, top_player_score)

        # To exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False

    return top_player_score, bottom_player_score


# Function to print the scoreboard from highest to lowest score
def print_scoreboard(scores):
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    print("===========================")
    print("         SCOREBOARD        ")
    print("===========================")
    for name, score in sorted_scores:
        print("||      " + name + ": " + str(score) + "      ||")
    print("===========================")

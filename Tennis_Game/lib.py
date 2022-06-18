from time import sleep
import pygame
import operator
from sprites import CENTER_X, LIMIT_BOT, Top_player, Bottom_player, Ball
from env import LIMIT_BOT_FIELD, step_bp, step_tp

# ------------------------------------------------------------

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

# Vars for point winners
BOT_WON = 1
TOP_WON = 2
HIT = 3
FAULT = 4
POINT = 5
MAX_POINTS = 15

# ------------------------------------------------------------

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


# Reads two lines from Agents.txt and gets info from it
def read_file():
    agents_file = open("Agents.txt", "r")
    agents = {}
    for line in agents_file:
        if line[0] != '#':
            # Name, Speed, Force, Energy
            info = line.split(" ")
            name, speed, force, energy, mode = info[0], info[1], info[2], info[3], info[4].rstrip()
            # agents = {'Rodrigo':('Rodrigo', 4, 3, 4, 'random'), ...}
            agents[name] = (name, float(speed), float(force), float(energy), mode)
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


# Function to draw the court lines, point screens and objects
def draw_court(screen, bottom_player_score, top_player_score):
    font = pygame.font.Font('freesansbold.ttf', 30)
    #Draw the court
    pygame.draw.rect(screen, COURT, [175, 75, 350, 500])
    #outer left line
    pygame.draw.line(screen, WHITE, (175, 574), (175, 75), 7)
    #outer right line
    pygame.draw.line(screen, WHITE, (525, 574), (525, 75), 7)
    #top center line
    pygame.draw.line(screen, WHITE, (175, 200), (525, 200), 7)
    #top outer line
    pygame.draw.line(screen, WHITE, (175, 78), (525, 78), 7)
    #bottom outer line
    pygame.draw.line(screen, WHITE, (175, 571), (525, 571), 7)
    #bottom center line
    pygame.draw.line(screen, WHITE, (175, 450), (525, 450), 7)
    #center white line
    pygame.draw.line(screen, WHITE, (350, 200), (350, 450), 7)
    #net
    pygame.draw.line(screen, BLACK, (172.5, 325), (528, 325), 10)
    #bottom serve line
    pygame.draw.line(screen, WHITE, (350, 574), (350, 584), 7)
    #top serve line
    pygame.draw.line(screen, WHITE, (350, 65), (350, 75), 7)

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


# Function to draw the stamina bar
def draw_bars(screen, top_player, bottom_player):
    barPosTop = (top_player.rect.topleft[0] + 5 ,top_player.rect.topleft[1] - 12)
    barPosBottom = (bottom_player.rect.topleft[0] - 10,bottom_player.rect.topleft[1] - 12)
    barSize = (55, 10)
    borderColor = (0,0,0)
    barColor = (0,128,0)
    
    # Draws top player's stamina
    pygame.draw.rect(screen, borderColor, (barPosTop, barSize), 1)
    innerPos = (barPosTop[0] + 3, barPosTop[1] + 3)
    innerSize = ((barSize[0] - 6) * top_player.stamina, barSize[1] - 6)
    pygame.draw.rect(screen, barColor, (innerPos, innerSize))
    
    # Draws bottom player's stamina
    pygame.draw.rect(screen, borderColor, (barPosBottom, barSize), 1)
    innerPos = (barPosBottom[0] + 3, barPosBottom[1] + 3)
    innerSize = ((barSize[0] - 6) * bottom_player.stamina, barSize[1] - 6)
    pygame.draw.rect(screen, barColor, (innerPos,innerSize))


# Function to compute step for each agent
def steps(screen, player_to_strike, bottom_player, top_player, tennisBall):
    
    # Compute bot agent step. HIT or None
    hit_bot = step_bp(player_to_strike, bottom_player, top_player, tennisBall, bottom_player.mode)
    # Compute top agent step
    hit_top = step_tp(player_to_strike, bottom_player, top_player, tennisBall, top_player.mode)
    # Update ball position
    event = tennisBall.update_position(screen)
    
    # Has any agent stroke the ball
    if hit_bot == HIT or hit_top == HIT:
        return HIT
    
    # Did the ball not pass the net
    if event == FAULT:
        return FAULT
    
    # Did anyone score a point
    if event == POINT:
        return POINT
    
    # Nothing interesting happened
    return None


# Function to replace the agent's at the serving position 
def restart_positions(top_player, bottom_player, tennisBall, server):
    top_player.restart_position()
    bottom_player.restart_position()
    tennisBall.restart_position(server)
    pygame.time.wait(750)


# Function to render the new score boxes
def render(screen, top_player_score, bottom_player_score):
    # Update scoreboards
    font = pygame.font.Font('freesansbold.ttf', 30)
    scorebox = font.render(str(top_player_score), True, WHITE, BLACK)
    scoreRect = scorebox.get_rect()
    scoreRect.center = (670, 50)
    screen.blit(scorebox, scoreRect)
    scorebox2 = font.render(str(bottom_player_score), True, WHITE, BLACK)
    scoreRect2 = scorebox2.get_rect()
    scoreRect2.center = (670, 50)
    screen.blit(scorebox2, scoreRect2)


# Changes player to serve and to strike
def change_roles(top_player, bottom_player, server):
    if server == top_player:
        return bottom_player, top_player
    return top_player, bottom_player


#Main game loop
def play(screen, top_player, bottom_player, tennisBall, all_sprites):
    # init scores
    bottom_player_score = 0
    top_player_score = 0
    server = top_player
    player_to_strike = bottom_player
    # flag to know when is to serve
    serve_flag = True

    carryOn = True
    clock = pygame.time.Clock()

    # draw the court
    draw_court(screen, bottom_player_score, top_player_score)

    while carryOn:

        pygame.font.Font('freesansbold.ttf', 32)
        screen.fill(OUT)
        point = 0

        draw_court(screen, bottom_player_score, top_player_score)

        # Serving time and server serves
        if serve_flag:
            tennisBall.serve(server, screen)
            serve_flag = False

        # Only computes rest if service was successful or it was not to serve
        else:
            # Players and ball only move if there was a service
            # update. compute steps
            hit = steps(screen, player_to_strike, bottom_player, top_player, tennisBall)
            
            # Player to strike striked the ball. Change it
            if hit == HIT:
                if player_to_strike == top_player:
                    player_to_strike = bottom_player
                else:
                    player_to_strike = top_player
            
            # Check if a point was scored
            point = tennisBall.scored_point(player_to_strike, hit)

            # player scored
            if point == BOT_WON or point == TOP_WON:
                # bottom player won
                if point == BOT_WON:
                    bottom_player_score += 1
                # top player won
                else:
                    top_player_score += 1
                # has someone won?
                if bottom_player_score == 15 or top_player_score == 15:
                    break
                # Changes server and player to strike
                server, player_to_strike = change_roles(top_player, bottom_player, server)
                # Re sets the agent's position
                restart_positions(top_player, bottom_player, tennisBall, server)
                # Renders the new score
                render(screen, top_player_score, bottom_player_score)
                serve_flag = True

            # Health bars
            draw_bars(screen, top_player, bottom_player)

            all_sprites.draw(screen)
            pygame.display.update()
            clock.tick(60)

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

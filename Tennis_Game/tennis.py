from lib import pygame, create_screen, start_screen, read_file, create_objects, play, print_scoreboard
import pandas as pd

WIN = 1
DRAW = 0
LOSS = -1

# Main execution
if __name__ == "__main__":
    agents = {}
    # Start game
    pygame.init()
    # Creates start screen
    screen = create_screen()
    # Executes start screen 
    start_screen(screen)
    # Read agent's information. {Agent_name: (name, speed, force, energy), ...}
    agents = read_file()
    # Create scores dict
    # {agent.name: (wins, score_average)}
    scores = {k:0 for k in agents.keys()}
    # database {mode: [(win_flag, points), ...], mode2: [..., ...]}
    database = {mode:[] for mode in ('random', 'beginner', 'expert', 'pro')}
    
    # All agents against each other
    print("\n\n===========================")
    print("        GAME STARTED       ")
    print("===========================\n")
    
    # 32 times
    for _ in range(24):
        # Takes n*(n-1) games 
        for top_name in set(agents.keys()):
            for bot_name in set(agents.keys()):
                # An agent can not play against itself
                if bot_name == top_name:
                    continue
                # Creates agents and ball
                top_player, bottom_player, ball, all_sprites = create_objects(agents, top_name, bot_name)

                print(top_name + " " + top_player.mode + " vs " + bot_name + " " + bottom_player.mode)
                # Executes game
                top_score, bot_score = play(screen, top_player, bottom_player, ball, all_sprites)
                print(top_name + ": " + str(top_score) + " / " + bot_name + ": " + str(bot_score) + "\n")
                # Updates score and database dictionairies
                if top_score > bot_score:
                    scores[top_name] += 1
                    database[top_player.mode].append((WIN, top_score))
                    database[bottom_player.mode].append((LOSS, bot_score))
                elif bot_score > top_score:
                    scores[bot_name] += 1
                    database[bottom_player.mode].append((WIN, bot_score))
                    database[top_player.mode].append((LOSS, top_score))
                else:
                    database[bottom_player.mode].append((DRAW, bot_score))
                    database[top_player.mode].append((DRAW, top_score))
    
    print_scoreboard(scores)
    # Code used to gather data
    #for mode in database.keys():
    #    df = pd.DataFrame(database[mode])
    #    file_name = 'results/' + mode + '.csv'
    #    df.to_csv(file_name, index=False, header=False)

    # End game
    pygame.quit()

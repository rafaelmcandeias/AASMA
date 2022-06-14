from lib import pygame, create_screen, start_screen, read_file, create_objects, play, print_scoreboard


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
    scores = {k:0 for k in agents.keys()}
    
    # All agents against each other
    print("\n\n===========================")
    print("        GAME STARTED       ")
    print("===========================\n")
    
    # Takes n! games 
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

            # Updates score dictionaire
            if top_score > bot_score:
                scores[top_name] += 1
            elif bot_score > top_score:
                scores[bot_name] += 1
    
    print_scoreboard(scores)
    # End game
    pygame.quit()

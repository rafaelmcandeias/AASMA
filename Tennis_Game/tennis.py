from lib import pygame, create_screen, start_screen, read_file, create_objects, play

# Main execution
if __name__ == "__main__":
    agents = {}
    # Start game
    pygame.init()
    # Creates start screen
    screen = create_screen()
    # Executes start screen 
    start_screen(screen)
    # Read agent's information
    agents = read_file()
    # All agents against each other
    for name in set(agents.keys()):
        for name2 in set(agents.keys()).difference(name):
            # Creates agents and ball
            top_player, bottom_player, ball, all_sprites = create_objects(agents, name, name2)
            # Executes game
            play(screen, top_player, bottom_player, ball, all_sprites)
    # End game
    pygame.quit()

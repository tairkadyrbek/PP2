import pygame
import sys
from racer import RacerGame
import ui
import persistence

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Racer Game")
settings = persistence.load_settings()
current_screen = "menu"
username = ""


def play_game():
    # Start and run the game
    global current_screen
    
    result = RacerGame(screen, settings, username)
    
    if result:
        # Save score
        persistence.add_score(username, result['score'], result['distance'], result['coins'])
        
        # Show game over
        action = ui.show_game_over(screen, result)
        if action == "retry":
            play_game()
        elif action == "menu":
            current_screen = "menu"


def main():
    # Main game loop
    global current_screen, username, settings
    
    running = True
    while running:
        if current_screen == "menu":
            action = ui.show_main_menu(screen)
            
            if action == "play":
                username = ui.get_username(screen)
                if username:
                    play_game()
                    
            elif action == "leaderboard":
                current_screen = "leaderboard"
                
            elif action == "settings":
                current_screen = "settings"
                
            elif action == "quit":
                running = False
                
        elif current_screen == "leaderboard":
            leaderboard = persistence.load_leaderboard()
            action = ui.show_leaderboard(screen, leaderboard)
            if action == "back":
                current_screen = "menu"
                
        elif current_screen == "settings":
            new_settings = ui.show_settings(screen, settings)
            if new_settings:
                settings = new_settings
                persistence.save_settings(settings)
            current_screen = "menu"
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
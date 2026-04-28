import pygame
import sys
from game import Game, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, GREEN, RED, GOLD, GRAY
from db import init_database, get_leaderboard
from config import load_settings, save_settings

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("Arial", 40)
font_medium = pygame.font.SysFont("Arial", 25)
font_small = pygame.font.SysFont("Arial", 20)


def draw_button(text, x, y, width, height, mouse_pos):
    rect = pygame.Rect(x, y, width, height)
    color = YELLOW if rect.collidepoint(mouse_pos) else WHITE
    pygame.draw.rect(screen, color, rect, 2)
    text_surf = font_medium.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect


def show_menu():
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        
        # Title
        title = font_large.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (150, 100))
        
        # Buttons
        play_btn = draw_button("Play", 200, 200, 200, 50, mouse_pos)
        board_btn = draw_button("Leaderboard", 200, 270, 200, 50, mouse_pos)
        settings_btn = draw_button("Settings", 200, 340, 200, 50, mouse_pos)
        quit_btn = draw_button("Quit", 200, 410, 200, 50, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    username = enter_username()
                    if username:
                        return username
                elif board_btn.collidepoint(event.pos):
                    show_leaderboard()
                elif settings_btn.collidepoint(event.pos):
                    show_settings()
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(30)


def enter_username():
    username = ""

    while True:
        screen.fill(BLACK)

        text = font_medium.render("Enter name: " + username, True, WHITE)
        screen.blit(text, (150, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        pygame.display.flip()
        clock.tick(30)


def show_leaderboard():
    data = get_leaderboard(10)

    while True:
        screen.fill(BLACK)

        title = font_large.render("TOP 10", True, YELLOW)
        screen.blit(title, (200, 50))

        for i, row in enumerate(data):
            text = font_small.render(f"{i+1}. {row[0]} - {row[1]}", True, WHITE)
            screen.blit(text, (150, 120 + i * 30))

        back = font_small.render("ESC - back", True, GRAY)
        screen.blit(back, (200, 500))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(30)


def show_settings():
    settings = load_settings()
    
    colors = [("Green", [0, 255, 0]), ("Blue", [0, 100, 255]), ("Red", [255, 0, 0]),
              ("Yellow", [255, 255, 0]), ("Purple", [128, 0, 128])]
    
    # find current color index
    color_index = 0
    for i, c in enumerate(colors):
        if settings['snake_color'] == c[1]:
            color_index = i

    
    while True:
        screen.fill(BLACK)
        
        title = font_large.render("SETTINGS", True, YELLOW)
        screen.blit(title, (200, 80))
        
        # Grid
        grid_val = "ON" if settings['grid_overlay'] else "OFF"
        grid_color = GREEN if settings['grid_overlay'] else RED
        grid_text = font_medium.render(f"G - Grid: {grid_val}", True, grid_color)
        screen.blit(grid_text, (150, 200))
        
        # Sound
        sound_val = "ON" if settings['sound'] else "OFF"
        sound_color = GREEN if settings['sound'] else RED
        sound_text = font_medium.render(f"S - Sound: {sound_val}", True, sound_color)
        screen.blit(sound_text, (150, 260))
        
        # Snake color
        label = font_medium.render("Snake Color:", True, WHITE)
        screen.blit(label, (150, 320))
        color_name, color_value = colors[color_index]
        color_text = font_medium.render(f"< {color_name} >", True, color_value)
        screen.blit(color_text, (350, 320))
    
        # hints
        hint1 = font_small.render("LEFT/RIGHT - change color", True, GRAY)
        hint2 = font_small.render("ESC - save & back", True, GRAY)
        
        screen.blit(hint1, (150, 400))
        screen.blit(hint2, (150, 440))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    settings['grid_overlay'] = not settings['grid_overlay']

                elif event.key == pygame.K_s:
                    settings['sound'] = not settings['sound']

                elif event.key == pygame.K_LEFT:
                    color_index = (color_index - 1) % len(colors)
                    settings['snake_color'] = colors[color_index][1]

                elif event.key == pygame.K_RIGHT:
                    color_index = (color_index + 1) % len(colors)
                    settings['snake_color'] = colors[color_index][1]

                elif event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return
        
        pygame.display.flip()
        clock.tick(30)


def show_game_over(game):
    while True:
        screen.fill(BLACK)

        # texts
        title = font_large.render("GAME OVER", True, RED)
        score = font_medium.render(f"Score: {game.score}", True, WHITE)
        retry = font_medium.render("Press R to retry", True, WHITE)
        menu = font_medium.render("ESC - menu", True, GRAY)

        # center positions
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        retry_rect = retry.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        menu_rect = menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))

        # draw
        screen.blit(title, title_rect)
        screen.blit(score, score_rect)
        screen.blit(retry, retry_rect)
        screen.blit(menu, menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'retry'
                elif event.key == pygame.K_ESCAPE:
                    return 'menu'

        pygame.display.flip()
        clock.tick(30)


def run_game(username):
    game = Game(screen, clock, username)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction("RIGHT")
        
        if not game.update():
            game.save_result()
            return show_game_over(game)
        
        game.draw()
        pygame.display.flip()
        clock.tick(game.get_fps())


def main():
    init_database()
    
    while True:
        username = show_menu()
        while True:
            result = run_game(username)
            if result == 'menu':
                break
            elif result == 'quit':
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
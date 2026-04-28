import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 50, 50)
GOLD = (255, 215, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


def show_main_menu(screen):
    """Show main menu"""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                if event.key == pygame.K_2:
                    return "leaderboard"
                if event.key == pygame.K_3:
                    return "settings"
                if event.key == pygame.K_q:
                    return "quit"
        
        screen.fill((30, 30, 30))
        
        # Title
        title = font.render("RACER GAME", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        # Menu options
        play_text = font.render("1 - Play", True, WHITE)
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(play_text, play_rect)
        
        leaderboard_text = font.render("2 - Leaderboard", True, WHITE)
        lb_rect = leaderboard_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        screen.blit(leaderboard_text, lb_rect)
        
        settings_text = font.render("3 - Settings", True, WHITE)
        settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, 390))
        screen.blit(settings_text, settings_rect)
        
        quit_text = font.render("Q - Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 460))
        screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()
        clock.tick(60)


def get_username(screen):
    """Get username from player"""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    input_text = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(input_text) > 0:
                    return input_text
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 15 and event.unicode.isprintable():
                    input_text += event.unicode
        
        screen.fill((30, 30, 30))
        
        prompt = font.render("Enter your name:", True, WHITE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(prompt, prompt_rect)
        
        # Input box
        pygame.draw.rect(screen, WHITE, (50, 260, 300, 50), 2)
        
        # Show typed text
        name_text = font.render(input_text, True, WHITE)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 285))
        screen.blit(name_text, name_rect)
        
        # Hint
        hint = font.render("Press ENTER", True, GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 380))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_leaderboard(screen, leaderboard):
    """Show leaderboard"""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                    return "back"
        
        screen.fill((30, 30, 30))
        
        # Title
        title = font.render("LEADERBOARD", True, GOLD)
        screen.blit(title, (80, 30))
        
        # Show top 10
        y_pos = 100
        for i in range(min(10, len(leaderboard))):
            entry = leaderboard[i]
            color = GOLD if i == 0 else WHITE
            
            text = f"{i+1}. {entry['name'][:10]} - {entry['score']} pts"
            score_text = small_font.render(text, True, color)
            screen.blit(score_text, (50, y_pos))
            y_pos += 35
        
        # If empty
        if len(leaderboard) == 0:
            empty = font.render("No scores yet!", True, GRAY)
            screen.blit(empty, (90, 250))
        
        # Back hint
        hint = small_font.render("Press B to go back", True, GRAY)
        screen.blit(hint, (90, 530))
        
        pygame.display.flip()
        clock.tick(60)


def show_settings(screen, current_settings):
    """Show settings"""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    
    settings = current_settings.copy()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    settings['sound'] = not settings.get('sound', True)
                
                if event.key == pygame.K_2:
                    colors = ["blue", "red", "green"]
                    current = settings.get("car_color", "blue")
                    idx = colors.index(current) if current in colors else 0
                    settings['car_color'] = colors[(idx + 1) % len(colors)]
                
                if event.key == pygame.K_3:
                    difficulties = ["easy", "medium", "hard"]
                    current = settings.get("difficulty", "medium")
                    idx = difficulties.index(current) if current in difficulties else 1
                    settings['difficulty'] = difficulties[(idx + 1) % len(difficulties)]
                
                if event.key == pygame.K_RETURN:
                    return settings
                
                if event.key == pygame.K_ESCAPE:
                    return None
        
        screen.fill((30, 30, 30))
        
        # Title
        title = font.render("SETTINGS", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Options
        sound_status = "ON" if settings.get('sound', True) else "OFF"
        sound_text = font.render(f"1 - Sound: {sound_status}", True, WHITE)
        sound_rect = sound_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(sound_text, sound_rect)
        
        car_color = settings.get('car_color', 'blue').upper()
        car_text = font.render(f"2 - Car: {car_color}", True, WHITE)
        car_rect = car_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(car_text, car_rect)
        
        difficulty = settings.get('difficulty', 'medium').upper()
        diff_text = font.render(f"3 - Difficulty: {difficulty}", True, WHITE)
        diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        screen.blit(diff_text, diff_rect)
        
        # Hints
        save_hint = font.render("ENTER - Save", True, GREEN)
        save_rect = save_hint.get_rect(center=(SCREEN_WIDTH // 2, 430))
        screen.blit(save_hint, save_rect)
        
        back_hint = font.render("ESC - Cancel", True, RED)
        back_rect = back_hint.get_rect(center=(SCREEN_WIDTH // 2, 490))
        screen.blit(back_hint, back_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_game_over(screen, result):
    """Show game over screen"""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 35)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                    return "menu"
        
        screen.fill((30, 30, 30))
        
        # Title
        if result['completed']:
            title = font.render("RACE COMPLETE!", True, GREEN)
        else:
            title = font.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)
        
        # Stats
        score_text = small_font.render(f"Score: {result['score']}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(score_text, score_rect)
        
        distance_text = small_font.render(f"Distance: {result['distance']}m", True, WHITE)
        distance_rect = distance_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(distance_text, distance_rect)
        
        coins_text = small_font.render(f"Coins: {result['coins']}", True, WHITE)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 340))
        screen.blit(coins_text, coins_rect)
        
        # Options
        retry_text = small_font.render("R - Retry", True, GREEN)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, 440))
        screen.blit(retry_text, retry_rect)
        
        menu_text = small_font.render("M - Main Menu", True, BLUE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(menu_text, menu_rect)
        
        pygame.display.flip()
        clock.tick(60)
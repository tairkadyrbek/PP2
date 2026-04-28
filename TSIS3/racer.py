import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60


class Player(pygame.sprite.Sprite):
    """Player car"""
    def __init__(self, color_name):
        super().__init__()
        self.image = pygame.image.load(f"assets/images/player_{color_name}.png")
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 500)
        self.speed = 5
        
    def move(self, keys):
        """Move player with arrow keys"""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed


class Enemy(pygame.sprite.Sprite):
    """Enemy car"""
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("assets/images/enemy.png")
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = -60
        self.speed = speed
        
    def update(self):
        """Move enemy down"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    """Road obstacle"""
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        
        # Random obstacle type
        obstacle_types = ["concrete", "oil", "pothole"]
        self.type = random.choice(obstacle_types)
        
        if self.type == "concrete":
            # Load concrete barrier image
            self.image = pygame.image.load("assets/images/obstacle.png")
            self.image = pygame.transform.scale(self.image, (60, 40))
            
        elif self.type == "oil":
            # Black oil spill (irregular circle)
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, BLACK, (20, 20), 18)
            pygame.draw.circle(self.image, (50, 50, 50), (15, 15), 8)
            pygame.draw.circle(self.image, (50, 50, 50), (25, 22), 6)
            
        else:  # pothole
            # Dark pothole
            self.image = pygame.Surface((35, 35))
            self.image.fill((40, 40, 40))  # Very dark gray
            pygame.draw.circle(self.image, (20, 20, 20), (17, 17), 15)
            pygame.draw.circle(self.image, BLACK, (17, 17), 15, 2)
            
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        
    def update(self):
        """Move obstacle down"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    """Collectible coin"""
    def __init__(self, speed):
        super().__init__()
        # Random coin value
        rand = random.random()
        if rand < 0.6:
            self.value = 5
            self.color = BRONZE
        elif rand < 0.9:
            self.value = 10
            self.color = SILVER
        else:
            self.value = 20
            self.color = GOLD
        
        # Draw coin as colored circle
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (12, 12), 12)
        pygame.draw.circle(self.image, BLACK, (12, 12), 12, 2)
        
        # Draw value number on coin
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center=(12, 12))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, SCREEN_WIDTH - 40)
        self.rect.y = -25
        self.speed = speed
        
    def update(self):
        """Move coin down"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """Power-up item"""
    def __init__(self, speed):
        super().__init__()
        # Random power-up type
        powerup_types = ["nitro", "shield", "repair"]
        self.type = random.choice(powerup_types)
        self.speed = speed
        
        # Load power-up image
        self.image = pygame.image.load(f"assets/images/{self.type}.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, SCREEN_WIDTH - 50)
        self.rect.y = -30
        
    def update(self):
        """Move power-up down"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


def spawn_enemy(enemies, obstacles, all_sprites, player, current_speed):
    enemy = Enemy(current_speed)
    found_safe = False

    for _ in range(20):
        enemy.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        enemy.rect.y = -60

        safe = True

        # avoid player
        if enemy.rect.colliderect(player.rect):
            safe = False

        # avoid other enemies
        if safe:
            for e in enemies:
                if enemy.rect.colliderect(e.rect):
                    safe = False
                    break

        # avoid obstacles
        if safe:
            for obs in obstacles:
                if enemy.rect.colliderect(obs.rect):
                    safe = False
                    break

        if safe:
            found_safe = True
            break

    if found_safe:
        enemies.add(enemy)
        all_sprites.add(enemy)


def spawn_obstacle(obstacles, enemies, all_sprites, player, current_speed):
    obstacle = Obstacle(current_speed)
    found_safe = False

    for _ in range(20):
        obstacle.rect.x = random.randint(0, SCREEN_WIDTH - obstacle.rect.width)
        obstacle.rect.y = -obstacle.rect.height

        safe = True

        # avoid player
        if obstacle.rect.colliderect(player.rect):
            safe = False

        # avoid enemies
        if safe:
            for e in enemies:
                if obstacle.rect.colliderect(e.rect):
                    safe = False
                    break

        # avoid other obstacles
        if safe:
            for obs in obstacles:
                if obstacle.rect.colliderect(obs.rect):
                    safe = False
                    break

        if safe:
            found_safe = True
            break

    if found_safe:
        obstacles.add(obstacle)
        all_sprites.add(obstacle)


def spawn_coin(coins, all_sprites, current_speed, enemies, obstacles, player):
    """Spawn a new coin in a safe location"""
    coin = Coin(current_speed)
    
    found_safe = False
    
    for attempt in range(20):
        # Random position at top
        coin.rect.x = random.randint(20, SCREEN_WIDTH - 40)
        coin.rect.y = -25
        
        safe = True
        
        # Check collision with enemies
        for enemy in enemies:
            if coin.rect.colliderect(enemy.rect):
                safe = False
                break
        
        # Check collision with obstacles
        if safe:
            for obstacle in obstacles:
                if coin.rect.colliderect(obstacle.rect):
                    safe = False
                    break
        
        # Check collision with player
        if safe and not coin.rect.colliderect(player.rect):
            found_safe = True
            break
    
    # Only add if safe position found
    if found_safe:
        coins.add(coin)
        all_sprites.add(coin)


def spawn_powerup(powerups, all_sprites, current_speed):
    """Spawn a new power-up"""
    powerup = PowerUp(current_speed)
    powerups.add(powerup)
    all_sprites.add(powerup)


def activate_powerup(powerup_type, obstacles, player):
    """Activate a power-up effect"""
    if powerup_type == "nitro":
        return "nitro", pygame.time.get_ticks() + 4000
    elif powerup_type == "shield":
        return "shield", 0
    else:  # repair
        # Clear nearby obstacles
        for obstacle in obstacles:
            if obstacle.rect.y > player.rect.y - 100 and obstacle.rect.y < player.rect.y + 100:
                obstacle.kill()
        return None, 0


def draw_road(screen, bg_y):
    """Draw the road background"""
    background = pygame.image.load("assets/images/AnimatedStreet.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Draw background twice for scrolling effect
    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - SCREEN_HEIGHT))


def draw_ui(screen, score, coins, distance, max_distance, current_speed, active_powerup, powerup_time):
    """Draw game UI"""
    font = pygame.font.SysFont("Arial", 20)
    small_font = pygame.font.SysFont("Arial", 16)
    
    # Score and coins
    score_text = font.render(f"Score: {score}", True, WHITE)
    coins_text = font.render(f"Coins: {coins}", True, GOLD)
    distance_text = small_font.render(f"Distance: {int(distance)}/{max_distance}", True, WHITE)
    speed_text = small_font.render(f"Speed: {int(current_speed)}", True, CYAN)
    
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(distance_text, (10, 70))
    screen.blit(speed_text, (SCREEN_WIDTH - 120, 10))
    
    # Active power-up
    if active_powerup == "nitro":
        remaining = max(0, (powerup_time - pygame.time.get_ticks()) / 1000)
        powerup_text = small_font.render(f"NITRO: {remaining:.1f}s", True, YELLOW)
        screen.blit(powerup_text, (SCREEN_WIDTH - 150, 40))
    elif active_powerup == "shield":
        powerup_text = small_font.render("SHIELD ACTIVE", True, BLUE)
        screen.blit(powerup_text, (SCREEN_WIDTH - 150, 40))


def RacerGame(screen, settings, username):
    """Main game function"""
    clock = pygame.time.Clock()
    
    # Initialize sound
    pygame.mixer.init()
    
    # Load sounds if sound is enabled
    crash_sound = None
    if settings.get("sound", True):
        # Play background music
        pygame.mixer.music.load("assets/sounds/background.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Loop forever
        
        # Load crash sound
        crash_sound = pygame.mixer.Sound("assets/sounds/crash.wav")
    
    # Game variables
    score = 0
    coins = 0
    distance = 0
    max_distance = 5000
    base_speed = 5
    current_speed = base_speed
    bg_y = 0  # Background scroll position
    
    # Difficulty
    difficulty_multipliers = {"easy": 0.7, "medium": 1.0, "hard": 1.5}
    difficulty = difficulty_multipliers.get(settings.get("difficulty", "medium"), 1.0)
    
    # Power-ups
    active_powerup = None
    powerup_time = 0
    shield_active = False
    nitro_active = False
    
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    # Player
    player_color_name = settings.get("car_color", "blue")
    player = Player(player_color_name)
    all_sprites.add(player)
    
    # Timers
    enemy_timer = 0
    obstacle_timer = 0
    coin_timer = 0
    powerup_timer = 0
    
    # Game loop
    running = True
    game_over = False
    
    while running and not game_over:
        dt = clock.tick(FPS)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
        
        # Update distance
        distance += current_speed / 10
        
        # Scroll background
        bg_y += current_speed
        if bg_y >= SCREEN_HEIGHT:
            bg_y = 0
        
        # Check win
        if distance >= max_distance:
            running = False
            break
        
        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Update speed
        speed_increase = (distance // 500) * 0.5
        nitro_boost = 3 if nitro_active else 0
        current_speed = base_speed + speed_increase + nitro_boost
        
        # Spawn enemies
        enemy_timer += dt
        enemy_spawn_rate = max(800 - (distance // 100) * 10, 400) / difficulty
        if enemy_timer > enemy_spawn_rate:
            spawn_enemy(enemies, obstacles, all_sprites, player, current_speed)
            enemy_timer = 0
        
        # Spawn obstacles
        obstacle_timer += dt
        obstacle_spawn_rate = max(1500 - (distance // 200) * 20, 700) / difficulty
        if obstacle_timer > obstacle_spawn_rate:
            spawn_obstacle(obstacles, enemies, all_sprites, player, current_speed)
            obstacle_timer = 0
        
        # Spawn coins
        coin_timer += dt
        if coin_timer > 1500:
            spawn_coin(coins_group, all_sprites, current_speed, enemies, obstacles, player)
            coin_timer = 0
        
        # Spawn power-ups
        powerup_timer += dt
        if powerup_timer > 8000:
            if random.random() < 0.3:
                spawn_powerup(powerups, all_sprites, current_speed)
            powerup_timer = 0
        
        # Update sprites
        all_sprites.update()
        
        # Check nitro expiration
        if active_powerup == "nitro" and pygame.time.get_ticks() > powerup_time:
            nitro_active = False
            active_powerup = None
        
        # Collect coins
        collected_coins = pygame.sprite.spritecollide(player, coins_group, True)
        for coin in collected_coins:
            coins += coin.value
            score += coin.value
        
        # Collect power-ups
        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in collected_powerups:
            if not active_powerup or active_powerup == "shield":
                new_powerup, new_time = activate_powerup(powerup.type, obstacles, player)
                if new_powerup == "nitro":
                    active_powerup = "nitro"
                    nitro_active = True
                    powerup_time = new_time
                elif new_powerup == "shield":
                    active_powerup = "shield"
                    shield_active = True
                else:
                    score += 10
        
        # Check collisions
        if pygame.sprite.spritecollide(player, enemies, False):
            if shield_active:
                shield_active = False
                active_powerup = None
                pygame.sprite.spritecollide(player, enemies, True)
            else:
                if crash_sound:
                    crash_sound.play()
                    pygame.time.wait(500)  # Wait for crash sound
                game_over = True
        
        if pygame.sprite.spritecollide(player, obstacles, False):
            if shield_active:
                shield_active = False
                active_powerup = None
                pygame.sprite.spritecollide(player, obstacles, True)
            else:
                if crash_sound:
                    crash_sound.play()
                    pygame.time.wait(500)  # Wait for crash sound
                game_over = True
        
        # Draw everything
        draw_road(screen, bg_y)
        all_sprites.draw(screen)
        draw_ui(screen, score, coins, distance, max_distance, current_speed, active_powerup, powerup_time)
        
        pygame.display.flip()
    
    # Stop music when game ends
    pygame.mixer.music.stop()
    
    # Return result
    if game_over:
        return {
            'score': score,
            'distance': int(distance),
            'coins': coins,
            'completed': False
        }
    else:
        score += 500  # Completion bonus
        return {
            'score': score,
            'distance': int(distance),
            'coins': coins,
            'completed': True
        }
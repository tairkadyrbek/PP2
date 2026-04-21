import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# Setting up FPS (Frames Per Second) for smooth gameplay
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors using RGB values
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Initial enemy speed
SCORE = 0  # Enemies dodged
COINS_COLLECTED = 0  # Total coin value collected
COINS_FOR_SPEEDUP = 50  # Speed increases every 50 coin points

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("resources/AnimatedStreet.png")

# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves down the screen"""
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("resources/Enemy.png")
        self.rect = self.image.get_rect()
        # Spawn at random x position at top of screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        """Move enemy downward and respawn at top when reaching bottom"""
        global SCORE
        self.rect.move_ip(0, SPEED)  # Move down by SPEED pixels
        # If enemy reaches bottom, increment score and respawn
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    """Player car controlled by arrow keys"""
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("resources/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Starting position
       
    def move(self):
        """Handle player movement based on keyboard input"""
        pressed_keys = pygame.key.get_pressed()
        
        # Move left if not at left edge
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        # Move right if not at right edge
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """Collectible coin with different weights/values"""
    def __init__(self):
        super().__init__()
        # Randomly determine coin type and value
        # 60% chance bronze (5 points), 30% silver (10 points), 10% gold (20 points)
        rand = random.random()
        if rand < 0.6:
            self.coin_type = 'bronze'
            self.value = 5
            self.color = BRONZE
        elif rand < 0.9:
            self.coin_type = 'silver'
            self.value = 10
            self.color = SILVER
        else:
            self.coin_type = 'gold'
            self.value = 20
            self.color = GOLD
        
        # Create coin image (circle with border)
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (12, 12), 12)
        pygame.draw.circle(self.image, BLACK, (12, 12), 12, 2)  # Black border
        
        # Draw value text on coin
        coin_font = pygame.font.SysFont("Arial", 12, bold=True)
        value_text = coin_font.render(str(self.value), True, BLACK)
        text_rect = value_text.get_rect(center=(12, 12))
        self.image.blit(value_text, text_rect)
        
        self.rect = self.image.get_rect()
        # Spawn at random position at top of screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)
    
    def move(self):
        """Move coin downward"""
        self.rect.move_ip(0, SPEED)  # Move at same speed as enemies
        # If coin reaches bottom, remove it
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Setting up Sprites        
P1 = Player()
E1 = Enemy()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()  # Group for all coins

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new User event for speed increase
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Trigger every 1000ms (1 second)

# Adding event for spawning coins
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 2000)  # Spawn coin every 2 seconds

# Track last speed increase threshold
last_speedup_threshold = 0

# Game Loop
while True:
      
    # Cycles through all events occurring  
    for event in pygame.event.get():
        # Increase game speed over time
        if event.type == INC_SPEED:
            SPEED += 0.5
        
        # Spawn new coin randomly
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        
        # Handle window close button
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))
    
    # Display score (dodged enemies) in top left
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    
    # Display collected coins in top right
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, GOLD)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))
    
    # Display current speed
    speed_text = font_small.render(f"Speed: {int(SPEED)}", True, BLUE)
    DISPLAYSURF.blit(speed_text, (SCREEN_WIDTH // 2 - 40, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    # Check for coin collection
    coins_collected = pygame.sprite.spritecollide(P1, coins, True)  # True = remove collected coins
    for coin in coins_collected:
        COINS_COLLECTED += coin.value  # Add coin value to total
        
        # Check if we should increase speed based on coin collection
        # Every COINS_FOR_SPEEDUP coins, increase speed by 1
        if COINS_COLLECTED // COINS_FOR_SPEEDUP > last_speedup_threshold:
            SPEED += 1
            last_speedup_threshold = COINS_COLLECTED // COINS_FOR_SPEEDUP
            print(f"Speed increased! Now: {SPEED}")  # Debug message
    
    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('resources/crash.wav').play()
        time.sleep(1)
                   
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        
        # Display final stats
        final_score = font_small.render(f"Score: {SCORE}", True, BLACK)
        final_coins = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
        DISPLAYSURF.blit(final_score, (150, 320))
        DISPLAYSURF.blit(final_coins, (150, 350))
        
        pygame.display.update()
        
        # Clean up all sprites
        for entity in all_sprites:
            entity.kill() 
        
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)
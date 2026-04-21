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
YELLOW = (255, 215, 0)  # Color for coins

# Game configuration variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Initial speed of enemies
SCORE = 0  # Number of enemies dodged
COINS = 0  # Number of coins collected

# Setting up fonts for displaying text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("resources/AnimatedStreet.png")

# Create game window
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


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
    """Collectible coin that appears randomly on the road"""
    def __init__(self):
        super().__init__()
        # Create a simple yellow circle as coin image
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        pygame.draw.circle(self.image, BLACK, (15, 15), 15, 2)  # Black border
        self.rect = self.image.get_rect()
        # Spawn at random position at top of screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    
    def move(self):
        """Move coin downward and respawn at random intervals"""
        self.rect.move_ip(0, SPEED)  # Move at same speed as enemies
        # If coin reaches bottom, respawn at top
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Setting up sprite instances
P1 = Player()
E1 = Enemy()

# Creating sprite groups for collision detection and rendering
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()  # Group for all coins
# Create initial coins (2-3 coins on screen)
for i in range(3):
    coin = Coin()
    coin.rect.y = random.randint(-200, 0)  # Stagger initial positions
    coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(*coins)  # Add all coins to rendering group

# Adding a custom event to increase speed over time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Trigger every 1000ms (1 second)

# Main game loop
while True:
    # Process all events (keyboard, mouse, custom events)
    for event in pygame.event.get():
        # Increase game speed every second
        if event.type == INC_SPEED:
            SPEED += 0.5
        # Handle window close button
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))
    
    # Display score (dodged enemies) in top left corner
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    
    # Display collected coins in top right corner
    coins_text = font_small.render(f"Coins: {COINS}", True, YELLOW)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    # Move and render all sprites (player, enemies, coins)
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    # Check for coin collection
    coins_collected = pygame.sprite.spritecollide(P1, coins, True)  # True = remove collected coins
    for coin in coins_collected:
        COINS += 1  # Increment coin counter
        # Create a new coin to replace the collected one
        new_coin = Coin()
        new_coin.rect.y = random.randint(-200, -30)  # Spawn above screen
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Check for collision between player and enemies (game over condition)
    if pygame.sprite.spritecollideany(P1, enemies):
        # Play crash sound
        pygame.mixer.Sound('resources/crash.wav').play()
        time.sleep(1)
        
        # Display game over screen
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        
        # Show final stats
        final_score = font_small.render(f"Score: {SCORE}", True, BLACK)
        final_coins = font_small.render(f"Coins: {COINS}", True, BLACK)
        DISPLAYSURF.blit(final_score, (150, 320))
        DISPLAYSURF.blit(final_coins, (150, 350))
        
        pygame.display.update()
        
        # Clean up all sprites
        for entity in all_sprites:
            entity.kill()
        
        # Wait before closing
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Update display and maintain frame rate
    pygame.display.update()
    FramePerSec.tick(FPS)
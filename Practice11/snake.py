import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20  # Size of each grid cell
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Colors (RGB format)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

# Game Variables
FPS = 10  # Initial frames per second (snake speed)
score = 0
level = 1
FOOD_PER_LEVEL = 3  # Number of foods needed to advance to next level
foods_eaten = 0

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Level 1")
clock = pygame.time.Clock()

# Setup fonts
font_large = pygame.font.SysFont("Arial", 40)
font_medium = pygame.font.SysFont("Arial", 25)
font_small = pygame.font.SysFont("Arial", 20)


class Snake:
    """Represents the snake player character"""
    
    def __init__(self):
        """Initialize snake at center of screen with length 3"""
        # Snake body is list of [x, y] positions
        self.body = [[GRID_WIDTH // 2, GRID_HEIGHT // 2],
                     [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2],
                     [GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2]]
        self.direction = "RIGHT"  # Initial direction
        self.grow = False  # Flag to indicate if snake should grow
    
    def move(self):
        """Move snake in current direction"""
        # Get current head position
        head_x, head_y = self.body[0]
        
        # Calculate new head position based on direction
        if self.direction == "UP":
            new_head = [head_x, head_y - 1]
        elif self.direction == "DOWN":
            new_head = [head_x, head_y + 1]
        elif self.direction == "LEFT":
            new_head = [head_x - 1, head_y]
        elif self.direction == "RIGHT":
            new_head = [head_x + 1, head_y]
        
        # Add new head to front of snake
        self.body.insert(0, new_head)
        
        # Remove tail unless snake is growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False  # Reset grow flag
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        # Prevent snake from reversing directly into itself
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction
    
    def check_wall_collision(self):
        """Check if snake head hits the wall (border) or UI panel"""
        head_x, head_y = self.body[0]
        
        # Check if head is outside the playing area or in UI panel area (top 2 rows)
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 2 or head_y >= GRID_HEIGHT:
            return True
        return False
    
    def check_self_collision(self):
        """Check if snake head collides with its own body"""
        head = self.body[0]
        
        # Check if head position matches any body segment (excluding head itself)
        if head in self.body[1:]:
            return True
        return False
    
    def eat_food(self):
        """Trigger snake growth on next move"""
        self.grow = True
    
    def draw(self, surface):
        """Draw snake on the screen"""
        for i, segment in enumerate(self.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            
            # Draw head slightly different (brighter green)
            if i == 0:
                pygame.draw.rect(surface, (0, 255, 100), (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(surface, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            
            # Add border to each segment
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)


class Food:
    """Represents the food that snake eats with different weights and timer"""
    
    def __init__(self, snake):
        """Initialize food at random valid position with random weight"""
        self.position = self.generate_position(snake)
        self.set_random_weight()
        self.spawn_time = pygame.time.get_ticks()  # Record when food spawned (milliseconds)
        self.lifetime = random.randint(5000, 10000)  # Food lives 5-10 seconds
    
    def generate_position(self, snake):
        """Generate random position that doesn't overlap with snake or walls"""
        while True:
            # Generate random grid position
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(2, GRID_HEIGHT - 1)  # Start from row 2 to avoid UI panel
            position = [x, y]
            
            # Check if position is valid (not on snake body)
            if position not in snake.body:
                return position
    
    def set_random_weight(self):
        """Randomly assign weight (points) and color to food"""
        # 50% chance normal (10 points), 30% big (20 points), 20% super (30 points)
        rand = random.random()
        if rand < 0.5:
            self.weight = 10
            self.color = RED
            self.name = "Normal"
        elif rand < 0.8:
            self.weight = 20
            self.color = ORANGE
            self.name = "Big"
        else:
            self.weight = 30
            self.color = GOLD
            self.name = "Super"
    
    def respawn(self, snake):
        """Move food to new random valid position and reset timer"""
        self.position = self.generate_position(snake)
        self.set_random_weight()
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(5000, 10000)
    
    def is_expired(self):
        """Check if food has expired (timer ran out)"""
        current_time = pygame.time.get_ticks()
        return (current_time - self.spawn_time) >= self.lifetime
    
    def get_time_left(self):
        """Get remaining time in seconds"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        remaining = max(0, self.lifetime - elapsed)
        return remaining / 1000.0  # Convert to seconds
    
    def draw(self, surface):
        """Draw food on the screen with pulsing effect when expiring"""
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        
        # Pulse effect when food is about to expire (last 2 seconds)
        time_left = self.get_time_left()
        if time_left < 2.0:
            # Pulsing effect using sine wave
            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.01) * 50))
            color = tuple(max(0, min(255, c + pulse)) for c in self.color)
        else:
            color = self.color
        
        pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))
        # Add border
        pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw weight indicator (size varies by weight)
        indicator_size = CELL_SIZE // 3
        if self.weight == 20:
            indicator_size = CELL_SIZE // 2
        elif self.weight == 30:
            indicator_size = int(CELL_SIZE * 0.6)
        
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        pygame.draw.circle(surface, WHITE, (center_x, center_y), indicator_size // 2)
        
        # Draw timer bar above food
        bar_width = CELL_SIZE
        bar_height = 3
        time_ratio = self.get_time_left() / (self.lifetime / 1000.0)
        filled_width = int(bar_width * time_ratio)
        
        # Draw background (gray)
        pygame.draw.rect(surface, GRAY, (x, y - 5, bar_width, bar_height))
        # Draw filled portion (green/yellow/red based on time left)
        if time_ratio > 0.5:
            bar_color = GREEN
        elif time_ratio > 0.25:
            bar_color = YELLOW
        else:
            bar_color = RED
        pygame.draw.rect(surface, bar_color, (x, y - 5, filled_width, bar_height))


def draw_grid(surface):
    """Draw grid lines on the playing field"""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_ui(surface, score, level, foods_eaten, food):
    """Draw score, level, and food info at top of screen"""
    # Create solid black background for UI (no transparency)
    pygame.draw.rect(surface, BLACK, (0, 0, SCREEN_WIDTH, 2 * CELL_SIZE))
    
    # Draw score
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    
    # Draw level
    level_text = font_small.render(f"Level: {level}", True, YELLOW)
    surface.blit(level_text, (200, 10))
    
    # Draw progress to next level
    progress_text = font_small.render(f"Foods: {foods_eaten}/{FOOD_PER_LEVEL}", True, GREEN)
    surface.blit(progress_text, (400, 10))
    
    # Draw food info (type and timer)
    food_info = font_small.render(f"{food.name} ({food.weight}pts) - {food.get_time_left():.1f}s", True, food.color)
    surface.blit(food_info, (10, 25))


def show_game_over(surface, final_score, final_level):
    """Display game over screen with final stats"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    surface.blit(game_over_text, text_rect)
    
    # Final score
    score_text = font_medium.render(f"Final Score: {final_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(score_text, score_rect)
    
    # Final level
    level_text = font_medium.render(f"Level Reached: {final_level}", True, YELLOW)
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    surface.blit(level_text, level_rect)
    
    # Restart instruction
    restart_text = font_small.render("Press SPACE to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    surface.blit(restart_text, restart_rect)
    
    pygame.display.update()


def show_level_up(surface, new_level):
    """Display level up notification"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # Level up text
    level_up_text = font_large.render(f"LEVEL {new_level}!", True, YELLOW)
    text_rect = level_up_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(level_up_text, text_rect)
    
    pygame.display.update()
    pygame.time.delay(1000)  # Show for 1 second


def reset_game():
    """Reset all game variables for new game"""
    global score, level, foods_eaten, FPS
    score = 0
    level = 1
    foods_eaten = 0
    FPS = 10
    pygame.display.set_caption("Snake Game - Level 1")
    return Snake(), Food(Snake())


def main():
    """Main game loop"""
    global score, level, foods_eaten, FPS
    
    # Initialize game objects
    snake = Snake()
    food = Food(snake)
    
    running = True
    game_over = False
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    # Control snake direction with arrow keys
                    if event.key == pygame.K_UP:
                        snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction("RIGHT")
                else:
                    # Game over controls
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        snake, food = reset_game()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        if not game_over:
            # Move snake
            snake.move()
            
            # Check for wall collision
            if snake.check_wall_collision():
                game_over = True
            
            # Check for self collision
            if snake.check_self_collision():
                game_over = True
            
            # Check if food expired (timer ran out)
            if food.is_expired():
                food.respawn(snake)
            
            # Check if snake eats food
            if snake.body[0] == food.position:
                snake.eat_food()
                score += food.weight  # Add food weight to score
                foods_eaten += 1
                
                # Check if level up condition is met
                if foods_eaten >= FOOD_PER_LEVEL:
                    level += 1
                    foods_eaten = 0
                    FPS += 2  # Increase speed (snake moves faster)
                    pygame.display.set_caption(f"Snake Game - Level {level}")
                    
                    # Show level up screen briefly
                    screen.fill(BLACK)
                    draw_grid(screen)
                    snake.draw(screen)
                    food.draw(screen)
                    draw_ui(screen, score, level, foods_eaten, food)
                    show_level_up(screen, level)
                
                # Spawn new food at valid position
                food.respawn(snake)
            
            # Drawing
            screen.fill(BLACK)  # Clear screen
            draw_grid(screen)  # Draw background grid
            snake.draw(screen)  # Draw snake
            food.draw(screen)  # Draw food with timer
            draw_ui(screen, score, level, foods_eaten, food)  # Draw UI
            
            pygame.display.update()
            clock.tick(FPS)  # Control game speed based on level
        
        else:
            # Show game over screen
            show_game_over(screen, score, level)
    
    pygame.quit()
    sys.exit()


# Run the game
if __name__ == "__main__":
    main()
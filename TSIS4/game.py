import pygame
import random
import math
from db import save_game_result, get_personal_best
from config import load_settings

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 100) // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
CYAN = (0, 255, 255)
DARK_GRAY = (50, 50, 50)

# Game settings
FPS = 10
FOOD_PER_LEVEL = 3


class Snake:
    def __init__(self):
        # Start with 3 segments in the middle
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2 + 2
        self.body = [[center_x, center_y], [center_x - 1, center_y], [center_x - 2, center_y]]
        self.direction = "RIGHT"
        self.grow = False
        self.shield_active = False
    
    def move(self):
        head_x, head_y = self.body[0]
        
        # Calculate new head position
        if self.direction == "UP":
            new_head = [head_x, head_y - 1]
        elif self.direction == "DOWN":
            new_head = [head_x, head_y + 1]
        elif self.direction == "LEFT":
            new_head = [head_x - 1, head_y]
        else:  # RIGHT
            new_head = [head_x + 1, head_y]
        
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        # Can't reverse direction
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposites[self.direction]:
            self.direction = new_direction
    
    def check_collision(self, obstacles):
        head_x, head_y = self.body[0]
        
        # Wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 2 or head_y >= GRID_HEIGHT + 2:
            return True
        
        # Self collision
        if self.body[0] in self.body[1:]:
            return True
        
        # Obstacle collision
        if self.body[0] in obstacles:
            return True
        
        return False
    
    def draw(self, surface, color):
        for i, segment in enumerate(self.body):
            x = segment[0] * CELL_SIZE
            y = (segment[1] - 2) * CELL_SIZE + 100
            
            # Draw shield effect
            if i == 0 and self.shield_active:
                pygame.draw.rect(surface, CYAN, (x - 2, y - 2, CELL_SIZE + 4, CELL_SIZE + 4))
            
            # Draw segment
            segment_color = tuple(min(255, c + 50) for c in color) if i == 0 else color
            pygame.draw.rect(surface, segment_color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)


class Food:
    def __init__(self, snake, obstacles):
        self.position = self.get_random_position(snake, obstacles)
        self.set_type()
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(5000, 10000)
    
    def get_random_position(self, snake, obstacles):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(2, GRID_HEIGHT + 1)
            pos = [x, y]
            if pos not in snake.body and pos not in obstacles:
                return pos
    
    def set_type(self):
        # 50% normal, 30% big, 20% super
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
    
    def respawn(self, snake, obstacles):
        self.position = self.get_random_position(snake, obstacles)
        self.set_type()
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(5000, 10000)
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time >= self.lifetime
    
    def get_time_left(self):
        elapsed = pygame.time.get_ticks() - self.spawn_time
        remaining = max(0, self.lifetime - elapsed)
        return remaining / 1000.0
    
    def draw(self, surface):
        x = self.position[0] * CELL_SIZE
        y = (self.position[1] - 2) * CELL_SIZE + 100
        
        # Pulse effect when expiring
        color = self.color
        if self.get_time_left() < 2.0:
            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.01) * 50))
            color = tuple(max(0, min(255, c + pulse)) for c in color)
        
        pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Timer bar
        time_ratio = self.get_time_left() / (self.lifetime / 1000.0)
        bar_width = int(CELL_SIZE * time_ratio)
        bar_color = GREEN if time_ratio > 0.5 else (YELLOW if time_ratio > 0.25 else RED)
        pygame.draw.rect(surface, GRAY, (x, y - 5, CELL_SIZE, 3))
        pygame.draw.rect(surface, bar_color, (x, y - 5, bar_width, 3))


class PoisonFood:
    def __init__(self, snake, obstacles, food):
        self.position = self.get_random_position(snake, obstacles, food)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(7000, 12000)
    
    def get_random_position(self, snake, obstacles, food):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(2, GRID_HEIGHT + 1)
            pos = [x, y]
            if pos not in snake.body and pos not in obstacles and pos != food.position:
                return pos
    
    def respawn(self, snake, obstacles, food):
        self.position = self.get_random_position(snake, obstacles, food)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(7000, 12000)
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time >= self.lifetime
    
    def draw(self, surface):
        x = self.position[0] * CELL_SIZE
        y = (self.position[1] - 2) * CELL_SIZE + 100
        
        pygame.draw.rect(surface, DARK_RED, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
        # Draw skull eyes
        pygame.draw.circle(surface, WHITE, (x + 7, y + 7), 2)
        pygame.draw.circle(surface, WHITE, (x + 13, y + 7), 2)


class PowerUp:
    def __init__(self, snake, obstacles, food, poison):
        self.type = random.choice(['speed', 'slow', 'shield'])
        self.position = self.get_random_position(snake, obstacles, food, poison)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000
    
    def get_random_position(self, snake, obstacles, food, poison):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(2, GRID_HEIGHT + 1)
            pos = [x, y]
            if (pos not in snake.body and pos not in obstacles and 
                pos != food.position and (poison is None or pos != poison.position)):
                return pos
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time >= self.lifetime
    
    def draw(self, surface):
        x = self.position[0] * CELL_SIZE
        y = (self.position[1] - 2) * CELL_SIZE + 100
        
        colors = {'speed': ORANGE, 'slow': BLUE, 'shield': CYAN}
        color = colors[self.type]
        
        pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw letter
        font = pygame.font.SysFont("Arial", 16)
        letter = font.render(self.type[0].upper(), True, BLACK)
        surface.blit(letter, (x + 6, y + 2))


class Game:
    def __init__(self, screen, clock, username):
        self.screen = screen
        self.clock = clock
        self.username = username
        self.settings = load_settings()
        self.font = pygame.font.SysFont("Arial", 20)
        
        # Game state
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.fps = FPS
        self.personal_best = get_personal_best(username)
        
        # Game objects
        self.snake = Snake()
        self.obstacles = self.make_obstacles()
        self.food = Food(self.snake, self.obstacles)
        self.poison = PoisonFood(self.snake, self.obstacles, self.food) if random.random() < 0.7 else None
        self.powerup = None
        
        # Active powerup
        self.active_powerup = None
        self.powerup_start = 0
    
    def make_obstacles(self):
        # No obstacles before level 3
        if self.level < 3:
            return []
        
        obstacles = []
        count = min(5 + (self.level - 3) * 2, 15)
        
        for _ in range(count):
            for attempt in range(50):
                x = random.randint(1, GRID_WIDTH - 2)
                y = random.randint(3, GRID_HEIGHT)
                pos = [x, y]
                
                # Don't place near snake
                too_close = any(abs(seg[0] - x) <= 2 and abs(seg[1] - y) <= 2 for seg in self.snake.body)
                
                if pos not in obstacles and pos not in self.snake.body and not too_close:
                    obstacles.append(pos)
                    break
        
        return obstacles
    
    def update(self):
        self.snake.move()
        
        # Check collision
        if self.snake.check_collision(self.obstacles):
            if self.snake.shield_active:
                self.snake.shield_active = False
            else:
                return False  # Game over
        
        # Food logic
        if self.food.is_expired():
            self.food.respawn(self.snake, self.obstacles)
        
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += self.food.weight
            self.foods_eaten += 1
            
            # Level up
            if self.foods_eaten >= FOOD_PER_LEVEL:
                self.level += 1
                self.foods_eaten = 0
                self.fps += 2
                self.obstacles = self.make_obstacles()
            
            self.food.respawn(self.snake, self.obstacles)
        
        # Poison logic
        if self.poison:
            if self.poison.is_expired():
                self.poison = PoisonFood(self.snake, self.obstacles, self.food) if random.random() < 0.7 else None
            elif self.snake.body[0] == self.poison.position:
                # Remove 2 segments
                if len(self.snake.body) > 2:
                    self.snake.body.pop()
                    self.snake.body.pop()
                elif len(self.snake.body) == 2:
                    self.snake.body.pop()
                else:
                    return False  # Game over
                self.poison = PoisonFood(self.snake, self.obstacles, self.food) if random.random() < 0.7 else None
        
        # Powerup spawn
        if self.powerup is None and random.random() < 0.01:
            self.powerup = PowerUp(self.snake, self.obstacles, self.food, self.poison)
        
        # Powerup logic
        if self.powerup:
            if self.powerup.is_expired():
                self.powerup = None
            elif self.snake.body[0] == self.powerup.position:
                if self.powerup.type == 'shield':
                    self.snake.shield_active = True
                else:
                    self.active_powerup = self.powerup.type
                    self.powerup_start = pygame.time.get_ticks()
                self.powerup = None
        
        # Check powerup duration
        if self.active_powerup and pygame.time.get_ticks() - self.powerup_start >= 5000:
            self.active_powerup = None
        
        return True
    
    def get_fps(self):
        if self.active_powerup == 'speed':
            return self.fps + 5
        elif self.active_powerup == 'slow':
            return max(5, self.fps - 5)
        return self.fps
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Grid
        if self.settings['grid_overlay']:
            for x in range(0, SCREEN_WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (x, 100), (x, SCREEN_HEIGHT))
            for y in range(100, SCREEN_HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (0, y), (SCREEN_WIDTH, y))
        
        # Obstacles
        for obs in self.obstacles:
            x = obs[0] * CELL_SIZE
            y = (obs[1] - 2) * CELL_SIZE + 100
            pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 2)
        
        # Game objects
        snake_color = tuple(self.settings['snake_color'])
        self.snake.draw(self.screen, snake_color)
        self.food.draw(self.screen)
        if self.poison:
            self.poison.draw(self.screen)
        if self.powerup:
            self.powerup.draw(self.screen)
        
        # UI
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, 100))
        
        texts = [
            (f"Score: {self.score}", WHITE, 10, 10),
            (f"Level: {self.level}", YELLOW, 10, 35),
            (f"Foods: {self.foods_eaten}/{FOOD_PER_LEVEL}", GREEN, 10, 60),
            (f"Best: {self.personal_best}", GOLD, 200, 10),
            (f"{self.food.name} ({self.food.weight}pts) - {self.food.get_time_left():.1f}s", self.food.color, 200, 35)
        ]
        
        if self.active_powerup:
            time_left = (5000 - (pygame.time.get_ticks() - self.powerup_start)) / 1000.0
            texts.append((f"PowerUp: {self.active_powerup.capitalize()} ({time_left:.1f}s)", CYAN, 200, 60))
        
        for text, color, x, y in texts:
            surface = self.font.render(text, True, color)
            self.screen.blit(surface, (x, y))
    
    def save_result(self):
        save_game_result(self.username, self.score, self.level)
        self.personal_best = max(self.personal_best, self.score)
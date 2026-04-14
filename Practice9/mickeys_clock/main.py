import pygame
import sys
from clock import draw_clock

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

# for saving proportions
def scale_by_width(img, width):
    height = int(width * img.get_height() / img.get_width())
    return pygame.transform.scale(img, (width, height))

def scale_by_height(img, height):
    width = int(height * img.get_width() / img.get_height())
    return pygame.transform.scale(img, (width, height))


# Load images
bg = pygame.image.load("images/clock.png")
mickey = pygame.image.load("images/mickey.png")
left_hand = pygame.image.load("images/hand_left.png")
right_hand = pygame.image.load("images/hand_right.png")

# Scale everything
bg = scale_by_width(bg, 800)
mickey = scale_by_width(mickey, 290)

# hands
left_hand = pygame.transform.scale(left_hand, (100, 190))
right_hand = pygame.transform.scale(right_hand, (100, 150))

running = True
while running:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_clock(screen, bg, mickey, left_hand, right_hand)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()
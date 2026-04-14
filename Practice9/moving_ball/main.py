import pygame
import sys
import ball

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# Ball
x, y = 300, 300
radius = 25
step = 20

running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                x = ball.move_left(x, radius, step)

            elif event.key == pygame.K_RIGHT:
                x = ball.move_right(x, radius, step, WIDTH)

            elif event.key == pygame.K_UP:
                y = ball.move_up(y, radius, step)

            elif event.key == pygame.K_DOWN:
                y = ball.move_down(y, radius, step, HEIGHT)
    
    ball.draw_ball(screen, x, y, radius)
    
    pygame.display.flip()
    
pygame.quit()
sys.exit()
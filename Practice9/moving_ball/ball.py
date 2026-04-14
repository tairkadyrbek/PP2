import pygame

def move_left(x, radius, step):
    if x - step - radius >= 0:
        x -= step
    return x

def move_right(x, radius, step, width):
    if x + step + radius <= width:
        x += step
    return x

def move_up(y, radius, step):
    if y - step - radius >= 0:
        y -= step
    return y

def move_down(y, radius, step, height):
    if y + step + radius <= height:
        y += step
    return y

def draw_ball(screen, x, y, radius):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
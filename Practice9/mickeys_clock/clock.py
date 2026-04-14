import pygame
from datetime import datetime
import math

def rotate_hand(image, angle, cx, cy, offset_adjust=0):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect()
    # Offset from center (half the hand length)
    offset = image.get_height() // 2 + offset_adjust
    # Convert angle to radians
    rad = math.radians(angle + 90)
    # Calculate the center position of the image
    x = cx + offset * math.cos(rad)
    y = cy - offset * math.sin(rad)
    rect.center = (x, y)
    return rotated, rect

def draw_clock(screen, bg, mickey, left_hand, right_hand):
    screen.fill((255, 255, 255))
    center = (300, 300)
    
    # background centered
    bg_rect = bg.get_rect(center=center)
    screen.blit(bg, bg_rect)
    
    now = datetime.now()
    minute = now.minute
    hour = now.hour % 12
    second = now.second
    
    # Angles
    minute_angle = -(minute * 6 + second * 0.1)
    hour_angle = -(hour * 30 + minute * 0.5)
    
    # Rotate hands with proper centering
    hour_rot, hour_rect = rotate_hand(right_hand, hour_angle, center[0], center[1], -10)
    minute_rot, minute_rect = rotate_hand(left_hand, minute_angle, center[0], center[1], -20)
    
    # Draw hands
    screen.blit(hour_rot, hour_rect)
    screen.blit(minute_rot, minute_rect)
    
    # Draw Mickey
    mickey_rect = mickey.get_rect(center=(300, 280))
    screen.blit(mickey, mickey_rect)
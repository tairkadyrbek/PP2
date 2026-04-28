import pygame
import math

def draw_shape(surface, color, start, end, shape_type, thickness):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    # Rectangle
    if shape_type in ('rect', 'rectangle'):
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(dx), abs(dy))
        pygame.draw.rect(surface, color, rect, thickness)

    # Circle
    elif shape_type == 'circle':
        radius = int(math.hypot(dx, dy))
        if radius > 0:
            pygame.draw.circle(surface, color, (x1, y1), radius, thickness)

    # Square
    elif shape_type == 'square':
        side = max(abs(dx), abs(dy))
        rect = pygame.Rect(
            x1 if dx >= 0 else x1 - side,
            y1 if dy >= 0 else y1 - side,
            side,
            side
        )
        pygame.draw.rect(surface, color, rect, thickness)

    # Right triangle
    elif shape_type in ('right_tri', 'right_triangle'):
        points = [(x1, y1), (x2, y2), (x1, y2)]
        pygame.draw.polygon(surface, color, points, thickness)

    # Equilateral Triangle (angle method)
    elif shape_type in ('eq_tri', 'equilateral_triangle'):
        side = math.hypot(dx, dy)
        if side == 0:
            return

        angle = math.atan2(dy, dx)

        x3 = x1 + side * math.cos(angle + math.pi / 3)
        y3 = y1 + side * math.sin(angle + math.pi / 3)

        points = [(x1, y1), (x2, y2), (int(x3), int(y3))]
        pygame.draw.polygon(surface, color, points, thickness)

    # Rhombus
    elif shape_type == 'rhombus':
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        points = [
            (int(mid_x), y1),
            (x2, int(mid_y)),
            (int(mid_x), y2),
            (x1, int(mid_y))
        ]
        pygame.draw.polygon(surface, color, points, thickness)


def flood_fill(surface, pos, new_color):
    """
    Flood fill algorithm to fill a closed region with a color.
    Uses stack (DFS) to avoid recursion on large fills.
    """
    width, height = surface.get_size()
    x, y = pos
    
    # Boundary check
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    
    # Get the target color at click position
    target_color = surface.get_at((x, y))
    
    # If already the same color, no need to fill
    if target_color[:3] == new_color[:3]:
        return
    
    # Stack-based flood fill (DFS)
    stack = [(x, y)]
    visited = set()
    
    while stack:
        px, py = stack.pop()
        
        # Skip if already visited
        if (px, py) in visited:
            continue
        
        # Boundary check
        if px < 0 or px >= width or py < 0 or py >= height:
            continue
        
        # Check if current pixel matches target color
        current_color = surface.get_at((px, py))
        if current_color[:3] != target_color[:3]:
            continue
        
        # Fill this pixel
        surface.set_at((px, py), new_color)
        visited.add((px, py))
        
        # Add neighboring pixels to stack (4-directional)
        stack.append((px + 1, py))  # Right
        stack.append((px - 1, py))  # Left
        stack.append((px, py + 1))  # Down
        stack.append((px, py - 1))  # Up
import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    # Brush settings
    radius = 15
    mode = 'blue'  # Current color mode
    tool = 'brush'  # Current tool: 'brush', 'rectangle', 'circle', 'eraser', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus'
    points = []
    
    # For shape drawing
    shape_start = None  # Starting point for shapes
    drawing_shape = False
    
    # Eraser settings
    eraser_size = 20
    
    # Available colors
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (128, 0, 128),
        'orange': (255, 165, 0),
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }
    
    current_color = colors['blue']  # Default color
    
    # Font for instructions
    font = pygame.font.SysFont("Arial", 14)
    
    while True:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            # Determine if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # Color selection
                if event.key == pygame.K_r:
                    mode = 'red'
                    current_color = colors['red']
                elif event.key == pygame.K_g:
                    mode = 'green'
                    current_color = colors['green']
                elif event.key == pygame.K_b:
                    mode = 'blue'
                    current_color = colors['blue']
                elif event.key == pygame.K_y:  # Yellow
                    mode = 'yellow'
                    current_color = colors['yellow']
                elif event.key == pygame.K_p:  # Purple
                    mode = 'purple'
                    current_color = colors['purple']
                elif event.key == pygame.K_o:  # Orange
                    mode = 'orange'
                    current_color = colors['orange']
                elif event.key == pygame.K_w and not ctrl_held:  # White
                    mode = 'white'
                    current_color = colors['white']
                elif event.key == pygame.K_k:  # Black
                    mode = 'black'
                    current_color = colors['black']
                
                # Tool selection
                elif event.key == pygame.K_1:  # Brush tool
                    tool = 'brush'
                elif event.key == pygame.K_2:  # Rectangle tool
                    tool = 'rectangle'
                elif event.key == pygame.K_3:  # Circle tool
                    tool = 'circle'
                elif event.key == pygame.K_4:  # Square tool
                    tool = 'square'
                elif event.key == pygame.K_5:  # Right triangle tool
                    tool = 'right_triangle'
                elif event.key == pygame.K_6:  # Equilateral triangle tool
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_7:  # Rhombus tool
                    tool = 'rhombus'
                elif event.key == pygame.K_e:  # Eraser tool
                    tool = 'eraser'
                
                # Clear screen
                elif event.key == pygame.K_c and not ctrl_held:
                    points = []
            
            # Mouse button events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if tool == 'brush':
                        # Start new stroke - add separator to prevent connecting
                        points.append({'type': 'separator'})
                
                if tool == 'brush' or tool == 'eraser':
                    # Left click grows radius/size
                    if event.button == 1:
                        if tool == 'brush':
                            radius = min(200, radius + 1)
                        else:
                            eraser_size = min(200, eraser_size + 1)
                    # Right click shrinks radius/size
                    elif event.button == 3:
                        if tool == 'brush':
                            radius = max(1, radius - 1)
                        else:
                            eraser_size = max(1, eraser_size - 1)
                
                # Start drawing shape (all shape tools)
                elif tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    if event.button == 1:  # Left click to start shape
                        shape_start = event.pos
                        drawing_shape = True
            
            # Mouse button release - finish shape
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_shape and tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    if event.button == 1:
                        shape_end = event.pos
                        # Save the shape
                        points.append({
                            'type': tool,
                            'start': shape_start,
                            'end': shape_end,
                            'color': current_color
                        })
                        drawing_shape = False
                        shape_start = None
            
            # Mouse motion events
            if event.type == pygame.MOUSEMOTION:
                # Get mouse button state
                buttons = pygame.mouse.get_pressed()
                
                if tool == 'brush' and buttons[0]:  # Left button pressed
                    # If mouse moved with brush, add point to list
                    position = event.pos
                    points = points + [{
                        'type': 'brush',
                        'pos': position,
                        'radius': radius,
                        'color': current_color,
                        'mode': mode
                    }]
                    points = points[-512:]  # Keep last 512 points
                
                elif tool == 'eraser' and buttons[0]:  # Left button pressed
                    # Eraser draws black circles (erases by covering with black)
                    position = event.pos
                    points.append({
                        'type': 'eraser',
                        'pos': position,
                        'size': eraser_size
                    })
                
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw all saved points/shapes
        for i, point in enumerate(points):
            if point['type'] == 'separator':
                # Skip separators, they're just markers
                continue
            
            elif point['type'] == 'brush':
                # Draw brush strokes
                # Only connect if previous point exists, is also brush, and no separator between
                if i > 0 and points[i-1]['type'] == 'brush':
                    drawLineBetween(screen, i, points[i-1]['pos'], point['pos'], 
                                  point['radius'], point['mode'], point['color'])
                else:
                    # Single point or start of new stroke
                    pygame.draw.circle(screen, point['color'], point['pos'], point['radius'])
            
            elif point['type'] == 'eraser':
                # Draw eraser marks as black circles
                pygame.draw.circle(screen, (0, 0, 0), point['pos'], point['size'])
            
            elif point['type'] == 'rectangle':
                # Draw saved rectangle
                draw_rectangle(screen, point['start'], point['end'], point['color'])
            
            elif point['type'] == 'circle':
                # Draw saved circle
                draw_circle(screen, point['start'], point['end'], point['color'])
            
            elif point['type'] == 'square':
                # Draw saved square (equal width and height)
                draw_square(screen, point['start'], point['end'], point['color'])
            
            elif point['type'] == 'right_triangle':
                # Draw saved right triangle (90 degree angle at bottom-left)
                draw_right_triangle(screen, point['start'], point['end'], point['color'])
            
            elif point['type'] == 'equilateral_triangle':
                # Draw saved equilateral triangle (all sides equal)
                draw_equilateral_triangle(screen, point['start'], point['end'], point['color'])
            
            elif point['type'] == 'rhombus':
                # Draw saved rhombus (diamond shape with equal sides)
                draw_rhombus(screen, point['start'], point['end'], point['color'])
        
        # Draw shape preview while drawing
        if drawing_shape and shape_start:
            mouse_pos = pygame.mouse.get_pos()
            
            if tool == 'rectangle':
                draw_rectangle(screen, shape_start, mouse_pos, current_color)
            
            elif tool == 'circle':
                draw_circle(screen, shape_start, mouse_pos, current_color)
            
            elif tool == 'square':
                draw_square(screen, shape_start, mouse_pos, current_color)
            
            elif tool == 'right_triangle':
                draw_right_triangle(screen, shape_start, mouse_pos, current_color)
            
            elif tool == 'equilateral_triangle':
                draw_equilateral_triangle(screen, shape_start, mouse_pos, current_color)
            
            elif tool == 'rhombus':
                draw_rhombus(screen, shape_start, mouse_pos, current_color)
        
        # Draw eraser cursor
        if tool == 'eraser':
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, (100, 100, 100), mouse_pos, eraser_size, 1)
        
        # Draw instructions panel
        draw_instructions(screen, font, tool, mode, radius, eraser_size)
        
        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, color_mode, color):
    """Draw a smooth line between two points"""
    # Calculate line interpolation
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    # Draw smooth line with circles
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def draw_rectangle(screen, start, end, color):
    """Draw a rectangle from start to end point"""
    start_x, start_y = start
    end_x, end_y = end
    width = abs(end_x - start_x)
    height = abs(end_y - start_y)
    top_left_x = min(start_x, end_x)
    top_left_y = min(start_y, end_y)
    pygame.draw.rect(screen, color, (top_left_x, top_left_y, width, height), 2)


def draw_circle(screen, start, end, color):
    """Draw a circle with center at start and radius to end"""
    start_x, start_y = start
    end_x, end_y = end
    radius = int(((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5)
    if radius > 0:
        pygame.draw.circle(screen, color, (start_x, start_y), radius, 2)


def draw_square(screen, start, end, color):
    """Draw a square (equal width and height based on larger dimension)"""
    start_x, start_y = start
    end_x, end_y = end
    
    # Calculate side length as the maximum of width and height
    side = max(abs(end_x - start_x), abs(end_y - start_y))
    
    # Determine direction for square placement
    if end_x < start_x:
        side = -side
    
    pygame.draw.rect(screen, color, (start_x, start_y, side, side), 2)


def draw_right_triangle(screen, start, end, color):
    """Draw a right triangle with 90 degree angle at start point"""
    start_x, start_y = start
    end_x, end_y = end
    
    # Three points of right triangle:
    # 1. Bottom-left (start point)
    # 2. Bottom-right (end_x, start_y)
    # 3. Top-left (start_x, end_y)
    point1 = (start_x, start_y)
    point2 = (end_x, start_y)
    point3 = (start_x, end_y)
    
    pygame.draw.polygon(screen, color, [point1, point2, point3], 2)


def draw_equilateral_triangle(screen, start, end, color):
    """Draw an equilateral triangle (all sides equal length)"""
    start_x, start_y = start
    end_x, end_y = end
    
    # Calculate base width
    base_width = end_x - start_x
    
    # Height of equilateral triangle = base * sqrt(3) / 2
    height = int(abs(base_width) * math.sqrt(3) / 2)
    
    # Adjust height direction based on mouse position
    if end_y < start_y:
        height = -height
    
    # Three points of equilateral triangle:
    # 1. Bottom-left
    # 2. Bottom-right
    # 3. Top-center
    point1 = (start_x, start_y)
    point2 = (end_x, start_y)
    point3 = ((start_x + end_x) // 2, start_y + height)
    
    pygame.draw.polygon(screen, color, [point1, point2, point3], 2)


def draw_rhombus(screen, start, end, color):
    """Draw a rhombus (diamond shape with equal sides)"""
    start_x, start_y = start
    end_x, end_y = end
    
    # Calculate center point
    center_x = (start_x + end_x) // 2
    center_y = (start_y + end_y) // 2
    
    # Calculate half widths
    half_width = abs(end_x - start_x) // 2
    half_height = abs(end_y - start_y) // 2
    
    # Four points of rhombus:
    # Top, Right, Bottom, Left
    point1 = (center_x, start_y)  # Top
    point2 = (end_x, center_y)    # Right
    point3 = (center_x, end_y)    # Bottom
    point4 = (start_x, center_y)  # Left
    
    pygame.draw.polygon(screen, color, [point1, point2, point3, point4], 2)


def draw_instructions(screen, font, tool, mode, radius, eraser_size):
    """Draw instructions and current settings on screen"""
    instructions = [
        "Tools: [1]Brush [2]Rect [3]Circle [4]Square [5]RightTri [6]EquiTri [7]Rhombus [E]Eraser",
        "Colors: [R]ed [G]reen [B]lue [Y]ellow [P]urple [O]range [W]hite [K]Black",
        "Mouse: Left=Bigger Right=Smaller  [C]lear  [ESC]Exit",
        f"Current: {tool.upper().replace('_', ' ')} | Color: {mode.upper()} | Size: {radius if tool == 'brush' else eraser_size}"
    ]
    
    y_offset = 10
    for instruction in instructions:
        text = font.render(instruction, True, (200, 200, 200))
        screen.blit(text, (10, y_offset))
        y_offset += 18


main()
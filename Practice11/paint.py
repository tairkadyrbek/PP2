import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    # Brush settings
    radius = 15
    mode = 'blue'  # Current color mode
    tool = 'brush'  # Current tool: 'brush', 'rectangle', 'circle', 'eraser'
    points = []
    
    # For shape drawing
    shape_start = None  # Starting point for rectangle/circle
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
    font = pygame.font.SysFont("Arial", 16)
    
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
            
                # Color selection (original + new colors)
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
                
                # Start drawing shape (rectangle or circle)
                elif tool == 'rectangle' or tool == 'circle':
                    if event.button == 1:  # Left click to start shape
                        shape_start = event.pos
                        drawing_shape = True
            
            # Mouse button release - finish shape
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_shape and (tool == 'rectangle' or tool == 'circle'):
                    if event.button == 1:
                        shape_end = event.pos
                        # Save the shape as a special point
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
                start_x, start_y = point['start']
                end_x, end_y = point['end']
                width = abs(end_x - start_x)
                height = abs(end_y - start_y)
                top_left_x = min(start_x, end_x)
                top_left_y = min(start_y, end_y)
                pygame.draw.rect(screen, point['color'], 
                               (top_left_x, top_left_y, width, height), 2)
            
            elif point['type'] == 'circle':
                # Draw saved circle
                start_x, start_y = point['start']
                end_x, end_y = point['end']
                radius_calc = int(((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5)
                if radius_calc > 0:
                    pygame.draw.circle(screen, point['color'], 
                                     (start_x, start_y), radius_calc, 2)
        
        # Draw shape preview while drawing
        if drawing_shape and shape_start:
            mouse_pos = pygame.mouse.get_pos()
            if tool == 'rectangle':
                start_x, start_y = shape_start
                end_x, end_y = mouse_pos
                width = abs(end_x - start_x)
                height = abs(end_y - start_y)
                top_left_x = min(start_x, end_x)
                top_left_y = min(start_y, end_y)
                pygame.draw.rect(screen, current_color, 
                               (top_left_x, top_left_y, width, height), 2)
            
            elif tool == 'circle':
                start_x, start_y = shape_start
                end_x, end_y = mouse_pos
                radius_calc = int(((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5)
                if radius_calc > 0:
                    pygame.draw.circle(screen, current_color, 
                                     (start_x, start_y), radius_calc, 2)
        
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
    # Always use the solid color passed in (no gradient effect)
    
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


def draw_instructions(screen, font, tool, mode, radius, eraser_size):
    """Draw instructions and current settings on screen"""
    instructions = [
        "Tools: [1]Brush [2]Rectangle [3]Circle [E]Eraser",
        "Colors: [R]ed [G]reen [B]lue [Y]ellow [P]urple [O]range [W]hite [K]Black",
        "Mouse: Left=Bigger Right=Smaller  [C]lear  [ESC]Exit",
        f"Current: {tool.upper()} | Color: {mode.upper()} | Size: {radius if tool == 'brush' else eraser_size}"
    ]
    
    y_offset = 10
    for instruction in instructions:
        text = font.render(instruction, True, (200, 200, 200))
        screen.blit(text, (10, y_offset))
        y_offset += 20


main()
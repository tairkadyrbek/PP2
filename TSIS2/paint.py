import pygame
from datetime import datetime
from tools import draw_shape, flood_fill

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 640, 480
FPS = 60

# Colors
COLORS = {
    'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0),
    'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0),
    'purple': (128, 0, 128), 'orange': (255, 165, 0)
}

# Setup Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App - TSIS 2")

# Main Canvas (permanent drawings)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(COLORS['black'])

# Fonts
text_font = pygame.font.SysFont('Arial', 24)
ui_font = pygame.font.SysFont('Arial', 14)

def draw_ui(tool, color, size):
    """Draw instructions overlay"""
    instructions = [
        "Size: [1]Small [2]Med [3]Large | Draw: [4]Pencil [5]Line | [F]Fill [T]Text [E]Eraser",
        "Shapes: [6]Rect [7]Circle [8]Square [9]RightTri [0]EquiTri [-]Rhombus",
        "Colors: [R]ed [G]reen [B]lue [Y]ellow [P]urple [O]range [W]hite [K]Black",
        f"Tool: {tool.upper().replace('_', ' ')} | Color: {color} | Size: {size} | [Ctrl+S]Save [C]lear"
    ]
    y = 10
    for text in instructions:
        surf = ui_font.render(text, True, (200, 200, 200))
        screen.blit(surf, (10, y))
        y += 18

def main():
    clock = pygame.time.Clock()
    
    # State
    tool = 'pencil'
    color = 'blue'
    color_rgb = COLORS[color]
    sizes = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}
    size = 5
    
    drawing = False
    last_pos = None
    start_pos = None
    
    # Text tool
    typing = False
    text_input = ""
    text_pos = (0, 0)
    
    running = True
    while running:
        # Draw canvas base
        screen.blit(canvas, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Text input mode
                if typing:
                    if event.key == pygame.K_RETURN:
                        surf = text_font.render(text_input, True, color_rgb)
                        canvas.blit(surf, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            text_input += event.unicode
                    continue
                
                # Save
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    filename = f"canvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Saved: {filename}")
                
                # Clear
                if event.key == pygame.K_c and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    canvas.fill(COLORS['black'])
                
                # Exit
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Sizes
                if event.key in sizes:
                    size = sizes[event.key]
                
                # Tools
                tool_map = {
                    pygame.K_4: 'pencil', pygame.K_5: 'line', pygame.K_6: 'rectangle',
                    pygame.K_7: 'circle', pygame.K_8: 'square', pygame.K_9: 'right_triangle',
                    pygame.K_0: 'equilateral_triangle', pygame.K_MINUS: 'rhombus',
                    pygame.K_e: 'eraser', pygame.K_f: 'fill', pygame.K_t: 'text'
                }
                if event.key in tool_map:
                    tool = tool_map[event.key]
                
                # Colors
                color_map = {
                    pygame.K_r: 'red', pygame.K_g: 'green', pygame.K_b: 'blue',
                    pygame.K_y: 'yellow', pygame.K_p: 'purple', pygame.K_o: 'orange',
                    pygame.K_w: 'white', pygame.K_k: 'black'
                }
                if event.key in color_map and not (event.key == pygame.K_b and (pygame.key.get_mods() & pygame.KMOD_CTRL)):
                    if not (event.key == pygame.K_w and (pygame.key.get_mods() & pygame.KMOD_CTRL)):
                        color = color_map[event.key]
                        color_rgb = COLORS[color]
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tool == 'text':
                    typing = True
                    text_pos = event.pos
                    text_input = ""
                elif tool == 'fill':
                    flood_fill(canvas, event.pos, color_rgb)
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                drawing = False
                if tool == 'line':
                    pygame.draw.line(canvas, color_rgb, start_pos, event.pos, size)
                elif tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    draw_shape(canvas, color_rgb, start_pos, event.pos, tool, size)
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'pencil':
                    pygame.draw.line(canvas, color_rgb, last_pos, event.pos, size)
                    last_pos = event.pos
                elif tool == 'eraser':
                    pygame.draw.line(canvas, COLORS['black'], last_pos, event.pos, size)
                    last_pos = event.pos
        
        # Live preview
        if drawing and tool not in ['pencil', 'eraser']:
            mouse_pos = pygame.mouse.get_pos()
            if tool == 'line':
                pygame.draw.line(screen, color_rgb, start_pos, mouse_pos, size)
            elif tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                draw_shape(screen, color_rgb, start_pos, mouse_pos, tool, size)
        
        # Text preview
        if typing:
            surf = text_font.render(text_input + "|", True, color_rgb)
            screen.blit(surf, text_pos)
        
        # UI overlay
        draw_ui(tool, color, size)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
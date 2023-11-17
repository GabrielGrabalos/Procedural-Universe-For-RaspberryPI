import pygame
import sys
import panzoom
from star import Star
from name_generator import NameGenerator

pz = panzoom.PanZoom()

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
SCREEN = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Mouse Events")

# Variables for mouse position
mouse_x, mouse_y = 0, 0

CELL_SIZE = 40

star_to_be_selected = None
selected_star = None

def draw():
    draw_width = int(pz.ScreenToWorldX(width) / CELL_SIZE + CELL_SIZE)
    draw_height = int(pz.ScreenToWorldY(height) / CELL_SIZE + CELL_SIZE)

    global star_to_be_selected
    previous_star_to_be_selected = star_to_be_selected

    star_to_be_selected = None

    # Fill background
    SCREEN.fill((0, 0, 0))

    for x in range(int(pz.ScreenToWorldX(-1) / CELL_SIZE - CELL_SIZE), draw_width):
        for y in range(int(pz.ScreenToWorldY(-1) / CELL_SIZE - CELL_SIZE), draw_height):
            if randint(0, 20, (x & 0xFFFF) << 16 | (y & 0xFFFF)) == 1:
                star = Star(x, y)
                if star.draw(SCREEN, pz, pygame, CELL_SIZE, mouse_x, mouse_y):
                    if star_to_be_selected == None:
                        star_to_be_selected = star
                    elif previous_star_to_be_selected != star:
                        star_to_be_selected = star
    
    if star_to_be_selected != None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    

    # Update display
    pygame.display.flip()

def _xorshift32(state):
    state ^= (state << 13) & 0xFFFFFFFF
    state ^= (state >> 17) & 0xFFFFFFFF
    state ^= (state << 5) & 0xFFFFFFFF
    return state & 0xFFFFFFFF

def randint(a, b, seed):
    return a + _xorshift32(seed) % (b - a + 1)

# Initial draw
draw()

# Main game loop
running = True
clock = pygame.time.Clock()

drag_track = panzoom.Point(0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                pz.MouseDown(mouse_x, mouse_y)
                drag_track.x = pz.dragStart.x
                drag_track.y = pz.dragStart.y

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            pz.MouseMove(mouse_x, mouse_y)
            draw()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pz.dragStart.x == drag_track.x and pz.dragStart.y == drag_track.y:
                    if star_to_be_selected != None:

                        selected_star = star_to_be_selected
                        star_to_be_selected = None
                        
                        print(NameGenerator.generate(selected_star.randInt(2,3), selected_star))
                        draw()
                        selected_star.drawSys(SCREEN, pygame)
                        pygame.display.flip()

                    else:
                        selected_star = None
                        draw()

                pz.MouseUp()

        # mouse wheel was scrolled up or down
        elif event.type == pygame.MOUSEWHEEL:
            pz.MouseWheel(mouse_x, mouse_y, -event.y * 160)
            draw()

        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            SCREEN = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            draw()
    
    clock.tick(30)  # Limit to 30 FPS

# Quit Pygame
pygame.quit()
sys.exit()
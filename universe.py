import pygame
import sys
import panzoom

pz = panzoom.PanZoom()

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Mouse Events")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Variables for mouse position
mouse_x, mouse_y = 0, 0

# Main game loop
running = True
while running:
    # print(pz.OffsetX, pz.OffsetY, pz.Scale)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                pz.MouseDown(mouse_x, mouse_y)

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            pz.MouseMove(mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pz.MouseUp()

        # mouse wheel was scrolled up or down
        elif event.type == pygame.MOUSEWHEEL:
            pz.MouseWheel(mouse_x, mouse_y, -event.y * 100)

        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Clear the screen
    screen.fill(white)

    s = 40

    # Draw a grid
    # for x in range(0, int(width / pz.Scale), s):
    #     pygame.draw.line(screen, black, ((x - pz.OffsetX % s + s)
    #                      * pz.Scale, 0), ((x - pz.OffsetX % s + s)*pz.Scale, height))

    # for y in range(0, int(height / pz.Scale), s):
    #     pygame.draw.line(screen, black, (0, (y - pz.OffsetY % s + s)
    #                      * pz.Scale), (width, (y - pz.OffsetY % s + s)*pz.Scale))

    # Draw circles in the intersections
    for x in range(-s , int(width / pz.Scale) + s, s):
        for y in range(-s, int(height / pz.Scale) + s, s):
            pygame.draw.circle(screen, black, ((
                x - pz.OffsetX % s + s)*pz.Scale, (y - pz.OffsetY % s + s)*pz.Scale), 4 * pz.Scale)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

import pygame
import sys
import panzoom
import time

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


def draw():
    # Clear the screen
    screen.fill(white)

    s = 40

    # Draw circles in the intersections
    for x in range(-s, int(width / pz.Scale) + s, s):
        for y in range(-s, int(height / pz.Scale) + s, s):
            pygame.draw.circle(screen, black, ((
                x - pz.OffsetX % s + s)*pz.Scale, (y - pz.OffsetY % s + s)*pz.Scale), 4 * pz.Scale)

    # Update display
    pygame.display.flip()

def _xorshift32(state):
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= (state >> 17) & 0xFFFFFFFF
        state ^= (state << 5) & 0xFFFFFFFF
        return state & 0xFFFFFFFF

def randint(a, b, seed):
    return a + _xorshift32(seed) % (b - a + 1)
    #return math.floor(a + math.sin(a * 12.9898 + b * 78.233) * math.sin(seed) * 4358.254) % b


def drawRand():
    start_time = time.time()

    # Clear the screen
    pygame.draw.rect(screen, black, (0, 0, width, height))

    # for every pixel in the screen
    for x in range(0, width):
        for y in range(0, height):
            if (randint(0, 20, (x << 16) | y) == 1):
                # set the color of the pixel
                pygame.draw.rect(screen, white, (x, y, 1, 1))

    pygame.display.flip()

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


def display_time(elapsed_time):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Time taken: {elapsed_time} seconds", True, white)
    screen.blit(text, (10, 10))
    pygame.display.flip()


drawRand()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                elapsed_time = drawRand()
                display_time(elapsed_time)

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

    # draw()

# Quit Pygame
pygame.quit()
sys.exit()

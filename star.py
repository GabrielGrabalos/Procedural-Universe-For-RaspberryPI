import pygame
import panzoom as pz
from name_generator import NameGenerator

class Star:

    # Static array of colors:
    colors = [
        (255, 223, 186),  # Light Gold
        (255, 197, 143),  # Peach
        (255, 150, 128),  # Salmon
        (255, 87, 104),   # Coral
        (170, 77, 116),   # Mauve
        (131, 100, 121),  # Plum
        (88, 77, 109),    # Deep Purple
        (53, 92, 125)     # Steel Blue
    ]

    def __init__(self, x, y, generate_system=False):
        self.x = x
        self.y = y
        self.state = (x & 0xFFFF) << 16 | (y & 0xFFFF)

        # Atributes:
        self.color = Star.colors[self.randInt(0, len(Star.colors) - 1)]
        self.diameter = self.randFloat(1, 2.5)
        self.RAND_OFFSET = self.randFloat(0, 2)

        if generate_system == False:
           return
        
        # Generate star infos:
        self.name = NameGenerator.generate(self.state, self.randInt(2, 4))
        self.mass = self.randFloat(0.1, 10)
        self.radius = self.diameter * 300000
        self.temperature = self.randFloat(0.1, 10)
        self.luminosity = self.randFloat(0.1, 10)
        self.age = self.randFloat(0.1, 10)
        
        # Generate a system:
        self.planets = []

        # Generate a random number of planets:
        for i in range(self.randInt(1, 5)):
            self.planets.append(Planet(self.x, self.y, i))
        


    def draw(
        self,
        screen: pygame.Surface,
        pz: pz.PanZoom,
        pygame: pygame,
        CELL_SIZE: int,
        mouse_x: int,
        mouse_y: int
    ):
        draw_x = pz.WorldToScreenX((self.x + self.RAND_OFFSET) * CELL_SIZE) + CELL_SIZE
        draw_y = pz.WorldToScreenY((self.y + self.RAND_OFFSET) * CELL_SIZE) + CELL_SIZE

        pygame.draw.circle(
            screen, self.color, (
                draw_x,
                draw_y
            ),
            self.diameter * 3 * pz.Scale
        )

        #if the mouse is hovering the circle:
        if (mouse_x - draw_x)**2 + (mouse_y - draw_y)**2 - 2 * pz.Scale <= (self.diameter * 3 * pz.Scale)**2:
            pygame.draw.circle(
                screen, (255, 255, 255), (
                    draw_x,
                    draw_y
                ),
                self.diameter * 3 * pz.Scale + int(2 * pz.Scale), 2
            )

            return True
        
        return False

    def randInt(self, a, b):
        self.state ^= (self.state << 13) & 0xFFFFFFFF
        self.state ^= (self.state >> 17) & 0xFFFFFFFF
        self.state ^= (self.state << 5) & 0xFFFFFFFF
        return a + (self.state % (b - a + 1))

    def randFloat(self, a, b):
        self.state ^= (self.state << 13) & 0xFFFFFFFF
        self.state ^= (self.state >> 17) & 0xFFFFFFFF
        self.state ^= (self.state << 5) & 0xFFFFFFFF
        return a + (self.state & 0xFFFFFFFF) / 0xFFFFFFFF * (b - a)

    def random(self):
        self.state ^= (self.state << 13) & 0xFFFFFFFF
        self.state ^= (self.state >> 17) & 0xFFFFFFFF
        self.state ^= (self.state << 5) & 0xFFFFFFFF
        return self.state & 0xFFFFFFFF

import pygame
import panzoom as pz
from name_generator import NameGenerator
import locale

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
        self.name = NameGenerator.generate(self.randInt(2, 3), self)
        self.mass = self.randInt(100000, 100000000000)
        self.radius = self.diameter * 300000
        self.temperature = self.randInt(2000, 50000)
        self.luminosity = self.randFloat(0.1, 10)
        self.age = self.randFloat(0.1, 12)

        # Generate a system:
        self.planets = []

        # Generate a random number of planets:
        # for i in range(self.randInt(1, 5)):
        #    self.planets.append(Planet(self.x, self.y, i))

    def draw(
        self,
        screen: pygame.Surface,
        pz: pz.PanZoom,
        pygame: pygame,
        CELL_SIZE: int,
        mouse_x: int,
        mouse_y: int
    ):
        draw_x = pz.WorldToScreenX(
            (self.x + self.RAND_OFFSET) * CELL_SIZE) + CELL_SIZE
        draw_y = pz.WorldToScreenY(
            (self.y + self.RAND_OFFSET) * CELL_SIZE) + CELL_SIZE

        pygame.draw.circle(
            screen, self.color, (
                draw_x,
                draw_y
            ),
            self.diameter * 3 * pz.Scale
        )

        # if the mouse is hovering the circle:
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

    def hovering_star_on_sys(self, mouse_x, mouse_y, star_x, star_y, star_radius):
        return (mouse_x - star_x)**2 + (mouse_y - star_y)**2 <= star_radius**2 and mouse_y > star_y

    def draw_infos(self, mouse_x, mouse_y, screen, pygame, menu_border_radius, menu_background_color):
        mouse_x += 40
        # Define side menu parameters
        font_size = 20
        font = pygame.font.Font('dogicapixel.ttf', font_size)

        # Set locale to format numbers with commas
        locale.setlocale(locale.LC_ALL, '')  # Use the default locale

        # Define star infos
        star_info = [
            f"Name: {self.name}",
            f"Mass: {self.format_number(self.mass)} kg",
            f"Radius: {self.format_number(self.radius)} km",
            f"Temperature: {self.format_number(self.temperature)} °C",
            f"Luminosity: {self.format_number(self.luminosity)} LO",
            f"Age: {self.format_number(self.age)} billion years",
        ]

        # Calculate dynamic width and height for the menu
        max_text_width = max(font.size(line)[0] for line in star_info)
        menu_width = max_text_width + 40  # Add padding
        menu_height = len(star_info) * font_size + 40 + 20 * 5  # Add padding

        border_size = 10

        # Draw side menu background
        menu_rect = pygame.Rect(mouse_x, mouse_y, menu_width, menu_height)
        menu_border_rect = pygame.Rect(
            mouse_x - border_size, mouse_y - border_size, menu_width + border_size * 2,
            menu_height + border_size * 2)

        # Draw a border on the rectangle
        border_color = (0, 0, 70)  # Darker blue for the border
        pygame.draw.rect(screen, border_color, menu_border_rect,
                        border_radius=menu_border_radius + border_size)
        pygame.draw.rect(screen, menu_background_color,
                        menu_rect, border_radius=menu_border_radius)

        # Draw star infos
        text_y = menu_rect.y + 20
        for line in star_info:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (menu_rect.x + 20, text_y))
            text_y += font_size + 20

    def format_number(self, number):
        formatted_number = locale.format_string('%.2f', number, grouping=True)
        return formatted_number.rstrip("0").rstrip(",")



    def drawSys(
        self,
        screen: pygame.Surface,
        pygame: pygame,
        mouse_x: int,
        mouse_y: int
    ):
        # Define side menu parameters
        menu_width = screen.get_width() * 1 / 6 + 100
        menu_height = screen.get_height() - 40
        menu_rect = pygame.Rect(20, 20, menu_width, menu_height)
        menu_border_radius = 20
        menu_background_color = (0, 0, 139)  # Dark Blue

        # Draw side menu background
        pygame.draw.rect(screen, menu_background_color,
                         menu_rect, border_radius=menu_border_radius)

        # Draw star representation at the top of the side menu
        star_diameter = int(self.diameter * 50)
        star_radius = star_diameter // 2

        # Calculate the position of the semicircle (star) at the top, centered horizontally
        star_x = menu_rect.centerx
        star_y = menu_rect.y

        # Draw only half of the circle (bottom part):
        pygame.draw.circle(
            screen, self.color, (
                star_x,
                star_y
            ),
            star_radius,
            width=0,
            draw_bottom_right=True,
            draw_bottom_left=True
        )

        if self.hovering_star_on_sys(mouse_x, mouse_y, star_x, star_y, star_radius):
            pygame.draw.circle(
                screen, (255, 255, 255), (
                    star_x,
                    star_y
                ),
                star_radius + 2, 2,
                draw_bottom_right=True,
                draw_bottom_left=True
            )

            self.draw_infos(mouse_x, mouse_y, screen, pygame,
                            menu_border_radius, menu_background_color)

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

from name_generator import NameGenerator
import locale
from moon import Moon


class Planet:

    planet_colors = [
        (56, 26, 59),     # Dark Purple
        (86, 36, 78),     # Deep Plum
        (135, 80, 83),    # Dusty Rose
        (193, 133, 63),   # Terra Cotta
        (239, 185, 82),   # Mustard Yellow
        (156, 200, 134),  # Sage Green
        (102, 148, 196),  # Sky Blue
        (38, 79, 120)     # Dark Blue
    ]

    def __init__(self, rand_int, rand_float, index, star):
        self.color = self.planet_colors[rand_int(0, len(self.planet_colors)-1)]
        self.radius = rand_float(0.5, 2.0)
        self.distance = star.diameter * 50 + index * 50 + rand_int(0, 100)

        self.name = NameGenerator.generate(rand_int(2, 3), star)
        self.mass = rand_int(100, 100000)
        self.temperature = rand_int(200, 1000)
        self.age = rand_float(0.1, 5)

        if rand_float(0, 1) < 0.1:  # 10% chance for an older planet
            self.age = rand_float(5, 12)  # Adjust the range for older ages

        self.population = max(
            0, rand_int(-1000000000000 // (self.age * 20), 100000000000))

        self.moons = []

        for i in range(rand_int(0, 5)):
            self.moons.append(Moon(rand_int, rand_float, i, self, star))
            
            if i > 0:
                self.moons[i].distance = self.moons[i-1].distance + self.moons[i].radius * 2 + rand_int(10, 30)

    def hovering(self, mouse_x, mouse_y, menu_rect):
        planet_x = menu_rect.x + menu_rect.width / 2
        planet_y = menu_rect.y + self.distance

        return (mouse_x - planet_x)**2 + (mouse_y - planet_y)**2 <= (self.radius * 4 * 2)**2

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
            f"Temperature: {self.format_number(self.temperature)} °C",
            f"Age: {self.format_number(self.age)} billion years",
            f"Population: {self.format_number(self.population)} living beings"
        ]

        # Calculate dynamic width and height for the menu
        max_text_width = max(font.size(line)[0] for line in star_info)
        menu_width = max_text_width + 40  # Add padding
        menu_height = len(star_info) * font_size + 40 + 20 * 4  # Add padding

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

    def draw(self, screen, pygame, mouse_x, mouse_y, menu_rect, menu_border_radius, menu_background_color):
        planet_x = menu_rect.x + menu_rect.width / 2
        planet_y = menu_rect.y + self.distance

        pygame.draw.circle(
            screen, self.color, (
                planet_x,
                planet_y
            ),
            self.radius * 4 * 2
        )

        for moon in self.moons:
            moon.draw(screen, pygame, mouse_x, mouse_y, planet_x,
                      planet_y, menu_border_radius, menu_background_color)

        if self.hovering(mouse_x, mouse_y, menu_rect):
            pygame.draw.circle(
                screen, (255, 255, 255), (
                    planet_x,
                    planet_y
                ),
                self.radius * 4 * 2 + 2, 2
            )

            self.draw_infos(mouse_x, mouse_y, screen, pygame,
                            menu_border_radius, menu_background_color)

    def format_number(self, number):
        formatted_number = locale.format_string('%.2f', number, grouping=True)
        return formatted_number.rstrip("0").rstrip(",")

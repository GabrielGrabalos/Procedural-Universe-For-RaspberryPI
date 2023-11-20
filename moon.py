import locale
from name_generator import NameGenerator


class Moon:

    moon_colors = [
        (200, 200, 200),  # Light Gray
        (150, 150, 150),  # Medium Gray
        (100, 100, 100),  # Dark Gray
        (255, 255, 255),  # White
    ]

    def __init__(self, rand_int, rand_float, index, planet, star):
        self.color = self.moon_colors[rand_int(0, len(self.moon_colors) - 1)]
        self.radius = rand_float(0.3, 0.8)
        self.distance = planet.radius * 3 + 10 + rand_int(5, 10)

        self.name = NameGenerator.generate(rand_int(1, 2), star)
        self.mass = rand_int(10, 1000)
        self.temperature = rand_int(-100, 100)
        self.age = rand_float(0.01, 1)

    def hovering(self, mouse_x, mouse_y, planet_x, planet_y):
        moon_x = planet_x + self.distance
        moon_y = planet_y

        return (mouse_x - moon_x) ** 2 + (mouse_y - moon_y) ** 2 <= (self.radius * 4 * 2) ** 2

    def draw_infos(self, mouse_x, mouse_y, screen, pygame, menu_border_radius, menu_background_color):
        mouse_x += 40
        # Define side menu parameters
        font_size = 20
        font = pygame.font.Font('dogicapixel.ttf', font_size)

        # Set locale to format numbers with commas
        locale.setlocale(locale.LC_ALL, '')

        # Define star infos
        moon_info = [
            f"Name: {self.name}",
            f"Mass: {self.format_number(self.mass)} kg",
            f"Temperature: {self.format_number(self.temperature)} °C",
            f"Age: {self.format_number(self.age)} billion years",
        ]

        # Calculate dynamic width and height for the menu
        max_text_width = max(font.size(line)[0] for line in moon_info)
        menu_width = max_text_width + 40  # Add padding
        menu_height = len(moon_info) * font_size + 40 + 20 * 3  # Add padding

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
        for line in moon_info:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (menu_rect.x + 20, text_y))
            text_y += font_size + 20

    def draw(self, screen, pygame, mouse_x, mouse_y, planet_x, planet_y, menu_border_radius, menu_background_color):
        moon_x = planet_x + self.distance
        moon_y = planet_y

        pygame.draw.circle(
            screen, self.color, (
                int(moon_x),
                int(moon_y)
            ),
            int(self.radius * 4 * 2)
        )

        if self.hovering(mouse_x, mouse_y, planet_x, planet_y):
            pygame.draw.circle(
                screen, (255, 255, 255), (
                    int(moon_x),
                    int(moon_y)
                ),
                int(self.radius * 4 * 2) + int(2), 2
            )

            self.draw_infos(mouse_x, mouse_y, screen, pygame,
                            menu_border_radius, menu_background_color)

    def format_number(self, number):
        formatted_number = locale.format_string('%.2f', number, grouping=True)
        return formatted_number.rstrip("0").rstrip(",")

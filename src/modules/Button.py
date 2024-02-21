import pygame

class Button:

    def __init__(self, x, y, widthB, heightB, text, font_size, default_color, hover_color, text_color, screen):
        self.x = x
        self.y = y
        self.width = widthB
        self.height = heightB
        self.widthA = widthB
        self.heightA = heightB
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.default_color = default_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.screen = screen

    def draw(self, mouse_pos):
        elevate = 5
        subtraction = int(elevate/2)
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:

            self.width = self.widthA + elevate  # Aumenta a largura do botão
            self.height = self.heightA + elevate  # Aumenta a altura do botão
            pygame.draw.rect(self.screen, self.hover_color, (self.x - subtraction,
                                                             self.y - subtraction, self.width, self.height))

        else:
            self.width = self.widthA   # Aumenta a largura do botão
            self.height = self.heightA  # Aumenta a altura do botão
            pygame.draw.rect(self.screen, self.default_color, (self.x, self.y, self.width, self.height))

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.screen.blit(text_surface, text_rect)

    def clicked(self, mouse_pos):
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height

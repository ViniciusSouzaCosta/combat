import pygame


class ScreenManager:
    def __init__(self, width, height, caption, background_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.caption = caption
        self.background_color = background_color

        self.border_thickness = 15
        self.border_color = (255, 160, 122)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
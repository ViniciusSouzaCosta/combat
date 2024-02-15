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

    def clear_screen(self):
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, self.border_color, (0, 50, self.width, self.border_thickness))
        pygame.draw.rect(self.screen, self.border_color, (0, 50, self.border_thickness, self.height))
        pygame.draw.rect(self.screen, self.border_color, (0, self.height - self.border_thickness, self.width, self.border_thickness))
        pygame.draw.rect(self.screen, self.border_color, (self.width - self.border_thickness, 50, self.border_thickness, self.height))

    def draw_obstacles(self, obstacles_config):
        obstacle_color = (255, 160, 122)
        for obstacle_info in obstacles_config:
            x, y, size, shape = obstacle_info
            if shape == 'horizontal':
                pygame.draw.rect(self.screen, obstacle_color, (x, y, size, 30))
            elif shape == 'vertical':
                pygame.draw.rect(self.screen, obstacle_color, (x, y, 30, size))

    def check_collision(self, player_rect, obstacles_config):
        for obstacle_info in obstacles_config:
            x, y, size, shape = obstacle_info
            obstacle_rect = None
            if shape == 'horizontal':
                obstacle_rect = pygame.Rect(x, y, size, 30)
            elif shape == 'vertical':
                obstacle_rect = pygame.Rect(x, y, 30, size)
            
            if obstacle_rect:
                if player_rect.colliderect(obstacle_rect):
                    return True
        return False

    def update_screen(self):
        pygame.display.flip()

class BreakoutGame:
    def __init__(self):
        self.screen_manager = ScreenManager(1000, 625, "Combat", background_color=(51, 180, 51))
        self.clock = pygame.time.Clock()
        self.player_rect = pygame.Rect(100, 100, 50, 50)  # Exemplo de um jogador retangular
        self.player_speed = 5

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            player_rect_old_pos = self.player_rect.copy()  # Salva a posição anterior do jogador
            if keys[pygame.K_LEFT]:
                self.player_rect.x -= self.player_speed
                if self.player_rect.left < self.screen_manager.border_thickness:
                    self.player_rect.left = self.screen_manager.border_thickness
            if keys[pygame.K_RIGHT]:
                self.player_rect.x += self.player_speed
                if self.player_rect.right > self.screen_manager.width - self.screen_manager.border_thickness:
                    self.player_rect.right = self.screen_manager.width - self.screen_manager.border_thickness
            if keys[pygame.K_UP]:
                self.player_rect.y -= self.player_speed
                if self.player_rect.top < 50 + self.screen_manager.border_thickness:
                    self.player_rect.top = 50 + self.screen_manager.border_thickness
            if keys[pygame.K_DOWN]:
                self.player_rect.y += self.player_speed
                if self.player_rect.bottom > self.screen_manager.height - self.screen_manager.border_thickness:
                    self.player_rect.bottom = self.screen_manager.height - self.screen_manager.border_thickness

            obstacles_config = [
                (290, 327, 100, 'horizontal'),  # (x, y, size, shape)
                (475, 425, 110, 'vertical'),
                (600, 327, 100, 'horizontal'),
                (475, 150, 110, 'vertical'),
                (475, 595, 30, 'vertical'),
                (475, 50, 30, 'vertical'),
                (120, 270, 150, 'vertical'),
                (860, 270, 150, 'vertical'),
                (860, 270, 40, 'horizontal'),
                (860, 400, 40, 'horizontal'),
                (110, 270, 40, 'horizontal'),
                (110, 400, 40, 'horizontal'),
            ]

            # Verifica colisão com obstáculos
            if self.screen_manager.check_collision(self.player_rect, obstacles_config):
                self.player_rect = player_rect_old_pos  # Retorna o jogador para a posição anterior

            self.screen_manager.clear_screen()
            self.screen_manager.draw_obstacles(obstacles_config)
            pygame.draw.rect(self.screen_manager.screen, (255, 0, 0), self.player_rect)  # Desenha o jogador
            self.screen_manager.update_screen()

if __name__ == "__main__":
    pygame.init()
    game = BreakoutGame()
    game.run()
    pygame.quit()

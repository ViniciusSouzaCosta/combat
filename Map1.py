import pygame
import math

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

    def check_collision(self, rect, obstacles_config):
        for obstacle_info in obstacles_config:
            x, y, size, shape = obstacle_info
            obstacle_rect = None
            if shape == 'horizontal':
                obstacle_rect = pygame.Rect(x, y, size, 30)
            elif shape == 'vertical':
                obstacle_rect = pygame.Rect(x, y, 30, size)
            
            if obstacle_rect and rect.colliderect(obstacle_rect):
                return True
        return False

    def check_border_collision(self, rect):
        if rect.left <= self.border_thickness or rect.right >= self.width - self.border_thickness or \
           rect.top <= 50 + self.border_thickness or rect.bottom >= self.height - self.border_thickness:
            return True
        return False

    def update_screen(self):
        pygame.display.flip()

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = 10
        self.angle = angle
        self.ricochets = 0
        self.max_ricochets = 3

    def update(self):
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = -math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += dx
        self.rect.y += dy

        # Ricochet off the walls
        if self.rect.left <= 0 or self.rect.right >= 1000:
            self.angle = 180 - self.angle
            self.ricochets += 1
        if self.rect.top <= 50 or self.rect.bottom >= 625:
            self.angle = -self.angle
            self.ricochets += 1

        # Remove the bullet if it exceeds maximum ricochets
        if self.ricochets >= self.max_ricochets:
            return True

        return False

class BreakoutGame:
    def __init__(self):
        self.screen_manager = ScreenManager(1000, 625, "Combat", background_color=(51, 180, 51))
        self.clock = pygame.time.Clock()
        self.player_rect = pygame.Rect(100, 100, 50, 50)
        self.player_speed = 3
        self.rotation_angle = 0
        self.bullets = []

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shoot_bullet()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rotation_angle += 2
            if keys[pygame.K_RIGHT]:
                self.rotation_angle -= 2

            rotated_player_surf = pygame.Surface((self.player_rect.width, self.player_rect.height), pygame.SRCALPHA)
            rotated_player_surf.fill((255, 255, 255, 0))  # Fill with transparent background
            rotated_player_rect = rotated_player_surf.get_rect(center=self.player_rect.center)

            pygame.draw.rect(rotated_player_surf, (255, 0, 0), (0, 0, self.player_rect.width, self.player_rect.height))

            player_rect_old_pos = self.player_rect.copy()

            if keys[pygame.K_UP]:
                dx = math.cos(math.radians(self.rotation_angle)) * self.player_speed
                dy = -math.sin(math.radians(self.rotation_angle)) * self.player_speed
                new_rect = self.player_rect.move(dx, dy)  # Check collision before updating position
                if not self.screen_manager.check_collision(new_rect, obstacles_config) and \
                   not self.screen_manager.check_border_collision(new_rect):
                    self.player_rect = new_rect

            if keys[pygame.K_DOWN]:
                dx = -math.cos(math.radians(self.rotation_angle)) * self.player_speed
                dy = math.sin(math.radians(self.rotation_angle)) * self.player_speed
                new_rect = self.player_rect.move(dx, dy)  # Check collision before updating position
                if not self.screen_manager.check_collision(new_rect, obstacles_config) and \
                   not self.screen_manager.check_border_collision(new_rect):
                    self.player_rect = new_rect

            obstacles_config = [
                (290, 327, 100, 'horizontal'),
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

            self.update_bullets(obstacles_config)
            self.screen_manager.clear_screen()
            self.screen_manager.draw_obstacles(obstacles_config)
            rotated_player_surf = pygame.transform.rotate(rotated_player_surf, self.rotation_angle)
            self.screen_manager.screen.blit(rotated_player_surf, rotated_player_rect)
            self.draw_bullets()
            self.screen_manager.update_screen()

    def shoot_bullet(self):
        x = self.player_rect.centerx
        y = self.player_rect.centery
        angle = self.rotation_angle
        bullet = Bullet(x, y, angle)
        self.bullets.append(bullet)

    def update_bullets(self, obstacles_config):
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
            elif self.screen_manager.check_collision(bullet.rect, obstacles_config) or \
                 self.screen_manager.check_border_collision(bullet.rect):
                self.bullets.remove(bullet)

    def draw_bullets(self):
        for bullet in self.bullets:
            pygame.draw.rect(self.screen_manager.screen, (255, 255, 0), bullet.rect)

if __name__ == "__main__":
    pygame.init()
    game = BreakoutGame()
    game.run()
    pygame.quit()
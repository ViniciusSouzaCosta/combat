from random import randint
from secrets import choice
from typing import Sequence
import pygame
from config import Config
from modules.Ball import Ball
from modules.Brick import Brick
from modules.Coordinate import Coordinate
from modules.Dimension import Dimension
from modules.Screen import Screen

BRICK_POSITIONS = [
    [400, 180, 35, 80],
    [400, 475, 35, 80],
    [230, 325, 80, 30],
    [570, 325, 80, 30],
    [120, 325, 7, 110],
    [103, 278, 17, 17],
    [103, 371, 17, 17],
    [680, 325, 7, 110],
    [697, 278, 17, 17],
    [697, 371, 17, 17],
]


class Tank(pygame.sprite.Sprite):
    def __init__(self, coordinate: Coordinate, sprite_path: str, player: int):

        super(Tank, self).__init__()
        self.coordinate = coordinate
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.rect.center = (self.coordinate.x, self.coordinate.y)
        self.dimension = Dimension(self.rect.width, self.rect.height)
        self.range_allowed_x = list(
            range(21, Config.SCREEN_WIDTH - self.dimension.width + 1)
        )
        self.range_allowed_y = list(
            range(76, Config.SCREEN_HEIGHT - self.dimension.height + 1)
        )
        self.x_velocity = 1.0 
        self.y_velocity = 1.0  
        self.current_angle = 0.0  
        self.player = player

    def rotate(self, angle: float = 45): 
        if self.current_angle + angle >= 360:
            self.current_angle = 0
            return
        if self.current_angle + angle < 0:
            self.current_angle = 360 + (self.current_angle + angle)
        else:
            self.current_angle += angle

    def change_position(
        self,
    ):
        new_x = choice(self.range_allowed_x)
        new_y = choice(self.range_allowed_y)

        for brick_position in BRICK_POSITIONS:
            brick_x, brick_y, brick_width, brick_height = brick_position
            surface_colliding = (
                brick_x - self.dimension.width <= new_x <= brick_x + brick_width
            ) and (brick_y - self.dimension.height <= new_y <= brick_y + brick_height)
            if surface_colliding:
                return self.change_position()

        self.coordinate.x = new_x
        self.coordinate.y = new_y

    def move_up(self):
        if self.current_angle == 0.0 or self.current_angle == 360:
            self.x_velocity = 0
            self.y_velocity = -1
        elif self.current_angle == 45:
            self.y_velocity = -1
            self.x_velocity = -1
        elif self.current_angle == 90:
            self.x_velocity = -1
            self.y_velocity = 0
        elif self.current_angle == 135:
            self.x_velocity = -1
            self.y_velocity = 1
        elif self.current_angle == 180:
            self.x_velocity = 0
            self.y_velocity = 1
        elif self.current_angle == 225:
            self.x_velocity = 1
            self.y_velocity = 1
        elif self.current_angle == 270:
            self.x_velocity = 1
            self.y_velocity = 0
        elif self.current_angle == 315:
            self.x_velocity = 1
            self.y_velocity = -1

        self.coordinate.x += 1 * self.x_velocity
        self.coordinate.y += 1 * self.y_velocity

    def is_colliding(self, coordinate: Coordinate, dimension: Dimension) -> bool:
        x_colision = coordinate.x <= self.coordinate.x <= coordinate.x + dimension.width
        y_colision = (
            coordinate.y <= self.coordinate.y <= coordinate.y + dimension.height
        )

        x_final_colision = (
            coordinate.x
            <= self.coordinate.x + self.dimension.width
            <= coordinate.x + dimension.width
        )
        y_final_colision = (
            coordinate.y
            <= self.coordinate.y + self.dimension.height
            <= coordinate.y + dimension.height
        )

        return (
            (x_colision and y_colision)
            or (x_final_colision and y_final_colision)
            or (x_colision and y_final_colision)
            or (x_final_colision and y_colision)
        )

    def fire(self) -> Ball:
        ball_coordinate = Coordinate(
            self.coordinate.x + self.dimension.width / 2,
            self.coordinate.y + self.dimension.height / 2,
        )
        ball_dimension = Dimension(5, 5)
        return Ball(ball_coordinate, ball_dimension, self.current_angle, self.player)

    def draw(self, screen: Screen):  # TODO: Draw a tank
        screen.surface.blit(
            pygame.transform.rotate(self.image, self.current_angle),
            (self.coordinate.x, self.coordinate.y),
        )

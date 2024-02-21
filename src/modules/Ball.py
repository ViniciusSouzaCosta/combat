import pygame
from config import Config
from modules.Brick import Brick
from modules.Coordinate import Coordinate
from modules.Dimension import Dimension
from modules.Screen import Screen


class Ball:
    def __init__(
        self, coordinate: Coordinate, dimension: Dimension, angle: float, player: int
    ):
        self.coordinate = coordinate
        self.dimension = dimension
        self.hits = 0 
        self.player = player  
        self.angle = angle
        self.x_velocity = 1.0 
        self.y_velocity = 1.0 
        self.init_velocity()

    def init_velocity(self):
        if self.angle == 0.0 or self.angle == 360:
            self.x_velocity = 0
            self.y_velocity = -1
        elif self.angle == 45:
            self.y_velocity = -1
            self.x_velocity = -1
        elif self.angle == 90:
            self.x_velocity = -1
            self.y_velocity = 0
        elif self.angle == 135:
            self.x_velocity = -1
            self.y_velocity = 1
        elif self.angle == 180:
            self.x_velocity = 0
            self.y_velocity = 1
        elif self.angle == 225:
            self.x_velocity = 1
            self.y_velocity = 1
        elif self.angle == 270:
            self.x_velocity = 1
            self.y_velocity = 0
        elif self.angle == 315:
            self.x_velocity = 1
            self.y_velocity = -1

    def change_direction(
        self, brick: Brick
    ): 
        if self.coordinate.x == brick.coordinate.x:
            percents = (self.coordinate.y - brick.coordinate.y) / brick.dimension.height

            if percents > 0.5:
                self.x_velocity *= -1
                self.y_velocity = 1
            elif percents < 0.5:
                self.x_velocity *= -1
                self.y_velocity *= -1
            else:
                self.x_velocity = 0
                self.y_velocity *= -1

        elif self.coordinate.y == brick.coordinate.y:
            percents = (self.coordinate.x - brick.coordinate.x) / brick.dimension.width

            if percents > 0.5:
                self.x_velocity *= -1
                self.y_velocity *= -1
            elif percents < 0.5:
                self.x_velocity = 1
                self.y_velocity *= -1
            else:
                self.x_velocity = 0
                self.y_velocity *= -1

    def is_colliding(self, coordinate: Coordinate, dimension: Dimension) -> bool:
        x_colision = coordinate.x <= self.coordinate.x <= coordinate.x + dimension.width
        y_colision = (
            coordinate.y <= self.coordinate.y <= coordinate.y + dimension.height
        )
        return x_colision and y_colision

    def draw(self, screen: Screen):  # TODO: Fires at a coordinate
        from pygame import mixer

        mixer.init()

        self.coordinate.x += Config.BALL_DRAW_VELOCITY * self.x_velocity
        self.coordinate.y += Config.BALL_DRAW_VELOCITY * self.y_velocity
        pygame.draw.rect(
            screen.surface,
            Config.COLORS["BLACK"],
            (
                self.coordinate.x,
                self.coordinate.y,
                self.dimension.width,
                self.dimension.height,
            ),
        )

        if self.coordinate.y >= 572:
            self.y_velocity *= -1
            self.hits += 1


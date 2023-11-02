from dataclasses import dataclass


@dataclass()
class Color:
    gray: tuple = (97, 107, 150)
    field_color: tuple = (97, 107, 150)

    blue: tuple = (113, 91, 201)
    screen_color: tuple = (113, 91, 201)

    lime: tuple = (177, 242, 111)
    red: tuple = (252, 84, 84)
    lemon: tuple = (252, 250, 83)
    orange: tuple = (240, 165, 61)
    sky_blue: tuple = (86, 245, 222)
    purple: tuple = (205, 115, 237)

    white: tuple = (255, 255, 255)
    black: tuple = (0, 0, 0)
    green: tuple = (0, 255, 0)
    navy: tuple = (0, 0, 255)

    def __post_init__(self):
        self.figure_color = [
            self.lime,
            self.red,
            self.lemon,
            self.orange,
            self.sky_blue,
            self.purple
        ]
        for i in range(len(self.figure_color)):
            self.figure_color[i] = tuple(max(j - 90, 0) for j in self.figure_color[i])


@dataclass()
class InitData:
    WIDTH: int = 600
    HEIGHT: int = 700
    ELEM_SIZE: int = 50
    COUNT_CELLS: int = 8
    FPS: int = 30

    def __post_init__(self):
        self.START_FIELD_POSITION = [self.WIDTH // 2 - self.ELEM_SIZE * (self.COUNT_CELLS // 2), self.ELEM_SIZE // 2]

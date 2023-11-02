import pygame
from GameObjects import Elem, GameObject, Field
from random import choice
from typing import List


class Game:
    class __FigureList:
        __all_figures = {
            'O*1': [
                [[0, 0]]
            ],
            'O*2': [
                [[i, j] for i in range(2) for j in range(2)]
            ],
            'O*3': [
                [[i, j] for i in range(3) for j in range(3)]
            ],
            'J': [
                [[1, i] for i in range(3)] + [[0, 2]],
                [[0, i] for i in range(3)] + [[1, 0]],
                [[i, 0] for i in range(3)] + [[2, 1]],
                [[i, 1] for i in range(3)] + [[0, 0]]
            ],
            'CORNER*2': [
                [x for p, x in enumerate([[i, j] for i in range(2) for j in range(2)]) if p != z] for z in range(4)
            ],
            'CORNER*3': [
                [[z, i] for i in range(3)] + [[i, j] for i in range(1, 3)] for z in (0, 2) for j in (0, 2)
            ],
            'L': [
                [[0, i] for i in range(3)] + [[1, 2]],
                [[1, i] for i in range(3)] + [[0, 0]],
                [[i, 1] for i in range(3)] + [[2, 0]],
                [[i, 0] for i in range(3)] + [[0, 1]]
            ],
            'I*2': [
                [[0, i] for i in range(2)],
                [[i, 0] for i in range(2)]
            ],
            'I*3': [
                [[0, i] for i in range(3)],
                [[i, 0] for i in range(3)]
            ],
            'I*4': [
                [[0, i] for i in range(4)],
                [[i, 0] for i in range(4)]
            ],
            'I*5': [
                [[0, i] for i in range(5)],
                [[i, 0] for i in range(5)]
            ],
            'I*2*3': [
                [[i, j] for i in range(2) for j in range(3)],
                [[i, j] for i in range(3) for j in range(2)]
            ],
            'Z': [
                [[i + j, i] for i in range(2) for j in range(2)],
                [[i, 1 - i + j] for i in range(2) for j in range(2)]
            ],
            'S': [
                [[i, i + j] for i in range(2) for j in range(2)],
                [[1 - i + j, i] for i in range(2) for j in range(2)]
            ],
            'T': [
                [[0, i] for i in range(3)] + [[1, 1]],
                [[1, i] for i in range(3)] + [[0, 1]],
                [[i, 0] for i in range(3)] + [[1, 1]],
                [[i, 1] for i in range(3)] + [[1, 0]]
            ],
            'CROSS': [
                [[0, 0], [1, 1]],
                [[1, 0], [0, 1]]
            ]
        }

        @staticmethod
        def __random_color(colors: List[tuple]):
            return choice(colors)

        def __random_figure(self):
            return choice(self.__all_figures[choice(list(self.__all_figures))])

        def __init__(self, st_field: List[int], cnt_cells: int, elem_size: int, colors: List[tuple]):
            self.__new_figures = [
                Elem([st_field[0] + i * elem_size * 3, st_field[1] + int(elem_size * (cnt_cells + .5))],
                     self.__random_color(colors), self.__random_figure(), elem_size) for i in range(3)]
            self.__index = 0

        def __getitem__(self, item):
            return self.__new_figures[item]

        def __setitem__(self, key, value):
            self.__new_figures[key] = value

        def __iter__(self):
            self.__index = 0
            return self

        def __next__(self):
            if self.__index < len(self.__new_figures):
                res = self.__new_figures[self.__index]
                self.__index += 1
                return res
            else:
                raise StopIteration

        @property
        def is_empty(self) -> bool:
            return not any(self.__new_figures)

        def draw(self):
            for elem in self.__new_figures:
                if elem:
                    elem.draw()

        def index(self, elem: Elem) -> int:
            for i, j in enumerate(self.__new_figures):
                if j == elem:
                    return i
            return -1

    def __init__(self, screen_size: tuple, screen_color: tuple, start_field_pos: List[int], cnt_cells: int,
                 elem_size: int):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.__tick = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(screen_size)
        self.__screen_color = screen_color
        self.__field = None
        self.__figures = None
        self.__chosen_figure = None
        self.__flag = False
        self.figure_colors = []

        self.__elem_size = elem_size
        self.__st_field_pos = start_field_pos
        self.__cnt_cells = cnt_cells
        GameObject.set_screen(self.__screen)

    def create_field(self, field_color: tuple):
        # self.__field = Field(InitData().START_FIELD_POSITION, InitData.COUNT_CELLS, Game.__elem_size, field_color)
        self.__field = Field(self.__st_field_pos, self.__cnt_cells, self.__elem_size, field_color)

    def create_new_figures(self):
        self.__figures = Game.__FigureList(self.__st_field_pos, self.__cnt_cells, self.__elem_size, self.figure_colors)

    def fill_screen(self):
        self.__screen.fill(self.__screen_color)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if pygame.mouse.get_pressed()[0]:
            self.__flag = False
            if not self.__chosen_figure:
                for elem in self.__figures:
                    if not elem:
                        continue
                    if elem.is_in_the_area(pygame.mouse.get_pos()):
                        elem.position = list(pygame.mouse.get_pos())
                        self.__chosen_figure = elem.mouse_down()
                        break
            else:
                elem = self.__chosen_figure
                elem.position = list(pygame.mouse.get_pos())
                self.__chosen_figure = elem.mouse_down()
                self.__flag = elem in self.__field
                del elem
        elif self.__chosen_figure:
            elem = self.__chosen_figure
            if self.__flag:
                self.__field.put_elem(elem)
                self.__figures[self.__figures.index(elem)] = None
                del elem
                if self.__figures.is_empty:
                    self.create_new_figures()
            self.__chosen_figure.mouse_up()
            self.__chosen_figure = None

    def draw(self):
        self.fill_screen()
        self.__field.draw()
        self.__figures.draw()

    def run(self, fps: int):
        self.create_new_figures()
        while True:
            self.__tick.tick(fps)
            self.handle_event()
            self.draw()
            pygame.display.flip()

from math import ceil
from Sector import Sector
from typing import List


class GameObject:
    __screen = None

    def __init__(self, sectors: List[Sector], elem_size: int, color: tuple):
        self._sectors = sectors
        self._elem_size = elem_size
        self._color = color

    @staticmethod
    def set_screen(sc):
        GameObject.__screen = sc

    def draw(self):
        for sector in self._sectors:
            sector.draw_sector(GameObject.__screen)


class Elem(GameObject):
    def __init__(self, coord: list, color: tuple, figure: list, elem_size: int):
        self.__el_in_raw = max(figure, key=lambda l: l[0])[0] + 1  # element in raw
        self.__el_in_col = max(figure, key=lambda l: l[1])[1] + 1  # elements in column
        self.__size = elem_size * 2 // 5  # start size of sector
        self.__structure = figure
        self.position = [coord[0] + elem_size, coord[1] + elem_size]  # center location
        self.__initial_data = {
            'elem_size': self.__size,
            'location': self.position
        }
        super().__init__([Sector([self.position[0] + sector[0] * self.__size - self.__el_in_raw * self.__size // 2,
                                  self.position[1] + sector[1] * self.__size - self.__el_in_col * self.__size // 2],
                                 color, self.__size) for sector in figure], elem_size, color)  # __structure of the figure
        self.__index: int

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__structure):
            res = self.__structure[self.__index]
            self.__index += 1
            return res
        else:
            raise StopIteration

    @property
    def el_in_raw(self):
        return self.__el_in_raw

    @property
    def el_in_col(self):
        return self.__el_in_col

    @property
    def color(self):
        return self._color

    @property
    def X(self):
        return self.position[0]

    @property
    def Y(self):
        return self.position[1]

    def __update_sectors(self):
        for i in range(len(self._sectors)):
            self._sectors[i].position = [
                self.X + self.__structure[i][0] * self.__size - self.__el_in_raw * self.__size // 2,
                self.Y + self.__structure[i][1] * self.__size - self.__el_in_col * self.__size // 2]
            self._sectors[i].size = self.__size

    def mouse_down(self):
        self.__size = self._elem_size
        self.__update_sectors()
        return self

    def mouse_up(self):
        self.position = self.__initial_data['location']
        self.__size = self.__initial_data['elem_size']
        self.__update_sectors()

    def is_in_the_area(self, point_pos: tuple):
        return self.X - ceil(self.__el_in_raw / 2) * self.__size <= point_pos[0] <= self.X + \
               ceil(self.__el_in_raw / 2) * self.__size and \
               self.Y - ceil(self.__el_in_col / 2) * self.__size <= point_pos[1] <= self.Y + \
               ceil(self.__el_in_col / 2) * self.__size


class Field(GameObject):
    def __init__(self, start_position: list, cnt_cells: int, elem_size: int, color: tuple):
        # injection need!!!
        self.__start_position = start_position
        self.__cnt_cells = cnt_cells
        self.__field = [[Sector([start_position[0] + j * elem_size,
                                 start_position[1] + i * elem_size],
                                color, elem_size) for i in range(cnt_cells)] for j in range(cnt_cells)]
        super().__init__([i for j in self.__field for i in j], elem_size, color)

    def __contains__(self, elem: Elem) -> bool:
        x = (elem.X - self.__start_position[0]) // self._elem_size - elem.el_in_raw // 2
        y = (elem.Y - self.__start_position[1]) // self._elem_size - elem.el_in_col // 2
        flag = False
        for i in self.__field:
            for sec in i:
                sec.reset_color()
        if self._elem_size * self.__cnt_cells >= elem.Y - self.__start_position[1] >= 0 and \
                self._elem_size * self.__cnt_cells >= elem.X - self.__start_position[0] >= 0 and \
                x >= 0 and y >= 0:
            flag = True
            for i, j in elem:
                if i + x >= self.__cnt_cells or j + y >= self.__cnt_cells:
                    flag = False
                    break
                flag &= self.__field[i + x][j + y].is_empty
            if flag:
                shadow_color = tuple(max(el_color - 20, 0) for el_color in elem.color)
                for i, j in elem:
                    self.__field[i + x][j + y].color = shadow_color
                    self.__field[i + x][j + y].is_empty = False
                for i in range(self.__cnt_cells):
                    p_list = [self.__field[i][j] for j in range(self.__cnt_cells)]
                    if not any([x.is_empty for x in p_list]):
                        for j in p_list:
                            j.color = shadow_color
                    p_list = [self.__field[j][i] for j in range(self.__cnt_cells)]
                    if not any([x.is_empty for x in p_list]):
                        for j in p_list:
                            j.color = shadow_color

                for i, j in elem:
                    # self.__field[i + x][j + y].color = shadow_color
                    self.__field[i + x][j + y].is_empty = True
        return flag

    def put_elem(self, elem: Elem):
        x = (elem.X - self.__start_position[0]) // self._elem_size - elem.el_in_raw // 2
        y = (elem.Y - self.__start_position[1]) // self._elem_size - elem.el_in_col // 2
        for i, j in elem:
            self.__field[i + x][j + y].fill_sector(elem.color)

        # clean lines
        for i in range(self.__cnt_cells):
            p_list = [self.__field[i][j] for j in range(self.__cnt_cells)]
            delete_vertical = p_list.copy() if not any([x.is_empty for x in p_list]) else []
            p_list = [self.__field[j][i] for j in range(self.__cnt_cells)]
            delete_horizontal = p_list.copy() if not any([x.is_empty for x in p_list]) else []
            for j in delete_horizontal:
                j.empty_sector(self._color)
            for j in delete_vertical:
                j.empty_sector(self._color)

        for i in self.__field:
            for sec in i:
                sec.reset_color()

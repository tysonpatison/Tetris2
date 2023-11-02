from pygame import draw as pg_draw


class Sector:
    def __init__(self, coord: list, color: tuple, size):
        self.color = color
        self.position = coord
        self.is_empty = True
        self.size = size
        self.__initial_data = {
            'color': self.color
        }

    def draw_sector(self, sc):
        proportion = [5, 6]  # proprortion of center square to sector size
        gradient = [8, 16]
        x, y = self.position
        left_up = [x + self.size // proportion[1], y + self.size // proportion[1]]
        left_down = [x + self.size // proportion[1], y + proportion[0] * self.size // proportion[1]]
        right_up = [x + proportion[0] * self.size // proportion[1], y + self.size // proportion[1]]
        right_down = [x + proportion[0] * self.size // proportion[1],
                      y + proportion[0] * self.size // proportion[1]]
        corners = {
            'left_up': self.position,
            'left_down': [x, y + self.size],
            'right_down': [x + self.size, y + self.size],
            'right_up': [x + self.size, y]
        }
        pg_draw.rect(sc, self.color,
                     left_up + [(proportion[0] * 2 - proportion[1]) * self.size // proportion[1]] * 2)
        pg_draw.polygon(sc, tuple(min(gradient[1] + i, 255) for i in self.color), [
            corners['left_up'], left_up, right_up, corners['right_up']
        ])  # top
        pg_draw.polygon(sc, tuple(min(gradient[0] + i, 255) for i in self.color), [
            corners['left_up'], left_up, left_down, corners['left_down']
        ])  # left
        pg_draw.polygon(sc, tuple(max(-gradient[0] + i, 0) for i in self.color), [
            corners['left_down'], left_down, right_down, corners['right_down']
        ])  # bottom
        pg_draw.polygon(sc, tuple(max(-gradient[1] + i, 0) for i in self.color), [
            corners['right_up'], right_up, right_down, corners['right_down']
        ])  # right
        pg_draw.lines(sc, tuple(max(-50 + i, 0) for i in self.color), True, list(corners.values()))


    def reset_color(self):
        self.color = self.__initial_data['color']

    def fill_sector(self, color: tuple):
        self.__initial_data['color'] = color
        self.color = color
        self.is_empty = False

    def empty_sector(self, color: tuple):
        self.color = color
        self.__initial_data['color'] = self.color
        self.is_empty = True

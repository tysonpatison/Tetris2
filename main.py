from game import Game
from config import Color, InitData


if __name__ == "__main__":
    game = Game(
        (InitData.WIDTH, InitData.HEIGHT),
        Color.screen_color,
        InitData().START_FIELD_POSITION,
        InitData.COUNT_CELLS,
        InitData.ELEM_SIZE
    )
    game.create_field(Color.field_color)
    game.figure_colors = Color().figure_color
    game.run(InitData.FPS)

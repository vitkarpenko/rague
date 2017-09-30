"""Main config file.
"""
from pathlib import Path

from bearlibterminal import terminal as blt


BASE_FOLDER = Path(__file__).parent
DATA = BASE_FOLDER / 'data'
SCREEN_WIDTH, SCREEN_HEIGHT = 80, 50
SCREEN_CENTER_COORDINATES = (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)
TILESET_PATH = BASE_FOLDER / 'data' / 'tiles' / 'Cheepicus_12x12.png'


blt.open()
blt.set("U+E100: {}, size=12x12, align=top-left".format(TILESET_PATH))
blt.set("window: size={}x{}, "
        "cellsize=12x12, "
        "title='Rague'; "
        "font: default".format(SCREEN_WIDTH, SCREEN_HEIGHT))
blt.set("input.filter={keyboard+}")
blt.composition(True)
blt.refresh()

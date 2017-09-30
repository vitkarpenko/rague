"""Main config file.
"""
from pathlib import Path

from bearlibterminal import terminal as blt


BASE_FOLDER = Path(__file__).parent
DATA = BASE_FOLDER / 'data'
SCREEN_WIDTH, SCREEN_HEIGHT = 100, 40
SCREEN_CENTER_COORDINATES = (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)


blt.open()
blt.set("window: size={}x{}, "
        "cellsize=auto, "
        "title='Rague'; "
        "font: default".format(SCREEN_WIDTH, SCREEN_HEIGHT))
blt.set("input.filter={keyboard+}")
blt.composition(True)
blt.refresh()

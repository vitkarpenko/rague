""" Main config file.
"""
from pathlib import Path

from bearlibterminal import terminal as blt


blt.open()
blt.set("window: size=80x25, cellsize=auto, title='Rague'; font: default")
blt.set("input.filter={keyboard+}")
blt.composition(True)

BASE_FOLDER = Path(__file__).parent
DATA = BASE_FOLDER / 'data'

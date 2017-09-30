"""This module provides Map class which represent
a game world without entities.
"""
from collections import namedtuple
from pathlib import Path


Tile = namedtuple(
    'Tile',
    ['symbol',
     'color',
     'passable']
)


FLOOR = Tile(0xE100+(11*16+2), 0x22C3B091, True)
WALL = Tile(0xE100+(13*16+11), 0xBBFFFACD, False)
NOTHING = Tile(0xE100, 0x00000000, False)


class Map:
    """Instance is just a dict associating
    x, y coordinates with the type of terrain.

    'f': floor; passable, transparent.
    'w': wall; blocks movement and line of sight.
    """

    def __init__(self, filepath=None):
        self.tiles = dict()
        if not filepath:
            self.generate_map()
        else:
            self.load_from_file(filepath)

    def __getitem__(self, position):
        x, y = position
        return self.tiles.get((x, y), NOTHING)

    def __setitem__(self, position, value):
        x, y = position
        self.tiles[(x, y)] = value

    def __iter__(self):
        return iter(self.tiles)

    def generate_map(self):
        """Generates map randomly."""
        pass

    def load_from_file(self, filepath):
        """Loads map from file."""
        def set_tile(x, y, symbol):
            if symbol == '.':
                self[x, y] = FLOOR
            elif symbol == '#':
                self[x, y] = WALL
            else:
                raise ValueError('Incorrect value {} '
                                 'in mapfile {}!'.format(symbol, filepath))
        mapfile = Path(__file__).parent / filepath
        with mapfile.open() as data:
            for index_y, line in enumerate(data):
                for index_x, symbol in enumerate(line[:-1]):
                    set_tile(index_x, index_y, symbol)

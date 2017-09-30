"""This module provides Map class which represent
a game world without entities.
"""
from collections import namedtuple


Tile = namedtuple(
    'Tile',
    ['symbol',
     'color',
     'passable']
)


FLOOR = Tile('.', 0x66C3B091, True)
WALL = Tile('#', 0xBBFFFACD, False)


class Map:
    """Instance is just a dict associating
    x, y coordinates with the type of terrain.

    'f': floor; passable, transparent.
    'w': wall; blocks movement and line of sight.
    """

    def __init__(self):
        self.tiles = {
            (x, y): FLOOR
            for x in range(30)
            for y in range(30)
        }

        for y in range(15):
            self[10, y] = WALL

    def __getitem__(self, position):
        x, y = position
        return self.tiles[(x, y)]

    def __setitem__(self, position, value):
        x, y = position
        self.tiles[(x, y)] = value

    def __iter__(self):
        return iter(self.tiles)

    def passable(self, position):
        x, y = position
        return self[x, y].passable

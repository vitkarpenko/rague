"""This module provides Map class which represent
a game world without entities.
"""


class Map:
    """Instance is just a dict associating
    x, y coordinates with the type of terrain.

    'f': floor; passable, transparent.
    'w': wall; blocks movement and line of sight.
    """

    def __init__(self):
        self.tiles = {
            (x, y): 'f'
            for x in range(30)
            for y in range(30)
        }

        for y in range(15):
            self[10, y] = 'w'

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
        return self[x, y] in ['f']

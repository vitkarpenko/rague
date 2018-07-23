"""This module provides Map class which represent
a game world without entities.
"""
from collections import namedtuple
from itertools import product
from math import floor
from pathlib import Path
import random
from copy import deepcopy


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
        self.generator = MapGenerator(size=(100, 100))
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
        self.tiles = self.generator.generate()

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

    def drop_player(self):
        """Randomly generates coordinates to place player in a room."""
        # Tuple is used because random.choice does not support sets.
        room = random.choice(tuple(self.generator.rooms))
        while True:
            x, y = random.choice(room.tiles)
            if x in room.borders[0] or y in room.borders[1]:
                continue
            else:
                return x, y


class MapGenerator:
    """Generates self.tiles for Map."""
    def __init__(self, size):
        self.dungeon = dict()
        self.rows, self.cols = size
        # x, y - coords of the top-left corner
        self.rooms = set()

    def generate(self):
        for _ in range(1000):
            self.try_add_room()
        for room in self.rooms:
            self.carve_room(room)
        self.carve_maze()
        return self.dungeon

    def try_add_room(self):
        """Tries to add one none-overlapping room to dungeon.
        If fails, does nothing.
        """
        def rooms_not_overlap(room1, room2):
            return (
                room1.x > room2.x + room2.width
                or room1.x + room1.width < room2.x
                or room1.y > room2.y + room2.height
                or room1.y + room1.height < room2.y
            )
        x, y = random.randrange(self.cols), random.randrange(self.rows)
        width, height = floor(random.gauss(13, 2)), floor(random.gauss(13, 2))
        room = Room(x, y, width, height)
        if not self.rooms or all(
            rooms_not_overlap(room, existing_room)
            for existing_room in self.rooms
            ): self.rooms.add(room)

    def carve_room(self, room):
        """Actually creates walls and floor for a room."""
        for x, y in room.tiles:
            if x in room.borders[0] or y in room.borders[1]:
                self.dungeon[(x, y)] = WALL
            else:
                self.dungeon[(x, y)] = FLOOR

    def carve_maze(self):
        maze = Maze(self.rows, self.cols)
        for (x, y), tile in maze.generate().items():
            if tile == FLOOR:
                self.dungeon[(x, y)] = FLOOR
                for x, y in maze.adjacent_cells(x, y):
                    if 0 < x < self.rows and 0 < y < self.cols:
                        self.dungeon[(x, y)] = FLOOR
            if tile == WALL and not self.dungeon.get((x, y)) == FLOOR:
                self.dungeon[(x, y)] = WALL


class Room:
    """Represents a single room in a dungeon."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tiles = [
            (x, y)
            for x in range(self.x, self.x + self.width)
            for y in range(self.y, self.y + self.height)
        ]
        self.borders = (
            (self.x, self.x + self.width - 1),
            (self.y, self.y + self.height - 1)
        )

    def __repr__(self):
        return "Room x={} y={} width={} height={} borders={}".format(
            self.x, self.y,
            self.width, self.height,
            self.borders
        )


class Maze:
    """Generates a maze using recursive backtracking algorithm."""
    def __init__(self, width: int, length: int):
        self.width = width
        self.length = length
        self.maze = {(x, y): WALL for x, y in product(range(self.length), range(self.width))}
        self.visited = set()
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def generate(self):
        try:
            self.carve_maze_from(1, 1)
        finally:
            return self.maze

    def adjacent_cells(self, x, y):
        return (
            (x-1, y+1), (x, y+1), (x+1, y+1),
            (x-1, y),             (x+1, y),
            (x-1, y-1), (x, y-1), (x+1, y-1)
        )

    def _cell_is_valid(self, x, y):
        return (
            (x, y) not in self.visited
            and 0 < x < self.width
            and 0 < y < self.length
            and sum(self.maze.get((x, y)) == FLOOR for x, y in self.adjacent_cells(x, y)) < 4
        )

    def carve_maze_from(self, x, y):
        self.maze[(x, y)] = FLOOR
        self.visited.add((x, y))
        directions = deepcopy(self.directions)
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            valid = self._cell_is_valid(nx, ny)
            if valid:
                self.carve_maze_from(nx, ny)

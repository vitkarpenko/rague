"""This module contains main loop.
"""

from rague.config import blt
from rague.entities import *
from rague.components import *
from rague.map import Map
from rague.world import World


player = Player(Position(4, 6))
map_ = Map()
world = World(map_)
world.entities.add(player)
world.systems['Renderer'].evaluate()

while True:
    world.make_iteration()


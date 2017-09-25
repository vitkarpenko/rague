""" This module contains main loop.
"""

from rague.world import World
from rague.entities import *
from rague.config import blt


world = World()
player = Player()
world.entities.add(player)

while True:
    world.make_iteration()


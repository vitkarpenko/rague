""" This module contains main loop.
"""

from rague.world import World
from rague.config import blt


world = World()
while True:
    world.make_iteration()


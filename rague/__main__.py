""" This module contains main loop.
"""

from rague.world import World
from rague.entity import Entity
from rague.config import blt


world = World()
player = Entity('player/player')
world.entities.add(player)

while True:
    world.make_iteration()


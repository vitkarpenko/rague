"""This module contains main loop.
"""


from rague.components import *
from rague.entities import *
from rague.map import Map
from rague.world import World

# Some preparation.
dungeon = Map()
player_x, player_y = dungeon.drop_player()
player = Player(Position(player_x, player_y))
world = World(dungeon, player)
world.entities.add(player)
world.systems['Renderer'].evaluate()

while True:
    world.make_iteration()

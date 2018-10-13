""" Configuration for testing.
"""

import sys
from pathlib import Path

import pytest

from rague.components import *
from rague.entities import *
from rague.map import Map
from rague.world import World

sys.path.append(str(Path('../rague').resolve()))
print(Path('../rague').resolve())




@pytest.fixture
def dummy_entity():
    return Dummy()


@pytest.fixture
def player():
    return Player(Position(5, 5))


@pytest.fixture
def world(player):
    map_ = Map('data/maps/test.map')
    world = World(map_, player)
    return world

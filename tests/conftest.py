""" Configuration for testing.
"""

from pathlib import Path
import sys
sys.path.append(
    str(Path('../rague').resolve())
)
print(Path('../rague').resolve())

import pytest

from rague.entities import *
from rague.map import Map
from rague.components import *
from rague.world import World


@pytest.fixture
def dummy_entity():
    return Dummy()


@pytest.fixture
def player():
    return Player()


@pytest.fixture
def world():
    map_ = Map()
    world = World(map_)
    return world


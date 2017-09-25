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
from rague.components import *
from rague.world import World


@pytest.fixture
def dummy_entity():
    return Dummy()


@pytest.fixture
def player():
    return Player()


@pytest.fixture
def world(player):
    world = World()
    world.entities.add(player)
    return world


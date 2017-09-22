""" Configuration for testing.
"""

from pathlib import Path
import sys
sys.path.append(
    str(Path('../rague').resolve())
)
print(Path('../rague').resolve())

import pytest

from rague.entity import Entity
from rague.world import World


@pytest.fixture
def dummy_entity():
    return Entity('tests/dummy')


@pytest.fixture
def player():
    return Entity('player/player')


@pytest.fixture
def world(player):
    world = World()
    world.entities.add(player)
    return world


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


@pytest.fixture
def dummy_entity():
    return Entity('tests/dummy')

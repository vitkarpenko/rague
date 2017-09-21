""" This module implements various systems
which actually changes state of the world.
"""
from abc import ABC, abstractmethod

from rague.components import (
    Position,
    Velocity
)


class System(ABC):
    """ System iterates through entities every
    turn and does some action with them.
    """
    def __init__(self, world):
        self.world = world

    @abstractmethod
    def compute(self):
        """ Makes one turn of evaluation on a
        set of world entities. """

    @property
    @abstractmethod
    def requested_components(self):
        """ Returns set of set of component classes which
        entity must have to be ruled by this system.
        """


class Movement(System):
    """ Movement system which controls changing entitie's coordinates.
    """
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'Position', 'Velocity'}

    def move(self, entity):
        """ Actually changes entity coordinates.
        """
        for coordinate in ('x', 'y'):
            entity.components['Position'][coordinate] += entity.components['Velocity'][coordinate]

    def compute(self):
        for entity in self.world:
            if all(requested in entity.components
                   for requested in self.requested_components):
                self.move(entity)

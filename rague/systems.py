""" This module implements various systems
which actually changes state of the world.
"""
from abc import ABC, abstractmethod

from rague.config import blt


class System(ABC):
    """ System iterates through entities every
    turn and does some action with them.
    """
    def __init__(self, world):
        self.world = world

    @abstractmethod
    def evaluate(self):
        """ Makes one turn of evaluation on a
        set of world entities. """

    @property
    @abstractmethod
    def requested_components(self):
        """ Returns set of set of component classes which
        entity must have to be ruled by this system.
        """


class Movement(System):
    """ Controls changing entitie's coordinates.
    """
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'Position', 'Velocity'}

    def move(self, entity):
        """ Actually changes entity coordinates.
        """
        entity.components['Position'].x += entity.components['Velocity'].x
        entity.components['Position'].y += entity.components['Velocity'].y

    def evaluate(self):
        for entity in self.world.entities:
            if all(requested in entity.components
                   for requested in self.requested_components):
                self.move(entity)


class PlayerControl(System):
    """ Controls player character.
    """
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'Player'}

    def evaluate(self):
        while True:
            blt.clear()
            if blt.has_input():
                key = blt.read()
                blt.refresh()
                print(key)
                blt.delay(500)

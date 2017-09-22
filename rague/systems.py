""" This module implements various systems
which actually changes state of the world.
"""
from abc import ABC, abstractmethod, abstractproperty

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

    @abstractproperty
    def requested_components(self):
        """ Returns set of set of component classes which
        entity must have to be ruled by this system.
        """

    @property
    def affected_entities(self):
        return {
            entity
            for entity in self.world.entities
            if all(requested in entity.components
                   for requested in self.requested_components)
        }


class PlayerControl(System):
    """ Controls player character.
    """
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'Player'}

    def evaluate(self):
        # Player is always single.
        player = next(iter(self.affected_entities))

        if blt.has_input():
            key = blt.read()
            print(key)
            if key in (blt.TK_CLOSE, blt.TK_ESCAPE):
                exit(0)
            elif blt.state(blt.TK_UP):
                player.components['Velocity'].y += 1
            elif blt.state(blt.TK_RIGHT):
                player.components['Velocity'].x += 1
            elif blt.state(blt.TK_DOWN):
                player.components['Velocity'].y -= 1
            elif blt.state(blt.TK_LEFT):
                player.components['Velocity'].x -= 1
            blt.read()



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
        for entity in self.affected_entities:
            self.move(entity)
            entity.components['Velocity'].x = 0
            entity.components['Velocity'].y = 0

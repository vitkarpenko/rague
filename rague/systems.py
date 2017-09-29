"""This module implements various systems
which actually changes state of the world.
"""
from abc import ABC, abstractmethod, abstractproperty

from rague.config import blt


class System(ABC):
    """System iterates through entities every
    turn and does some action with them.
    """
    def __init__(self, world):
        self.world = world

    @abstractmethod
    def evaluate(self):
        """Makes one turn of evaluation on a
        set of world entities.
        """

    @abstractproperty
    def requested_components(self):
        """Returns set of set of component classes which
        entity must have to be ruled by this system.
        """

    @property
    def affected_entities(self):
        return {
            entity
            for entity in self.world.entities
            if all(requested in entity.__dict__
                   for requested in self.requested_components)
        }


class PlayerControl(System):
    """Controls player character."""
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'player_controlled'}

    def evaluate(self):
        # Player is always single.
        try:
            player = next(iter(self.affected_entities))
        except StopIteration:
            return

        key = blt.read()
        if key in (blt.TK_CLOSE, blt.TK_ESCAPE):
            exit(0)
        elif blt.state(blt.TK_UP):
            player.velocity.y -= 1
        elif blt.state(blt.TK_RIGHT):
            player.velocity.x += 1
        elif blt.state(blt.TK_DOWN):
            player.velocity.y += 1
        elif blt.state(blt.TK_LEFT):
            player.velocity.x -= 1
        else:
            # KeyError is handled in World
            # to ignore incorrect keypresses.
            raise KeyError


class Movement(System):
    """Controls changing entitie's coordinates."""
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'position', 'velocity'}

    def move(self, entity):
        """Actually changes entity coordinates.
        """
        entity.position.x += entity.velocity.x
        entity.position.y += entity.velocity.y

    def evaluate(self):
        for entity in self.affected_entities:
            self.move(entity)
            entity.velocity.x = 0
            entity.velocity.y = 0


class Renderer(System):
    """Draws on screen a map and entities."""
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'visible'}

    def evaluate(self):
        blt.clear()
        for x, y in self.world.map_:
            if self.world.map_[x, y] == 'f':
                blt.puts(x, y, '[color=gray].[/color]')
            else:
                blt.puts(x, y, '[color=gray]#[/color]')
        for entity in self.affected_entities:
            """blt.clear_area(
                entity.position.x - entity.velocity.x,
                entity.position.y - entity.velocity.y,
                1, 1
            )"""
            blt.puts(entity.position.x, entity.position.y, '[color=gray]{}[\color]'.format(entity.visible.symbol))
        blt.refresh()

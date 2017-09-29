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
        elif blt.state(blt.TK_UP) or blt.state(blt.TK_K):
            player.velocity.y -= 1
        elif blt.state(blt.TK_RIGHT) or blt.state(blt.TK_L):
            player.velocity.x += 1
        elif blt.state(blt.TK_DOWN) or blt.state(blt.TK_J):
            player.velocity.y += 1
        elif blt.state(blt.TK_LEFT) or blt.state(blt.TK_H):
            player.velocity.x -= 1
        else:
            # KeyError is handled in World
            # to ignore incorrect keypresses.
            raise KeyError


class Movement(System):
    """Controls changing entitie's coordinates.
    On every iteration pushes message
    'moved_coords' - list of 2-tuples which
    represents map coordinates that has been freed
    this turn - to world.messages.
    """
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'position', 'velocity'}

    def move(self, entity):
        """Actually changes entity coordinates.
        """
        if entity.velocity.x != 0 or entity.velocity.y != 0:
            self.moved_coords.append((entity.position.x, entity.position.y))
            entity.position.x += entity.velocity.x
            entity.position.y += entity.velocity.y

    def evaluate(self):
        self.moved_coords = []
        for entity in self.affected_entities:
            self.move(entity)
            entity.velocity.x = 0
            entity.velocity.y = 0
        self.world.messages['moved_coords'] = self.moved_coords


class Renderer(System):
    """Draws on screen a map and entities."""
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'visible'}

    def draw_map(self, x, y):
        if self.world.map_[x, y] == 'f':
            blt.puts(x, y, '[color=gray].[/color]')
        else:
            blt.puts(x, y, '[color=gray]#[/color]')

    def evaluate(self):
        for x, y in self.world.map_:
            self.draw_map(x, y)
        for entity in self.affected_entities:
            blt.puts(entity.position.x, entity.position.y, '[color=gray]{}[\color]'.format(entity.visible.symbol))
        for x, y in self.world.messages.get('moved_coords', []):
            blt.clear_area(x, y, 1, 1)
            self.draw_map(x, y)
        blt.refresh()

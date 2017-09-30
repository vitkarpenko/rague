"""This module implements various systems
which actually changes state of the world.
"""
from abc import ABC, abstractmethod, abstractproperty

from rague.config import blt
from rague.config import SCREEN_CENTER_COORDINATES


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
    """Controls changing entitie's coordinates."""
    def __init__(self, world):
        super().__init__(world)

    @property
    def requested_components(self):
        return {'position', 'velocity'}

    def move(self, entity):
        """Actually changes entity coordinates.
        """
        new_x = entity.position.x + entity.velocity.x
        new_y = entity.position.y + entity.velocity.y
        if self.world.map_[new_x, new_y].passable:
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
        return {'visual'}

    def draw_map(self, x, y):
        tile = self.world.map_[x, y]
        blt.color(tile.color)
        blt.puts(
            x, y,
            tile.symbol
        )

    def draw_entity(self, entity):
        blt.color(entity.visual.color)
        blt.clear_area(entity.position.x, entity.position.y, 1, 1)
        blt.puts(
            entity.position.x, 
            entity.position.y,
            entity.visual.symbol
        )

    def world_to_local_coords(self, x, y):
        return (
            SCREEN_CENTER_COORDINATES[0] + (x - player.position.x),
            SCREEN_CENTER_COORDINATES[1] + (y - player.position.y)
        )

    def evaluate(self):
        blt.clear()
        for x, y in self.world.map_:
            self.draw_map(x, y)
        for entity in self.affected_entities:
            self.draw_entity(entity)
        blt.refresh()

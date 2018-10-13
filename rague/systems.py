"""This module implements various systems
which actually changes state of the world.
"""
from abc import ABC, abstractmethod

from rague.config import (SCREEN_CENTER_COORDINATES, SCREEN_HEIGHT,
                          SCREEN_WIDTH, blt)


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

    @property
    @abstractmethod
    def requested_components(self):
        """Returns set of set of component classes which
        entity must have to be ruled by this system.
        """

    @property
    def affected_entities(self):
        return {
            entity
            for entity in self.world.entities
            if all(
                requested in entity.__dict__ for requested in self.requested_components
            )
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
        if self.world.dungeon[new_x, new_y].passable:
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

    def draw_map(self, x, y, x_shift, y_shift):
        """Coodrinates are shifted for centering camera on player."""
        tile = self.world.dungeon[x, y]
        x, y = (x + x_shift, y + y_shift)
        if x > SCREEN_WIDTH or y > SCREEN_WIDTH:
            return
        blt.color(tile.color)
        blt.put(x, y, tile.symbol)

    def draw_entity(self, entity, x_shift, y_shift):
        """Coodrinates are shifted  for centering camera on player."""
        x, y = (entity.position.x + x_shift, entity.position.y + y_shift)
        if x > SCREEN_WIDTH or y > SCREEN_WIDTH:
            return
        blt.color(entity.visual.color)
        blt.put(x, y, entity.visual.symbol)
        if entity == self.world.player:
            print('Player coords: {}, {}'.format(entity.position.x, entity.position.y))

    def evaluate(self):
        blt.clear()
        x_shift, y_shift = (
            int(SCREEN_CENTER_COORDINATES[0] - self.world.player.position.x),
            int(SCREEN_CENTER_COORDINATES[1] - self.world.player.position.y),
        )
        for x, y in self.world.dungeon:
            self.draw_map(x, y, x_shift, y_shift)
        for entity in self.affected_entities:
            self.draw_entity(entity, x_shift, y_shift)
        blt.refresh()

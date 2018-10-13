from rague.components import *

from .entity import Entity


class Player(Entity):
    components = {
        Position(),
        Velocity(),
        PlayerControlled(),
        Visual(0xE100 + 1, color=0xFFB0E0E6),
    }

from .entity import Entity
from rague.components import *


class Player(Entity):
    components = {
        Position(),
        Velocity(),
        PlayerControlled(),
        Visual(0xE100+(4*16), color=0xFFB0E0E6)
    }

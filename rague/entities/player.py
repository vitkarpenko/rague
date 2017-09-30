from .entity import Entity
from rague.components import *


class Player(Entity):
    components = {
        Position(),
        Velocity(),
        PlayerControlled(),
        Visual('@', color=0xFFB0E0E6)
    }

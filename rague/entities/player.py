from .entity import Entity
from rague.components import *


class Player(Entity):
    components = {
        Position(),
        Velocity(),
        PlayerControlled(),
        Visible('@')
    }

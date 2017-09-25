from .entity import Entity
from rague.components import *


class Dummy(Entity):
    components = {
        Position(),
        Velocity(1, 1),
    }

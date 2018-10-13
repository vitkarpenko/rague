from rague.components import *

from .entity import Entity


class Dummy(Entity):
    components = {Position(), Velocity(1, 1)}

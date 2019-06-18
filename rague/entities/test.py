from rague.components import Position, Velocity

from .entity import Entity


class Dummy(Entity):
    components = {Position(), Velocity(1, 1)}

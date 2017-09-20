""" This module contains all components definitions.
"""


class Component:
    """ Base class for all components.
    Provides some common utility methods.
    """
    pass


class Position(Component):
    """ Represents place in the world.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Velocity(Component):
    """ Represents current vector speed.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

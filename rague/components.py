"""This module contains all components definitions.
"""


class Component:
    """Base class for all components.
    Provides some common utility methods.
    """
    pass


class Position(Component):
    """Represents place in the world."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Velocity(Component):
    """Represents current vector speed."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class PlayerControlled(Component):
    """Indicates that entity is directly controlled by player."""
    def __init__(self):
        pass

class Visible(Component):
    """Shows how entity should be drawn on screen."""
    def __init__(self, symbol):
        self.symbol = symbol

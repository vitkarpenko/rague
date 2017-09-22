""" This module provides World class
used to control entities and systems.
World also used by systems as a communicator.
"""
from rague.systems import System


class World:
    """ self.entities: set of all entities in the world.
    """
    def __init__(self):
        self.entities = set()
        # Instantiating all systems.
        self.systems = [system(self) for system in System.__subclasses__()]

    def make_iteration(self):
        for system in self.systems:
            system.evaluate()
        

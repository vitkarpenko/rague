""" This module provides World class
used to control entities and systems.
World also used by systems as a communicator.
"""
from rague.systems import System


class World:
    """
    self.dungeon: instance of a Map class.
    self.entities: set of all entities in the world.
    self.messages: dict used by systems to exchange messages.
    """
    def __init__(self, dungeon, player):
        self.entities = set()
        self.messages = dict()
        # Instantiating all systems.
        self.systems = ({
            system.__name__: system(self)
            for system in System.__subclasses__()
        })
        self.systems_evaluation_order = [
            'PlayerControl',
            'Movement',
            'Renderer'
        ]
        self.dungeon = dungeon
        self.player = player

    def make_iteration(self):
        for system in self.systems_evaluation_order:
            try:
                self.systems[system].evaluate()
            except KeyError:
                # Don't do anything on incorrect input.
                # Such as F11 or releasing any key.
                return

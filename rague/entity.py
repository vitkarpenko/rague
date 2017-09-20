""" This module provides Entity class.
"""
import json
from pathlib import Path

from rague import (
    components,
    config
)


class Entity:
    """ Represents any in-game object.
    """
    def __init__(self, template_path):
        """ template: string containing path to
        JSON entity template (relative to data/entities folder)
        without and extension.

        Usage examples:
        Entity('enemies/crab')
        """
        self.components = set()

        with (config.DATA / 'entities' / (template_path + '.json')).open() as template_json:
            template = json.load(template_json)

        for component in template:
            try:
                component_class = getattr(components, component)
                component_instance = component_class.__init__(**template[component])
                self.components.update(component_instance)
            except AttributeError:
                raise AttributeError("Entity {} uses component "
                                     "{} which is not defined!".format(template_path, component))

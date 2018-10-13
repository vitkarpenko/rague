"""This module provides main Entity class
used as a base for all other entities (through
subclassing or instantiation).
"""
from copy import deepcopy

from rague.components import Component
from rague.utils import to_snake_case


class EntityMeta(type):
    """Every entity should declare a set of "components" instances
    which are used as a default values for instantiation.
    This metaclass turns this set into a dictionary
    for convenience.
    """

    def __new__(mcs, name, bases, attrs):
        if 'components' not in attrs:
            raise AttributeError(
                'Entity subclasses should declare a set of '
                'Components called "components".'
            )
        components_dict = {
            component.__class__.__name__: component for component in attrs['components']
        }
        attrs['components'] = components_dict
        clsobj = super().__new__(mcs, name, bases, attrs)
        return clsobj


class Entity(metaclass=EntityMeta):
    components = {}

    def __init__(self, *args):
        init_components = {
            component.__class__.__name__: component
            for component in args
            if isinstance(component, Component)
        }
        merged_components = {**deepcopy(self.components), **init_components}
        if not merged_components:
            return
        for key, val in merged_components.items():
            setattr(self, to_snake_case(key), val)

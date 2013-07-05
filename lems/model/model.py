"""
Model storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import os
from os.path import dirname

from lems.base import LEMSBase
from lems.util import Map, make_id
from lems.parser import LEMSFileParser
from lems.errors import ModelError

class Model(LEMSBase):
    """
    Stores a model.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        
        self.targets = list()
        """ List of targets to be run on startup.
        @type: list(str) """
        
        self.dimensions = Map()
        """ Dictionary of dimensions defined in the model.
        @type: dict(str -> lems.model.fundamental.Dimension """
        
        self.units = Map()
        """ Map of units defined in the model.
        @type: dict(str -> lems.model.fundamental.Unit """
        
        self.component_types = Map()
        """ Map of component types defined in the model.
        @type: dict(str -> lems.model.component.ComponentType) """
        
        self.components = Map()
        """ Map of root components defined in the model.
        @type: dict(str -> lems.model.component.Component) """

        self.constants = Map()
        """ Map of constants in this component type.
        @type: dict(str -> lems.model.component.Constant) """

        self.include_directories = []
        """ List of include directories to search for included LEMS files.
        @type: list(str) """

    def add_target(self, target):
        """
        Adds a simulation target to the model.

        @param target: Name of the component to be added as a
        simulation target.
        @type target: str
        """
        
        self.targets.append(target)
        
    def add_dimension(self, dimension):
        """
        Adds a dimension to the model.

        @param dimension: Dimension to be added.
        @type dimension: lems.model.fundamental.Dimension
        """

        self.dimensions[dimension.name] = dimension

    def add_unit(self, unit):
        """
        Adds a unit to the model.

        @param unit: Unit to be added.
        @type unit: lems.model.fundamental.Unit
        """

        self.units[unit.symbol] = unit

    def add_component_type(self, component_type):
        """
        Adds a component type to the model.

        @param component_type: Component type to be added.
        @type component_type: lems.model.fundamental.ComponentType
        """

        self.component_types[component_type.name] = component_type

    def add_component(self, component):
        """
        Adds a component to the model.

        @param component: Component to be added.
        @type component: lems.model.fundamental.Component
        """

        self.components[component.id] = component

    def add_constant(self, constant):
        """
        Adds a paramter to the model.

        @param constant: Constant to be added.
        @type constant: lems.model.component.Constant
        """

        self.constants[constant.name] = constant

    def add(self, child):
        """
        Adds a typed child object to the model.

        @param child: Child object to be added.
        """

        if isinstance(child, Dimension):
            self.add_dimension(child)
        elif isinstance(child, Unit):
            seld.add_unit(child)
        elif isinstance(child, ComponentType):
            self.add_component_type(child)
        elif isinstance(child, Component):
            self.add_component(child)
        elif isinstance(child, Constant):
            self.add_constant(child)
        else:
            raise ModelError('Unsupported child element')

    def add_include_directory(self, path):
        self.include_directories.append(path)

    def include_file(self, path, include_dirs = []):
        inc_dirs = include_dirs if include_dirs else self.include_dirs

        parser = LEMSFileParser(self, inc_dirs)
        if os.access(path, os.F_OK):
           parser.parse(open(path).read()) 
           return
        else:
            for inc_dir in inc_dirs:
                new_path = (inc_dir + '/' + path)
                if os.access(new_path, os.F_OK):
                    parser.parse(open(new_path).read())
                    return
        raise Exception('Unable to open ' + path)
            
    def import_from_file(self, filepath):
        inc_dirs = self.include_directories.copy()
        inc_dirs.append(dirname(filepath))
                        
        parser = LEMSFileParser(self, inc_dirs)
        with open(filepath) as f:
            parser.parse(f.read())
        
    def export_to_file(self, filepath):
        pass

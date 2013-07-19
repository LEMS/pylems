"""
Model storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import os
from os.path import dirname

from lems.base import LEMSBase
from lems.util import Map, make_id, merge_maps, merge_lists
from lems.parser import LEMSFileParser
from lems.errors import ModelError

from lems.model.fundamental import Dimension,Unit
from lems.model.component import Component,ComponentType,Constant

import xml.etree.ElementTree as xe

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
        """
        Adds a directory to the include file search path.

        @param path: Directory to be added.
        @type path: str
        """
        
        self.include_directories.append(path)

    def include_file(self, path, include_dirs = []):
        """
        Includes a file into the current model.

        @param path: Path to the file to be included.
        @type path: str

        @param include_dirs: Optional alternate include search path.
        @type include_dirs: list(str)
        """
        
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
        """
        Import a model from a file.

        @param filepath: File to be imported.
        @type filepath: str
        """
        
        inc_dirs = self.include_directories.copy()
        inc_dirs.append(dirname(filepath))
                        
        parser = LEMSFileParser(self, inc_dirs)
        with open(filepath) as f:
            parser.parse(f.read())
        
    def export_to_file(self, filepath, level_prefix = '  '):
        """
        Exports this model to a file.

        @param filepath: File to be exported to.
        @type filepath: str
        """

        xmlstr = '<Lems>\n'

        for target in self.targets:
            xmlstr += level_prefix + '<Target component="{0}"/>\n'.format(target)

        """
        for dimension in self.dimensions:
            xmlstr += dimension.toxml()
            
        for unit in self.units:
            xmlstr += unit.toxml()
            
        for component_type in self.component_types:
            xmlstr += component_type.toxml()
            
        for component in self.components:
            xmlstr += component.toxml()
            
        for constant in self.constants:
            xmlstr += constant.toxml()
        """    
        xmlstr += '</Lems>'

        print(xmlstr)


    def resolve(self):
        """
        Resolves references in this model.
        """

        model = self.copy()
        
        for ct in model.component_types:
            model.resolve_component_type(ct)

        return model

    def resolve_component_type(self, component_type):
        """
        Resolves references in the specified component type.

        @param component_type: Component type to be resolved.
        @type component_type: lems.model.component.ComponentType
        """

        #print(component_type.name, component_type.extends)
        
        # Resolve component type from base types if present.
        if component_type.extends:
            try:
                base_ct = self.component_types[component_type.extends]
            except:
                raise ModelError("Component type '{0}' trying to extend unknown component type '{1}'",
                                 component_type.name, component_type.extends)

            self.resolve_component_type(base_ct)
            self.merge_component_types(component_type, base_ct)
            component_type.extends = None

        

    def merge_component_types(self, ct, base_ct):
        """
        Merge various maps in the given component type from a base 
        component type.

        @param ct: Component type to be resolved.
        @type ct: lems.model.component.ComponentType

        @param base_ct: Component type to be resolved.
        @type base_ct: lems.model.component.ComponentType
        """

        merge_maps(ct.parameters, base_ct.parameters)
        merge_maps(ct.constants, base_ct.constants)
        merge_maps(ct.exposures, base_ct.exposures)
        merge_maps(ct.requirements, base_ct.requirements)
        merge_maps(ct.children, base_ct.children)
        merge_maps(ct.texts, base_ct.texts)
        merge_maps(ct.links, base_ct.links)
        merge_maps(ct.paths, base_ct.paths)
        merge_maps(ct.event_ports, base_ct.event_ports)
        merge_maps(ct.component_references, base_ct.component_references)
        merge_maps(ct.attachments, base_ct.attachments)

        merge_maps(ct.dynamics.state_variables, base_ct.dynamics.state_variables)
        merge_maps(ct.dynamics.derived_variables, base_ct.dynamics.derived_variables)
        merge_maps(ct.dynamics.time_derivatives, base_ct.dynamics.time_derivatives)
        merge_lists(ct.dynamics.event_handlers, base_ct.dynamics.event_handlers)
        merge_maps(ct.dynamics.kinetic_schemes, base_ct.dynamics.kinetic_schemes)
        
        merge_lists(ct.structure.event_connections, base_ct.structure.event_connections)
        merge_lists(ct.structure.child_instances, base_ct.structure.child_instances)
        merge_lists(ct.structure.multi_instantiates, base_ct.structure.multi_instantiates)

        merge_maps(ct.simulation.runs, base_ct.simulation.runs)
        merge_maps(ct.simulation.records, base_ct.simulation.records)
        merge_maps(ct.simulation.data_displays, base_ct.simulation.data_displays)
        merge_maps(ct.simulation.data_writers, base_ct.simulation.data_writers)

"""
Model storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import os
from os.path import dirname

from lems.base.base import LEMSBase
from lems.base.util import make_id, merge_maps, merge_lists
from lems.base.map import Map
from lems.parser.LEMS import LEMSFileParser
from lems.base.errors import ModelError

from lems.model.fundamental import Dimension,Unit
from lems.model.component import Constant,ComponentType,Component,FatComponent

import xml.dom.minidom as minidom

import re

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

        self.fat_components = Map()
        """ Map of root fattened components defined in the model.
        @type: dict(str -> lems.model.component.FatComponent) """

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

    def add_fat_component(self, fat_component):
        """
        Adds a fattened component to the model.

        @param fat_component: Fattened component to be added.
        @type fat_component: lems.model.fundamental.Fat_component
        """

        self.fat_components[fat_component.id] = fat_component

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
            self.add_unit(child)
        elif isinstance(child, ComponentType):
            self.add_component_type(child)
        elif isinstance(child, Component):
            self.add_component(child)
        elif isinstance(child, FatComponent):
            self.add_fat_component(child)
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

        xmlstr = '<Lems>'

        for target in self.targets:
            xmlstr += '<Target component="{0}"/>'.format(target)

        for dimension in self.dimensions:
            xmlstr += dimension.toxml()
            
        for unit in self.units:
            xmlstr += unit.toxml()
            
        for constant in self.constants:
            xmlstr += constant.toxml()
            
        for component_type in self.component_types:
            xmlstr += component_type.toxml()
            
        for component in self.components:
            xmlstr += component.toxml()
            
        xmlstr += '</Lems>'

        xmlstr = minidom.parseString(xmlstr).toprettyxml(level_prefix, '\n',)

        with open(filepath, 'w') as f:
            f.write(xmlstr)

    def resolve(self):
        """
        Resolves references in this model.
        """

        model = self.copy()
        
        for ct in model.component_types:
            model.resolve_component_type(ct)

        for c in model.components:
            if c.id not in model.fat_components:
                model.add(model.fatten_component(c))

        for c in ct.constants:
            c2 = c.copy()
            c2.numeric_value = model.get_numeric_value(c2.value, c2.dimension)
            model.add(c2)
            
        return model

    def resolve_component_type(self, component_type):
        """
        Resolves references in the specified component type.

        @param component_type: Component type to be resolved.
        @type component_type: lems.model.component.ComponentType
        """

        # Resolve component type from base types if present.
        if component_type.extends:
            try:
                base_ct = self.component_types[component_type.extends]
            except:
                raise ModelError("Component type '{0}' trying to extend unknown component type '{1}'",
                                 component_type.name, component_type.extends)

            self.resolve_component_type(base_ct)
            self.merge_component_types(component_type, base_ct)
            component_type.types = set.union(component_type.types, base_ct.types)
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

    def fatten_component(self, c):
        """
        Fatten a component but resolving all references into the corresponding component type.

        @param c: Lean component to be fattened.
        @type c: lems.model.component.Component

        @return: Fattened component.
        @rtype: lems.model.component.FatComponent
        """

        try:
            ct = self.component_types[c.type]
        except:
            raise ModelError("Unable to resolve type '{0}' for component '{1}'",
                             c.type, c.id)
        
        fc = FatComponent(c.id, c.type)

        ### Resolve parameters
        for parameter in ct.parameters:
            if parameter.name in c.parameters:
                p = parameter.copy()
                p.value = c.parameters[parameter.name]
                p.numeric_value = self.get_numeric_value(p.value, p.dimension)
                fc.add_parameter(p)
            else:
                raise ModelError("Parameter '{0}' not initialized for component '{1}'",
                                 parameter.name, c.id)

        ### Resolve constants
        for constant in ct.constants:
            constant2 = constant.copy()
            constant2.numeric_value = self.get_numeric_value(constant2.value, constant2.dimension)
            fc.add(constant2)

        ### Resolve texts
        for text in ct.texts:
            t = text.copy()
            t.value = c.parameters[text.name] if text.name in c.parameters else ''
            fc.add(t)
                
        ### Resolve texts
        for link in ct.links:
            if link.name in c.parameters:
                l = link.copy()
                l.value = c.parameters[link.name]
                fc.add(l)
            else:
                raise ModelError("Link parameter '{0}' not initialized for component '{1}'",
                                 link.name, c.id)
                
        ### Resolve paths
        for path in ct.paths:
            if path.name in c.parameters:
                p = path.copy()
                p.value = c.parameters[path.name]
                fc.add(p)
            else:
                raise ModelError("Path parameter '{0}' not initialized for component '{1}'",
                                 path.name, c.id)

        ### Resolve component references.
        for cref in ct.component_references:
            if cref.name in c.parameters:
                cref2 = cref.copy()
                cid = c.parameters[cref.name]

                if cid not in self.fat_components:
                    self.add(self.fatten_component(self.components[cid]))

                cref2.referenced_component = self.fat_components[cid]
                fc.add(cref2)
            else:
                raise ModelError("Component reference '{0}' not initialized for component '{1}'",
                                 cref.name, c.id)
            
        merge_maps(fc.exposures, ct.exposures)
        merge_maps(fc.requirements, ct.requirements)
        merge_maps(fc.children, ct.children)
        merge_maps(fc.texts, ct.texts)
        merge_maps(fc.links, ct.links)
        merge_maps(fc.paths, ct.paths)
        merge_maps(fc.event_ports, ct.event_ports)
        merge_maps(fc.attachments, ct.attachments)

        fc.dynamics = ct.dynamics.copy()
        fc.structure = ct.structure.copy()
        fc.simulation = ct.simulation.copy()

        fc.types = ct.types

        ### Resolve children
        for child in c.children:
            fc.add(self.fatten_component(child))

        return fc

    def get_numeric_value(self, value_str, dimension = None):
        """
        Get the numeric value for a parameter value specification.

        @param value_str: Value string
        @type value_str: str

        @param dimension: Dimension of the value
        @type dimension: str
        """

        bitsnum = re.split('[_a-zA-Z]+', value_str)
        bitsalpha = re.split('[^_a-zA-Z]+', value_str)

        n = float(bitsnum[0].strip())
        bitsnum = bitsnum[1:]
        bitsalpha = bitsalpha[1:]
        s = ''

        l = max(len(bitsnum), len(bitsalpha))
        for i in range(l):
            if i < len(bitsalpha):
                s += bitsalpha[i].strip()
            if i < len(bitsnum):
                s += bitsnum[i].strip()
        
        #number = float(re.split('[_a-zA-Z]+', parameter.value)[0].strip())
        #sym = re.split('[^_a-zA-Z]+', parameter.value)[1].strip()

        number = n
        sym = s

        numeric_value = None

        if sym == '':
            numeric_value = number
        else:
            if sym in self.units:
                unit = self.units[sym]

                if dimension:
                    if dimension != unit.dimension and dimension != '*':
                        raise SimBuildError("Unit symbol '{0}' cannot "
                                            "be used for dimension '{1}'",
                                            sym, dimension)
                else:
                    dimension = unit.dimension

                numeric_value = number * (10 ** unit.power)
            else:
                raise SimBuildError("Unknown unit symbol '{0}'",
                                    sym)
        return numeric_value

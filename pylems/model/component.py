"""
Types for component types and components

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.model.parameter import ParameterType,Parameter

class ComponentType(PyLEMSBase):
    """
    Stores the specification of a user-defined component type.
    """
    
    def __init__(self, name, extends = None):
        """
        Constructor

        @param name: Name of this component type.
        @type name: string

        @param extends: Base component type extended by this type.
        @type extends: pylems.model.component.ComponentType
        """

        self.name = name
        """ Name of this component type.
        @type: string """

        self.extends = extends
        """ Base component type extended by this type.
        @type: pylems.model.component.ComponentType """

        self.parameter_types = None
        """ Dictionaty of parameter types in this object.
        @type: dict(string -> pylems.model.parameter.ParameterType) """

        if extends:
            if extends.parameter_types:
                for ptn in extends.parameter_types:
                    self.add_parameter_type(extends.parameter_types[ptn].copy())

    def add_parameter_type(self, parameter_type):
        """
        Adds a parameter type to the list of parameter types in this object.

        @param parameter_type: Parametert type to be added
        @type parameter_type: pylems.model.parameter.ParameterType

        @raise ModelError: Raised when the parameter type is already defined
        in the current object.
        """

        if self.parameter_types == None:
            self.parameter_types = dict()

        if parameter_type.name in self.parameter_types:
            raise ModelError('Duplicate parameter_type type - ' +
                             parameter_type.name)

        self.parameter_types[parameter_type.name] = parameter_type

    def fix_parameter_type(self, parameter_name, value_string, model):
        """
        Fixes the value of a parameter type to the specified value.

        @param parameter_name: Name of the parameter to be fixed.
        @type parameter_name: string

        @param value_string: Value to which the parameter needs to be fixed to.
        For example, "30mV" or "45 kg"
        @type string

        @param model: Model object storing the current model. (Needed to find
        the dimension for the specified symbol)
        @type model: pylems.model.model.Model

        @attention: Having to pass the model in as a parameter is a temporary
        hack. This should fixed at some point of time, once PyLEMS is able to
        run a few example files.

        @raise ModelError: Raised when the parameter type does not exist in this 
        component type.
        """

        if parameter_name in self.parameter_types:
            self.parameter_types[parameter_name].fix_value(value_string, model)
        else:
            raise ModelError('Parameter type ' + value_string +
                             ' not present in ' + self.name)

class Component(PyLEMSBase):
    """
    Stores a single instance of a given component type.
    """

    def __init__(self, id, component_type, extends = None):
        """
        Constructor

        @param id: Id/name for this component.
        @type id: string

        @param component_type: Type of component.
        @type component_type: pylems.model.component.ComponentType

        @param extends: Component extended by this one.
        @param extends: pylems.model.component.Component

        @note: Atleast one of component_type or extends must be valid.
        """
        
        self.id = id 
        """ Globally unique name for this component.
        @type: string """
        
        self.component_type = None
        """ Type of component.
        @type: pylems.model.component.ComponentType """
            
        self.parameters = None
        """ Dictionaty of parameters in this object.
        @type: dict(string -> pylems.model.parameter.Parameter) """

        if component_type == None and extends == None:
            raise ModelError('Component definition requires a component type ' +
                             'or a base component')

        if component_type:
            self.component_type = component_type

            if component_type.parameter_types != None:
                for ptn in component_type.parameter_types:
                    pt = component_type.parameter_types[ptn]
                    p = Parameter(pt)
                    self.add_parameter(p)
                    if pt.fixed:
                        p.set_value(pt.fixed_value)
        else:
            self.component_type = extends.component_type

            for pn in extends.parameters:
                p = extends.parameters[pn]
                self.add_parameter(p.copy())

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of parameters in this object.

        @param parameter: Parameter to be added
        @type parameter: pylems.model.parameter.Parameter

        @raise ModelError: Raised when the parameter is already defined in the 
        current object.
        """

        if self.parameters == None:
            self.parameters = dict()

        self.parameters[parameter.parameter_type.name] = parameter

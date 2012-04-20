"""
Context storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import ModelError

class Context(PyLEMSBase):
    """
    Stores the current type and variable context.
    """

    def __init__(self, parent = None):
        """
        Constructor
        """

        self.parent = parent
        """ Reference to parent context.
        @type: pylems.model.context.Context """

        self.component_types = None
        """ Dictionary of references to component types defined in this conext.
        @type: dict(string -> pylems.model.component.ComponentType) """

        self.components = None
        """ Dictionary of references to components defined in this context.
        @type: dict(string -> pylems.model.component.Component) """

        self.parameters = None
        """ Dictionary of references to parameters defined in this context.
        @type: dict(string -> pylems.model.parameter.Parameter) """

    def add_component_type(self, component_type):
        """
        Adds a component type to the list of defined component types in the
        current context.

        @param component_type: Component type to be added
        @type component_type: pylems.model.component.ComponentType

        @raise ModelError: Raised when the component type is already defined
        in the current context.
        """

        if self.component_types == None:
            self.component_types = dict()

        if component_type.name in self.component_types:
            raise ModelError('Duplicate component type - ' +
                             component_type.name)

        self.component_types[component_type.name] = component_type

    def add_component(self, component):
        """
        Adds a component to the list of defined components in the current
        context.

        @param component: Component to be added
        @type component: pylems.model.component.ComponentType

        @raise ModelError: Raised when the component is already defined in the 
        current context.
        """

        if self.components == None:
            self.components = dict()

        if component.id in self.components:
            raise ModelError('Duplicate component type - ' + component.id)

        self.components[component.id] = component

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of defined parameters in the current
        context.

        @param parameter: Parameter to be added
        @type parameter: pylems.model.parameter.ParameterType

        @raise ModelError: Raised when the parameter is already defined in the 
        current context.
        """

        if self.parameters == None:
            self.parameters = dict()

        if parameter.name in self.parameters:
            raise ModelError('Duplicate parameter type - ' + parameter.name)

        self.parameters[parameter.name] = parameter

    def lookup_parameter(self, parameter_name):
        """
        Lookup a parameter in this context by name.

        @param parameter_name: Name of the parameter.
        @type: string

        @return: Corresponding Parameter object or None if not found.
        @rtype: pylems.model.parameter.Parameter
        """

        if parameter_name in self.parameters:
            return self.parameters[parameter_name]
        else:
            return None

class Contextual(PyLEMSBase):
    """
    Base class for objects that need to store their own context.
    """

    def __init__(self, parent = None):
        """
        Constructor.
        """
        
        self.context = Context(parent)
        """ Context object.
        @type: pylems.model.context.Context """

    def add_component_type(self, component_type):
        """
        Adds a component type to the list of defined component types in the
        current context.

        @param component_type: Component type to be added
        @type component_type: pylems.model.component.ComponentType
        """

        self.context.add_component_type(component_type)

    def add_component(self, component):
        """
        Adds a component to the list of defined components in the current
        context.

        @param component: Component to be added
        @type component: pylems.model.component.Component
        """

        self.context.add_component(component)

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of defined parameters in the current
        context.

        @param parameter: Parameter to be added
        @type parameter: pylems.model.parameter.Parameter
        """

        self.context.add_parameter(parameter)

    def lookup_parameter(self, parameter_name):
        """
        Lookup a parameter in this context by name.

        @param parameter_name: Name of the parameter.
        @type: string

        @return: Corresponding Parameter object or None if not found.
        @rtype: pylems.model.parameter.Parameter
        """

        return self.context.lookup_parameter(parameter_name)

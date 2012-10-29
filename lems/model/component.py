"""
Types for component types and components

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.errors  import ModelError
from lems.model.context import Context,Contextual
from lems.model.parameter import Parameter

class ComponentType(Contextual):
    """
    Stores the specification of a user-defined component type.
    """

    def __init__(self, name, context, extends = None):
        """
        Constructor

        @param name: Name of this component type.
        @type name: string

        @param context: The context in which to create this component type.
        @type context: lems.model.context.Context

        @param extends: Base component type extended by this type.
        @type extends: string
        """

        Contextual.__init__(self, name, context, Context.COMPONENT_TYPE)

        self.name = name
        """ Name of this component type.
        @type: string """

        self.extends = extends
        """ Base component type extended by this type.
        @type: string """

        self.types = set()
        """ List of compatible type (base types).
        @type: set(string) """

        self.types.add(name)
        self.types.add(extends)

    def fix_parameter(self, parameter_name, value_string, model):
        """
        Fixes the value of a parameter to the specified value.

        @param parameter_name: Name of the parameter to be fixed.
        @type parameter_name: string

        @param value_string: Value to which the parameter needs to be fixed to.
        For example, "30mV" or "45 kg"
        @type string

        @param model: Model object storing the current model. (Needed to find
        the dimension for the specified symbol)
        @type model: lems.model.model.Model

        @attention: Having to pass the model in as a parameter is a temporary
        hack. This should fixed at some point of time, once PyLEMS is able to
        run a few example files.

        @raise ModelError: Raised when the parameter does not exist in this
        component type.
        """

        parameter = self.lookup_parameter(parameter_name)
        if parameter == None:
            raise ModelError('Parameter ' + value_string +
                             ' not present in ' + self.name)

        parameter.fix_value(value_string, model)

class Component(Contextual):
    """
    Stores a single instance of a given component type.
    """

    def __init__(self, id_, context, component_type, extends = None):
        """
        Constructor

        @param id_: Id/name for this component.
        @type id_: string

        @param context: The context in which to create this component.
        @type context: lems.model.context.Context

        @param component_type: Type of component.
        @type component_type: string

        @param extends: Component extended by this one.
        @param extends: string

        @note: Atleast one of component_type or extends must be valid.
        """

        Contextual.__init__(self, id_, context, Context.COMPONENT)

        self.id = id_
        """ Globally unique name for this component.
        @type: string """

        self.component_type = component_type
        """ Type of component.
        @type: string """

        if component_type == None and extends == None:
            raise ModelError('Component definition requires a component type ' +
                             'or a base component')

        self.extends = extends
        """ Name of component extended by this component..
        @type: string """

    def is_type(self, component_type):
        """
        Check if this component is an instance of the specified component
        type.

        @param component_type: Name of the component type.
        @type component_type: string

        @return: Returns True if this component is of the specified type,
        otherwide False
        @rtype: Boolean
        """

        typeobj = self.context.lookup_component_type(self.component_type)
        return component_type in typeobj.types

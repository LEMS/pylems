"""
Context storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import ModelError
from pylems.model.behavior import Behavior

class Context(PyLEMSBase):
    """
    Stores the current type and variable context.
    """

    GLOBAL = 0
    """ Global context """
    
    COMPONENT_TYPE = 1
    """ Component type context """
    
    COMPONENT = 2
    """ Component context """

    def __init__(self, name, parent = None, context_type = GLOBAL):
        """
        Constructor
        """

        self.name = name
        """ Name identifying this context.
        @type: string """

        self.parent = parent
        """ Reference to parent context.
        @type: pylems.model.context.Context """

        self.component_types = {}
        """ Dictionary of component types defined in this conext.
        @type: dict(string -> pylems.model.component.ComponentType) """

        self.components = {}
        """ Dictionary of components defined in this context.
        @type: dict(string -> pylems.model.component.Component) """

        self.component_refs = {}
        """ Dictionary of component references defined in this context.
        @type: dict(string -> string) """

        self.child_defs = {}
        """ Dictionary of single-instance child objects defined in this
        context.
        @type: dict(string -> string) """
        
        self.children_defs = {}
        """ Dictionary of multi-instance child objects defined in this
        context.
        @type: dict(string -> string) """
        
        self.parameters = {}
        """ Dictionary of references to parameters defined in this context.
        @type: dict(string -> pylems.model.parameter.Parameter) """

        self.context_type = context_type
        """ Context type (Global, component type or component)
        @type: enum(Context.GLOBAL, Context.COMPONENT_TYPE or
        Context.COMPONENT_TYPE) """

        self.behavior_profiles = {}
        """ Stores the various behavior profiles of the current object.
        @type: dict(string -> pylems.model.behavior.Behavior) """

        self.selected_behavior_profile = None
        """ Name of the selected brhavior profile.
        @type: pylems.model.behavior.Behavior """

        self.exposures = []
        """ List of names of exposed variables.
        @type: list(string) """

        self.texts = {}
        """ Dictionary of text parameters.
        @type: dict(string -> string) """
        
        self.paths = {}
        """ Dictionary of path parameters.
        @type: dict(string -> string) """

    def add_component_type(self, component_type):
        """
        Adds a component type to the list of defined component types in the
        current context.

        @param component_type: Component type to be added
        @type component_type: pylems.model.component.ComponentType

        @raise ModelError: Raised when the component type is already defined
        in the current context.
        """

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

        if component.id in self.components:
            raise ModelError('Duplicate component type - ' + component.id)

        self.components[component.id] = component

    def add_component_ref(self, name, type):
        """
        Adds a component reference to the list of defined component
        references in the current context.

        @param name: Name of the component reference.
        @type name: string

        @param type: Type of the component reference.
        @type type: string

        @raise ModelError: Raised when the component reference is already
        defined in the current context.
        """

        if name in self.component_refs:
            raise ModelError('Duplicate component reference ' + name)
        
        self.component_refs[name] = type

    def add_child(self, name, type):
        """
        Adds a child object definition to the list of single-instance child
        object definitions in the current context.

        @param name: Name of the child object.
        @type name: string

        @param type: Type of the child object.
        @type type: string

        @raise ModelError: Raised when the definition is already in the
        current context.
        """

        if name in self.child_defs:
            raise ModelError('Duplicate child definition ' + name)
        
        self.child_defs[name] = type

    def add_children(self, name, type):
        """
        Adds a child object definition to the list of multi-instance child
        object definitions in the current context.

        @param name: Name of the child object.
        @type name: string

        @param type: Type of the child object.
        @type type: string

        @raise ModelError: Raised when the definition is already in the
        current context.
        """

        if name in self.children_defs:
            raise ModelError('Duplicate children definition ' + name)
        
        self.children_defs[name] = type

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of defined parameters in the current
        context.

        @param parameter: Parameter to be added
        @type parameter: pylems.model.parameter.ParameterType

        @raise ModelError: Raised when the parameter is already defined in the 
        current context.
        """

        if parameter.name in self.parameters:
            raise ModelError('Duplicate parameter type - ' + parameter.name)

        self.parameters[parameter.name] = parameter

    def add_behavior_profile(self, name):
        """
        Adds a behavior profile to the current context.

        @param name: Name of the behavior profile.
        @type name: string
        """
        
        if name in self.behavior_profiles:
            raise ModelError('Duplicate behavior profile \'' + name + '\'')

        self.behavior_profiles[name] = Behavior(name)
        self.select_behavior_profile(name)

    def select_behavior_profile(self, name):
        """
        Selects a behavior profile by name.

        @param name: Name of the behavior profile.
        @type name: string

        @raise ModelError: Raised when the specified behavior profile is
        undefined in the current context.
        """

        if name not in self.behavior_profiles:
            raise ModelError('Unknown behavior profile')

        self.selected_behavior_profile = self.behavior_profiles[name]
        
    def add_exposure(self, name):
        """
        Adds a state variable exposure to the current context.

        @param name: Name of the state variable being exposed.
        @type name: string

        @raise ModelError: Raised when the exposure name already exists
        in the current context.

        @raise ModelError: Raised when the exposure name is not
        being defined in the context of a component type.
        """
        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError('Exposure names can only be defined in ' +
                             'a component type')
        
        if name in self.exposures:
            raise ModelError('Duplicate exposure name')

        self.exposures += [name]
        
    def add_text_var(self, name, value = None):
        """
        Adds a text variable to the current context.

        @param name: Name of the text variable.
        @type name: string

        @param value: Value of the text variable.
        @type value: string

        @raise ModelError: Raised when the text variable already exists
        in the current context.
        """
        
        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError('Text variables can only be defined in ' +
                             'a component type')
        
        if name in self.texts:
            raise ModelError('Duplicate text variable')

        self.texts[name] = value
        
    def add_path_var(self, name, value = None):
        """
        Adds a path variable to the current context.

        @param name: Name of the path variable.
        @type name: string

        @param value: Value of the path variable.
        @type value: string

        @raise ModelError: Raised when the path variable already exists
        in the current context.
        """
        
        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError('Path variables can only be defined in ' +
                             'a component type')
        
        if name in self.paths:
            raise ModelError('Duplicate path variable')

        self.paths[name] = value
        
    def lookup_component_type(self, name):
        """
        Searches the current context and parent contexts for a component type
        with the given name.

        @param name: Name of the component type.
        @type name: string

        @return: Resolved component type object, or None on failure.
        @rtype: pylems.model.component.ComponentType
        """

        if name in self.component_types:
            return self.component_types[name]
        elif self.parent:
            return self.parent.lookup_component_type(name)
        else:
            return None

    def lookup_component(self, name):
        """
        Searches the current context and parent contexts for a component
        with the given name.

        @param name: Name of the component.
        @type name: string

        @return: Resolved component object, or None on failure.
        @rtype: pylems.model.component.Component
        """

        if name in self.components:
            return self.components[name]
        elif self.parent:
            return self.parent.lookup_component(name)
        else:
            return None

    def lookup_component_ref(self, name):
        """
        Searches the current context and parent contexts for a component
        with the given name.

        @param name: Name of the component.
        @type name: string

        @return: Resolved component object, or None on failure.
        @rtype: pylems.model.component.Component
        """

        if name in self.component_refs:
            cname = self.component_refs[name]
            return self.lookup_component(cname)
        elif self.parent:
            return self.parent.lookup_component_ref(name)
        else:
            return None

    def lookup_parameter(self, parameter_name):
        """
        Looks up a parameter by name within this context.

        @param parameter_name: Name of the parameter.
        @type parameter_name: string

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

    def __init__(self, name, parent = None, context_type = Context.GLOBAL):
        """
        Constructor.
        """
        
        self.context = Context(name, parent, context_type)
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
        @type parameter_name: string

        @return: Corresponding Parameter object or None if not found.
        @rtype: pylems.model.parameter.Parameter
        """

        return self.context.lookup_parameter(parameter_name)

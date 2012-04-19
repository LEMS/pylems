"""
Context storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.errors import ModelError

class Context:
    """
    Stores the current variable context.
    """

    def __init__(self, parent = None):
        """
        Constructor
        """

        self.parent = parent
        """ Reference to parent context.
        @type: pylems.model.context.Context """

        self.component_types = None
        """ Dictionary of references to component types defined in the model.
        @type: dict(string -> pylems.model.component.ComponentType) """

        self.components = None
        """ Dictionary of references to components defined in the model.
        @type: dict(string -> pylems.model.component.Component) """

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

class Contextual:
    """
    Base class for objects that need to store their own context.
    """

    def __init__(self):
        self.context = None
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

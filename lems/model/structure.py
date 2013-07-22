"""
Structural properties of component types.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError

class With(LEMSBase):
    """
    Stores a with-as statement.
    """

    def __init__(self, instance, as_):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """

        self.instance = instance
        """ Instance to be referenced.
        @type: str """

        self.as_ = as_
        """ Alternative name.
        @type: str """

class EventConnection(LEMSBase):
    """
    Stores an event connection specification.
    """

    def __init__(self, from_, to, 
                 source_port, target_port,
                 receiver, receiver_container):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """

        self.from_ = from_
        """ Name of the source component for event.
        @type: str """

        self.to = to
        """ Name of the target component for the event.
        @type: str """

        self.source_port = source_port
        """ Source port name.
        @type: str """

        self.target_port = target_port
        """ Target port name.
        @type: str """

        self.receiver = receiver
        """ Name of the proxy receiver component attached to the target component that actually receiving the event.
        @type: str """

        self.receiver_container = receiver_container
        """ Name of the child component grouping to add the receiver to.
        @type: str """

    def __eq__(self, o):
        return (self.from_ == o.from_ and self.to == o.to and
                self.source_port == o.source_port and self.target_port == o.target_port)


class ChildInstance(LEMSBase):
    """
    Stores a child instantiation specification.
    """

    def __init__(self, component):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """

        self.component = component
        """ Name of the component reference to be used for instantiation.
        @type: str """
        
    def __eq__(self, o):
        return self.component == o.component

class MultiInstantiate(LEMSBase):
    """
    Stores a child multi-instantiation specification.
    """

    def __init__(self, component, number):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """

        self.component = component
        """ Name of the component reference to be used for instantiation.
        @type: str """

        self.number = number
        """ Name of the paramter specifying the number of times the component 
        reference is to be instantiated.
        @type: str"""
        
    def __eq__(self, o):
        return self.component == o.component and self.number == o.number

class Structure(LEMSBase):
    """
    Stores structural properties of a component type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.withs = Map()
        """ Map of With statements.
        @type: Map(str -> lems.model.structure.With) """

        self.event_connections = list()
        """ List of event connections.
        @type: list(lems.model.structure.EventConnection) """

        self.child_instances = list()
        """ List of child instantations.
        @type: list(lems.model.structure.ChildInstance) """

        self.multi_instantiates = list()
        """ List of child multi-instantiations.
        @type: list(lems.model.structure.MultiInstantiate) """

    def add_with(self, with_):
        """
        Adds a with-as specification to the structure.

        @param with_: With-as specification.
        @type with_: lems.model.structure.With
        """

        self.withs[with_.instance] = with_
        
    def add_event_connection(self, ec):
        """
        Adds an event conenction to the structure.

        @param ec: Event connection.
        @type ec: lems.model.structure.EventConnection
        """

        self.event_connections.append(ec)

    def add_child_instance(self, ci):
        """
        Adds a child instantiation specification.

        @param ci: Child instantiation specification.
        @type ci: lems.model.structure.ChildInstance
        """

        self.child_instances.append(ci)

    def add_multi_instantiate(self, mi):
        """
        Adds a child multi-instantiation specification.

        @param mi: Child multi-instantiation specification.
        @type mi: lems.model.structure.MultiInstantiate
        """

        self.multi_instantiates.append(mi)

    def add(self, child):
        """
        Adds a typed child object to the structure object.

        @param child: Child object to be added.
        """

        if isinstance(child, With):
            self.add_with(child)
        elif isinstance(child, EventConnection):
            self.add_event_connection(child)
        elif isinstance(child, ChildInstance):
            self.add_child_instance(child)
        elif isinstance(child, MultiInstantiate):
            self.add_multi_instantiate(child)
        else:
            raise ModelError('Unsupported child element')

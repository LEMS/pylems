"""
Component structure storage.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import PyLEMSBase
from lems.base.errors import ModelError

class Structure(PyLEMSBase):
    """
    Stores the structural characteristics for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.event_connections = []
        """ List of event connections b/w components. The from and to
        attributes are described as component:port
        @type: list((string, string)) """

        self.single_child_defs = []
        """ List of single-child instantiation definitions.
        @type: list(string) """

        self.multi_child_defs = {}
        """ List of multi-child instantiation definitions.
        @type: dict(string -> string) """

        self.foreach = []
        """ List of foreach declarations. """
        
    def add_event_connection(self, from_, to):
        """
        Adds an event connection to the list of event connections in this
        component.

        @param from_: The component:port from where the event originates.
        @type from_: string

        @param to: The component:port to which the event is being sent.
        @type to: string
        """

        if from_.find(':') >= 0:
            (from_component, from_port) = from_.split(':', 1)
        else:
            from_component = from_
            from_port = ''

        if to.find(':') >= 0:
            (to_component, to_port) = to.split(':', 1)
        else:
            to_component = to
            to_port = ''

        self.event_connections.append((from_component, from_port,
                                       to_component, to_port))

    def add_single_child_def(self, component):
        """
        Adds a single-child instantiation definition to this component type.

        @param component: Name of component reference used as template for
        instantiating the child.
        @type component: string
        """
        
        if component in self.single_child_defs:
            raise ModelError("Duplicate child instantiation = '{0}'".format(\
                component))
        self.single_child_defs.append(component)

    def add_multi_child_def(self, component, number):
        """
        Adds a single-child instantiation definition to this component type.

        @param component: Name of component reference used as template for
        instantiating the child.
        @type component: string

        @param number: Number of objects to be instantiated.
        @type number: string
        """
        
        if component in self.single_child_defs:
            raise ModelError("Duplicate child multiinstantiation = "
                             "'{0}'".format(component))

        if self.multi_child_defs != {}:
            raise ModelError("Only one multi-instantiation is permitted "
                             "per component type - '{0}'".format(component))

        self.multi_child_defs[component] = number

    def add_foreach(self, name, target):
        """
        Adds a foreach structure nesting.

        @param name: Name used to refer to the enumerated target references.
        @type name: string

        @param target: Path to thetarget references.
        @type target: string
        """

        foreach = ForEach(name, target)
        self.foreach.append(foreach)
        return foreach

class ForEach(Structure):
    """
    Stores a <ForEach> statement and containing structures.
    """

    def __init__(self, name, target):
        """
        Constructor.

        @param name: Name used to refer to the enumerated target instances.
        @type name: string

        @param target: Path to the target instances.
        @type target: string
        """
        
        Structure.__init__(self)

        self.name = name
        """ Name used to refer to the enumerated target instances.
        @type: string """
        
        self.target = target
        """ Path to the target instances.
        @type: string """

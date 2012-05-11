"""
Component structure storage.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

class Structure(PyLEMSBase):
    """
    Stores the structural characteristics for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.event_connections = []
        """ Dictionary of event connections b/w components. The from and to
        attributes are described as component:port
        @type: list((string, string)) """
        
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

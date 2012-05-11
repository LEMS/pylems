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

        self.event_connections = {}
        """ Dictionary of event connections """

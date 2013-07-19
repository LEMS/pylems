"""
Base runnable classes.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase
from lems.errors import SimBuildError

class RunnableType(LEMSBase):
    """
    Base runnable component type class.
    """

    def __init__(self, parent = None):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        self.parent = parent
        """ Parent runnable.
        @type: lems.sim.runnable.Runnable """

"""
Simulation.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import SimError

class Simulation(PyLEMSBase):
    """
    Simulation class.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        
        self.runnables = {}
        """ Dictionary of runnable components in this simulation.
        @type dict(string -> pylems.sim.runnable.Runnable) """

    def add_runnable(self, id, runnable):
        """
        Adds a runnable component to the list of runnable components in
        this simulation.

        @param id: Component id
        @type id: string
        
        @param runnable: A runnable component
        @type runnable: pylems.sim.runnable.Runnable
        """

        if id in self.runnables:
            raise SimError('Duplicate runnable component {0}'.format(id))
        
        self.runnables[id] = runnable

    def run(self):
        for id in self.runnables:
            runnable = self.runnables[id]
            print runnable.time_step, runnable.time_total

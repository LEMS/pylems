"""
Simulation.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import SimError

import heapq

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
        current_time = 0

        run_queue = []
        for id in self.runnables:
            runnable = self.runnables[id]
            next_time = current_time + runnable.single_step(\
                runnable.time_step)
            if next_time > current_time:
                heapq.heappush(run_queue, (next_time, runnable))

        while run_queue:
            (current_time, runnable) = heapq.heappop(run_queue)
            next_time = current_time + runnable.single_step(\
                runnable.time_step)
            if next_time > current_time:
                heapq.heappush(run_queue, (next_time, runnable))

            if run_queue == []:
                break
            
            (time, runnable) = heapq.heappop(run_queue)
            while time == current_time:
                next_time = current_time + runnable.single_step(\
                    runnable.time_step)
                if next_time > current_time:
                    heapq.heappush(run_queue, (next_time, runnable))
                    
                if run_queue == []:
                    break
                (time, runnable) = heapq.heappop(run_queue)

            if time > current_time:
                heapq.heappush(run_queue, (time, runnable))

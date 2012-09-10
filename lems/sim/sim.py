"""
Simulation.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.errors import SimError

import heapq

class Simulation(LEMSBase):
    """
    Simulation class.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        
        self.runnables = {}
        """ Dictionary of runnable components in this simulation.
        @type: dict(string -> lems.sim.runnable.Runnable) """

        self.run_queue = []
        """ Priority of pairs of (time-to-next run, runnable)
        @type: list((Integer, lems.sim.runnable.Runnable)) """

        self.event_queue = []
        """ List of posted events
        @type: list(lems.sim."""

    def add_runnable(self, id, runnable):
        """
        Adds a runnable component to the list of runnable components in
        this simulation.

        @param id: Component id
        @type id: string
        
        @param runnable: A runnable component
        @type runnable: lems.sim.runnable.Runnable
        """

        if id in self.runnables:
            raise SimError('Duplicate runnable component {0}'.format(id))
        
        self.runnables[id] = runnable

    def init_run(self):
        self.current_time = 0
        for id in self.runnables:
            heapq.heappush(self.run_queue, (0, self.runnables[id]))
        
    def step(self):
        current_time = self.current_time

        if self.run_queue == []:
            return False

        (current_time, runnable) = heapq.heappop(self.run_queue)
        time = current_time
        while time == current_time:
            next_time = current_time + runnable.single_step(\
                runnable.time_step)

            if next_time > current_time:
                heapq.heappush(self.run_queue, (next_time, runnable))
                        
            if self.run_queue == []:
                break
            (time, runnable) = heapq.heappop(self.run_queue)

            if time > current_time:
                heapq.heappush(self.run_queue, (time, runnable))

        self.current_time = current_time

        if self.run_queue == []:
            return False
        else:
            return True

    def run(self):
        """
        Runs the simulation.
        """

        self.init_run()
        while self.step():
            pass

    def push_state(self):
        for id in self.runnables:
            self.runnables[id].push_state()

    def pop_state(self):
        for id in self.runnables:
            self.runnables[id].pop_state()

    def enable_plasticity(self):
        for id in self.runnables:
            self.runnables[id].plastic = True

    def disable_plasticity(self):
        for id in self.runnables:
            self.runnables[id].plastic = False

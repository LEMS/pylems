"""
Simulation builder.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

class SimulationBuilder(PyLEMSBase):
    """
    Simulation class.
    """
    
    def __init__(self, model):
        """
        Constructor.

        @param model: Model upon which the simulation is to be generated.
        @type model: pylems.model.model.Model
        """
        
        self.model = model

    def build(self):
        """
        Build the simulation components from the model.
        """

        for component_name in self.model.default_runs:
            self.process_default_run()

        pass

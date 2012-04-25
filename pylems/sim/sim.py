"""
Simulation generator.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

class Simulation(PyLEMSBase):
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

        pass

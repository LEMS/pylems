"""
Simulation builder.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import SimBuildError

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
            if component_name not in self.model.context.components:
                raise SimBuildError('Unable to find component \'{0}\' to run'\
                                    .format(component_name))
            component = self.model.context.components[component_name]
            self.build_runnable_component(component)

    def build_runnable_component(self, component):
        type_name = component.component_type
        if type_name not in self.model.context.component_types:
            
                raise SimBuildError('Unable to find component type \'{0}\''\
                                    .format(type_name))
        component_type = self.model.context.component_types[type_name]
        

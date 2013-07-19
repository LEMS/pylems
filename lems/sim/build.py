"""
Simulation builder.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.errors import SimBuildError
from lems.sim.runnable import Runnable
from lems.sim.sim import Simulation

class SimulationBuilder(LEMSBase):
    """
    Simulation builder class.
    """

    def __init__(self, model):
        """
        Constructor.

        @param model: Model upon which the simulation is to be generated.
        @type model: lems.model.model.Model
        """

        self.model = model
        """ Model to be used for constructing the simulation.
        @type: lems.model.model.Model """

        self.sim = None
        """ Simulation built from the model.
        @type: lems.sim.sim.Simulation """

    def build(self):
        """
        Build the simulation components from the model.

        @return: A runnable simulation object
        @rtype: lems.sim.sim.Simulation
        """

        self.sim = Simulation()

        for target_component_id in self.model.targets:
            if target_component_id not in self.model.components:
                raise SimBuildError("Unable to find target component '{0}'",
                                    target_component_id)
            
            component = self.model.components[target_component_id]
            component_type = self.model.component_types[component.type]

            runnable_type = self.build_runnable_type(component_type)
            runnable.instantiate(component)
            
            self.sim.add_runnable(runnable)

        return self.sim

    def build_runnable_type(self, component_type):
        """
        Builds a runnable component type.
        """

        

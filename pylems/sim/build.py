"""
Simulation builder.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import SimBuildError
from pylems.sim.runnable import Runnable

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

            runnable = self.build_runnable(component)

    def build_runnable(self, component):
        runnable = Runnable()
        context = component.context

        print 'Building ' + component.id
        
        for pn in context.parameters:
            p = context.parameters[pn]
            if p.numeric_value:
                runnable.add_instance_variable(p.name, p.numeric_value)
            else:
                if p.dimension == '__component_ref__':
                    ref = context.parent.lookup_component(p.value)
                    if ref == None:
                        raise SimBuildError(('Unable to resolve component '
                                             'reference {0}').\
                                            format(component_name))
                    self.build_runnable(ref)

        if context.selected_behavior_profile:
            self.add_runnable_behavior(runnable,
                                       context.selected_behavior_profile)

        print component.id, runnable.__dict__

    def add_runnable_behavior(self, runnable, behavior_profile):
        regime = behavior_profile.default_regime

        for svn in regime.state_variables:
            sv = regime.state_variables[svn]
            runnable.add_instance_variable(sv.name, 0)
            runnable.add_instance_variable(sv.name + '_shadow', 0)

        time_step_code = []
        for tdn in regime.state_variables:
            if tdn not in regime.state_variables:
                raise SimBuildError(('Time derivative for undefined state '
                                     'variable {0}').format(tdn))
            td = regime.state_variables[tdn]

            

"""
Simulation builder.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import SimBuildError
from pylems.sim.runnable import Runnable
from pylems.sim.sim import Simulation
from pylems.parser.expr import ExprNode
from pylems.model.behavior import EventHandler,Action

class SimulationBuilder(PyLEMSBase):
    """
    Simulation builder class.
    """
    
    def __init__(self, model):
        """
        Constructor.

        @param model: Model upon which the simulation is to be generated.
        @type model: pylems.model.model.Model
        """
        
        self.model = model
        self.sim = None

    def build(self):
        """
        Build the simulation components from the model.

        @return: A runnable simulation object
        @rtype: pylems.sim.sim.Simulation
        """

        self.sim = Simulation()

        for component_id in self.model.default_runs:
            if component_id not in self.model.context.components:
                raise SimBuildError('Unable to find component \'{0}\' to run'\
                                    .format(component_id))
            component = self.model.context.components[component_id]

            runnable = self.build_runnable(component)
            
        return self.sim

    def build_runnable(self, component):
        """
        Build a runnable component from a component specification and add
        it to the simulation.

        @param component: Component specification
        @type component: pylems.model.component.Component

        @raise SimBuildError: Raised when a componen reference cannot be
        resolved.
        """
        
        runnable = Runnable()
        context = component.context

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
            self.add_runnable_behavior(component, runnable,
                                       context.selected_behavior_profile)

        self.sim.add_runnable(component.id, runnable)

    def add_runnable_behavior(self, component, runnable, behavior_profile):
        """
        Add behavior to a runnable component based on the behavior
        specifications in the component model.

        @param component: Component model containing behavior specifications.
        @type component: pylems.model.component.Component

        @param runnable: Runnable component to which behavior is to be added.
        @type runnable: pylems.sim.runnable.Runnable

        @param behavior_profile: The behavior profile to be used to generate
        behavior code in the runnable component.
        @type behavior_profile: pylems.model.behavior.Behavior

        @raise SimBuildError: Raised when a time derivative expression refers
        to an undefined variable.

        @raise SimBuildError: Raised when there are invalid time
        specifications for the <Run> statement.

        @raise SimBuildError: Raised when the component reference for <Run>
        cannot be resolved.
        """
        
        context = component.context
        regime = behavior_profile.default_regime

        for svn in regime.state_variables:
            sv = regime.state_variables[svn]
            runnable.add_instance_variable(sv.name, 0)

        time_step_code = []
        for tdn in regime.time_derivatives:
            if tdn not in regime.state_variables:
                raise SimBuildError(('Time derivative for undefined state '
                                     'variable {0}').format(tdn))
            
            td = regime.time_derivatives[tdn]
            time_step_code += ['self.{0} += dt * ({1})'.format(td.variable,
                               self.build_expression_from_tree(\
                                   td.expression_tree))]
        runnable.add_method('update_state_variables', ['self', 'dt'],
                            time_step_code)

        event_handler_code = []
        for eh in regime.event_handlers:
            event_handler_code += self.build_event_handler(eh)
        runnable.add_method('run_postprocessing_event_handlers', ['self'],
                            event_handler_code)

        for rn in regime.runs:
            run = regime.runs[rn]
            c = context.lookup_component_ref(run.component)
            if c != None and c.id in self.sim.runnables:
                target = self.sim.runnables[c.id]
                time_step = context.lookup_parameter(run.increment)
                time_total = context.lookup_parameter(run.total)
                if time_step != None and time_total != None:
                    target.configure_time(time_step.numeric_value,
                                          time_total.numeric_value)
                else:
                    raise SimBuildError(('Invalid time specifications in '
                                         '<Run>'))
            else:
                raise SimBuildError(('Invalid component reference {0} in '
                                     '<Run>').format(c.id))

    def convert_op(self, op):
        """
        Converts NeuroML arithmetic/logical operators to python equivalents.

        @param op: NeuroML operator
        @type op: string

        @return: Python operator
        @rtype: string
        """
        
        if op == '.gt.':
            return '>'
        elif op == '.ge.':
            return '>='
        elif op == '.lt.':
            return '<'
        elif op == '.le.':
            return '<='
        elif op == '.eq.':
            return '=='
        elif op == '.ne.':
            return '!='
        else:
            return op
        
    def build_expression_from_tree(self, tree_node):
        """
        Recursively builds a Python expression from a parsed expression tree.

        @param tree_node: Root node for the tree from which the expression
        is to be built.
        @type tree_node: pylems.parser.expr.ExprNode

        @return: Generated Python expression.
        @rtype: string
        """
        
        if tree_node.type == ExprNode.VALUE:
            if tree_node.value[0].isalpha():
                return 'self.{0}_shadow'.format(tree_node.value)
            else:
                return tree_node.value
        else:
            return '({0}) {1} ({2})'.format(\
                self.build_expression_from_tree(tree_node.left),
                self.convert_op(tree_node.op),
                self.build_expression_from_tree(tree_node.right))

    def build_event_handler(self, event_handler):
        """
        Build event handler code.

        @param event_handler: Event handler object
        @type event_handler: pylems.model.behavior.EventHandler

        @return: Generated event handler code.
        @rtype: list(string)
        """
        
        if event_handler.type == EventHandler.ON_CONDITION:
            return self.build_on_condition(event_handler)
        else:
            return []

    def build_on_condition(self, on_condition):
        """
        Build OnCondition event handler code.

        @param on_condition: OnCondition event handler object
        @type on_condition: pylems.model.behavior.OnCondition

        @return: Generated OnCondition code
        @rtype: list(string)
        """
        
        on_condition_code = []

        on_condition_code += ['if {0}:'.format(\
            self.build_expression_from_tree(on_condition.expression_tree))]

        for action in on_condition.actions:
            on_condition_code += ['    ' + self.build_action(action)]

        return on_condition_code
            
    def build_action(self, action):
        """
        Build event handler action code.

        @param action: Event handler action object
        @type action: pylems.model.behavior.Action

        @return: Generated action code
        @rtype: string
        """
        
        if action.type == Action.STATE_ASSIGNMENT:
            return self.build_state_assignment(action)
        else:
            return ''

    def build_state_assignment(self, state_assignment):
        """
        Build state assignment code.

        @param state_assignment: State assignment object
        @type state_assignment: pylems.model.behavior.StateAssignment

        @return: Generated state assignment code
        @rtype: string
        """
        
        return 'self.{0} = {1}'.format(\
            state_assignment.variable,
            self.build_expression_from_tree(state_assignment.expression_tree))

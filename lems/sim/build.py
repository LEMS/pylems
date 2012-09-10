"""
Simulation builder.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import copy

from lems.base.base import LEMSBase
from lems.base.errors import SimBuildError
from lems.sim.runnable import Runnable
from lems.sim.sim import Simulation
from lems.parser.expr import ExprNode
from lems.model.behavior import EventHandler,Action

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

        self.current_record_target = None


    def build(self):
        """
        Build the simulation components from the model.

        @return: A runnable simulation object
        @rtype: lems.sim.sim.Simulation
        """

        self.sim = Simulation()

        for component_id in self.model.default_runs:
            if component_id not in self.model.context.components:
                raise SimBuildError('Unable to find component \'{0}\' to run'\
                                    .format(component_id))
            component = self.model.context.components[component_id]

            runnable = self.build_runnable(component)
            self.sim.add_runnable(component.id, runnable)
            
        return self.sim

    def build_runnable(self, component, parent = None):
        """
        Build a runnable component from a component specification and add
        it to the simulation.

        @param component: Component specification
        @type component: lems.model.component.Component

        @param parent: Parent runnable component.
        @type parent: lems.sim.runnable.Runnable

        @raise SimBuildError: Raised when a component reference cannot be
        resolved.
        """

        runnable = Runnable(component.id, parent)

        context = component.context
        record_target_backup = self.current_record_target

        for pn in context.parameters:
            p = context.parameters[pn]
            if p.numeric_value:
                runnable.add_instance_variable(p.name, p.numeric_value)
            else:
                pass
                ## if p.dimension == '__component_ref__':
                ##     ref = context.parent.lookup_component(p.value)
                ##     if ref == None:
                ##         raise SimBuildError(('Unable to resolve component '
                ##                              'reference {0}').\
                ##                             format(component_name))
                ##     self.sim.add_runnable(ref.id, self.build_runnable(ref))

        for port in context.event_in_ports:
            runnable.add_event_in_port(port)
        for port in context.event_out_ports:
            runnable.add_event_out_port(port)

        if context.selected_behavior_profile:
            self.add_runnable_behavior(component, runnable,
                                       context.selected_behavior_profile)
        else:
            runnable.add_method('update_state_variables', ['self', 'dt'],
                                [])
            runnable.add_method('run_preprocessing_event_handlers', ['self'],
                                [])
            runnable.add_method('run_postprocessing_event_handlers', ['self'],
                                [])
            
        for cn in context.components:
            child = context.components[cn]
            runnable.add_child(child.id, self.build_runnable(child, runnable))

        self.build_structure(component, runnable, context.structure)

        if context.selected_behavior_profile:
            self.add_recording_behavior(component, runnable,
                                        context.selected_behavior_profile)
            
        self.current_record_target = record_target_backup

        return runnable

    def build_structure(self, component, runnable, structure):
        """
        Adds structure to a runnable component based on the structure
        specifications in the component model.

        @param component: Component model containing structure specifications.
        @type component: lems.model.component.Component

        @param runnable: Runnable component to which structure is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param structure: The structure object to be used to add
        structure code in the runnable component.
        @type structure: lems.model.structure.Structure
        """

        context = component.context

        # Process single-child instantiations
        # TBD
        
        # Process multi-child instatiantions
        for cparam in structure.multi_child_defs:
            sparam = structure.multi_child_defs[cparam]
            c1 = component
            c2 = context.lookup_component(cparam)
            template = self.build_runnable(context.lookup_component(cparam),
                                           component)
            
            for i in xrange(sparam):
                instance = copy.deepcopy(template)
                instance.id = "{0}#{1}#{2}".format(component.id,
                                                   template.id,
                                                   i)
                runnable.array.append(instance)
        
        # Process event connections
        for (from_component, from_port,
             to_component, to_port) in structure.event_connections:
            self.add_event_connection(runnable, from_component, from_port,
                                      to_component, to_port)

    def add_event_connection(self, runnable,
                             from_component, from_port,
                             to_component, to_port):
        if from_component in runnable.children:
            from_ = runnable.children[from_component]
        else:
            raise SimBuildError('Unable to find component \'{0}\' '
                                'under \'{1}\''.format(\
                                    from_component, runnable.id))

        if to_component in runnable.children:
            to = runnable.children[to_component]
        else:
            raise SimBuildError('Unable to find component \'{0}\' '
                                'under \'{1}\''.format(\
                                    to_component, runnable.id))

        from_.register_event_out_callback(\
            from_port, lambda: to.inc_event_in(to_port))
            

    def add_runnable_behavior(self, component, runnable, behavior_profile):
        """
        Adds behavior to a runnable component based on the behavior
        specifications in the component model.

        @param component: Component model containing behavior specifications.
        @type component: lems.model.component.Component

        @param runnable: Runnable component to which behavior is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param behavior_profile: The behavior profile to be used to generate
        behavior code in the runnable component.
        @type behavior_profile: lems.model.behavior.Behavior

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

        pre_event_handler_code = []
        post_event_handler_code = []
        for eh in regime.event_handlers:
            if eh.type == EventHandler.ON_CONDITION:
                post_event_handler_code += self.build_event_handler(eh)
            else:
                pre_event_handler_code += self.build_event_handler(eh)
        runnable.add_method('run_preprocessing_event_handlers', ['self'],
                            pre_event_handler_code)
        runnable.add_method('run_postprocessing_event_handlers', ['self'],
                            post_event_handler_code)

        for rn in regime.runs:
            run = regime.runs[rn]
            c = context.lookup_component_ref(run.component)
            if c != None:
                target = self.build_runnable(c, self)
                self.sim.add_runnable(c.id, target)
                self.current_record_target = target
                time_step = context.lookup_parameter(run.increment)
                time_total = context.lookup_parameter(run.total)
                if time_step != None and time_total != None:
                    target.configure_time(time_step.numeric_value,
                                          time_total.numeric_value)
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
        @type tree_node: lems.parser.expr.ExprNode

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
        @type event_handler: lems.model.behavior.EventHandler

        @return: Generated event handler code.
        @rtype: list(string)
        """
        
        if event_handler.type == EventHandler.ON_CONDITION:
            return self.build_on_condition(event_handler)
        elif event_handler.type == EventHandler.ON_EVENT:
            return self.build_on_event(event_handler)
        else:
            return []

    def build_on_condition(self, on_condition):
        """
        Build OnCondition event handler code.

        @param on_condition: OnCondition event handler object
        @type on_condition: lems.model.behavior.OnCondition

        @return: Generated OnCondition code
        @rtype: list(string)
        """
        
        on_condition_code = []

        on_condition_code += ['if {0}:'.format(\
            self.build_expression_from_tree(on_condition.expression_tree))]

        for action in on_condition.actions:
            on_condition_code += ['    ' + self.build_action(action)]

        return on_condition_code
            
    def build_on_event(self, on_event):
        """
        Build OnEvent event handler code.

        @param on_event: OnEvent event handler object
        @type on_event: lems.model.behavior.OnEvent

        @return: Generated OnEvent code
        @rtype: list(string)
        """
        
        on_event_code = []

        on_event_code += ['count = self.event_in_counters[\'{0}\']'.\
                          format(on_event.port),
                          'while count > 0:',
                          '    count -= 1']
        for action in on_event.actions:
            on_event_code += ['    ' + self.build_action(action)]
        on_event_code += ['self.event_in_counters[\'{0}\'] = 0'.\
                          format(on_event.port),]

        return on_event_code
            
    def build_action(self, action):
        """
        Build event handler action code.

        @param action: Event handler action object
        @type action: lems.model.behavior.Action

        @return: Generated action code
        @rtype: string
        """
        
        if action.type == Action.STATE_ASSIGNMENT:
            return self.build_state_assignment(action)
        if action.type == Action.EVENT_OUT:
            return self.build_event_out(action)
        else:
            return ''

    def build_state_assignment(self, state_assignment):
        """
        Build state assignment code.

        @param state_assignment: State assignment object
        @type state_assignment: lems.model.behavior.StateAssignment

        @return: Generated state assignment code
        @rtype: string
        """
        
        return 'self.{0} = {1}'.format(\
            state_assignment.variable,
            self.build_expression_from_tree(state_assignment.expression_tree))

    def build_event_out(self, event_out):
        """
        Build event out code.

        @param event_out: event out object
        @type event_out: lems.model.behavior.StateAssignment

        @return: Generated event out code
        @rtype: string
        """

        event_out_code = 'for c in self.event_out_callbacks[\'{0}\']: c()'.\
                         format(event_out.port)
        
        return event_out_code

    def add_recording_behavior(self, component, runnable, behavior_profile):
        """
        Adds recording-related behavior to a runnable component based on
        the behavior specifications in the component model.

        @param component: Component model containing behavior specifications.
        @type component: lems.model.component.Component

        @param runnable: Runnable component to which behavior is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param behavior_profile: The behavior profile to be used to generate
        behavior code in the runnable component.
        @type behavior_profile: lems.model.behavior.Behavior

        @raise SimBuildError: Raised when a target for recording could not be
        found.
        """

        context = component.context
        regime = behavior_profile.default_regime

        for rn in regime.records:
            rec = regime.records[rn]
            if self.current_record_target == None:
                raise SimBuildError('No target available for '
                                    'recording variables')
            self.current_record_target.add_variable_recorder(rec.quantity)
            
            

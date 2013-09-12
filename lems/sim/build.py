"""
Simulation builder.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import copy

from lems.base.base import LEMSBase
from lems.base.errors import SimBuildError
from lems.sim.runnable import Runnable
from lems.sim.sim import Simulation
from lems.parser.expr import ExprNode
from lems.model.dynamics import *
from lems.sim.runnable import Regime as RunnableRegime


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

        self.current_data_output = None


    def build(self):
        """
        Build the simulation components from the model.

        @return: A runnable simulation object
        @rtype: lems.sim.sim.Simulation
        """

        self.sim = Simulation()

        for component_id in self.model.targets:
            if component_id not in self.model.components:
                raise SimBuildError("Unable to find target component '{0}'",
                                    component_id)
            component = self.model.fat_components[component_id]

            runnable = self.build_runnable(component)
            self.sim.add_runnable(runnable)

        return self.sim

    def build_runnable(self, component, parent = None, id_ = None):
        """
        Build a runnable component from a component specification and add
        it to the simulation.

        @param component: Component specification
        @type component: lems.model.component.FatComponent

        @param parent: Parent runnable component.
        @type parent: lems.sim.runnable.Runnable

        @param id_: Optional id for therunnable. If it's not passed in,
        the runnable will inherit the id of the component.

        @raise SimBuildError: Raised when a component reference cannot be
        resolved.
        """

        if id_ == None:
            runnable = Runnable(component.id, component, parent)
        else:
            runnable = Runnable(id_, component, parent)

        simulation = component.simulation

        record_target_backup = self.current_record_target
        data_output_backup = self.current_data_output

        do = None
        for d in simulation.data_displays:
            do = d
        if do == None:
            for d in simulation.data_writers:
                do = d

        if do != None:
            self.current_data_output = do

        for parameter in component.parameters:
            runnable.add_instance_variable(parameter.name, parameter.numeric_value)

        derived_parameter_code = []
        
        derived_parameter_ordering = order_derived_parameters(component)
        
        for dpn in derived_parameter_ordering:
            derived_parameter = component.derived_parameters[dpn]
            runnable.add_derived_variable(derived_parameter.name)
            
            expression = self.build_expression_from_tree(runnable,
                                                        None,
                                                        derived_parameter.expression_tree)
            
            derived_parameter_code += ['self.{0} = ({1})'.format(
                        derived_parameter.name,
                        expression)]
            derived_parameter_code += ['self.{0}_shadow = ({1})'.format(
                        derived_parameter.name,
                        expression)]
        #print derived_parameter_code
       
        suffix = ''
        runnable.add_method('update_derived_parameters' + suffix, ['self'],
                            derived_parameter_code)
            
        for constant in component.constants:
            runnable.add_instance_variable(constant.name, constant.numeric_value)

        for text in component.texts:
            runnable.add_text_variable(text.name, text.value)
            
        for link in component.links:
            runnable.add_text_variable(link.name, link.value)

        for ep in component.event_ports:
            if ep.direction.lower() == 'in':
                runnable.add_event_in_port(ep.name)
            else:
                runnable.add_event_out_port(ep.name)

        dynamics = component.dynamics
        self.add_dynamics_1(component, runnable, dynamics, dynamics)

        for regime in dynamics.regimes:
            self.add_dynamics_1(component, runnable, regime, dynamics)

            if regime.initial:
                runnable.current_regime = regime.name

            rn = regime.name
            if rn not in runnable.regimes:
                runnable.add_regime(RunnableRegime(rn))
            r = runnable.regimes[rn]
            suffix = '_regime_' + rn

            r.update_state_variables = runnable.__dict__['update_state_variables'
                                                         + suffix]
            r.update_derived_variables = runnable.__dict__['update_derived_variables'
                                                           + suffix]
            r.run_startup_event_handlers = runnable.__dict__['run_startup_event_handlers'
                                                             + suffix]
            r.run_preprocessing_event_handlers = runnable.__dict__['run_preprocessing_event_handlers'
                                                                   + suffix]
            r.run_postprocessing_event_handlers = runnable.__dict__['run_postprocessing_event_handlers'
                                                                    + suffix]

        self.process_simulation_specs(component, runnable, component.simulation)

        for child in component.child_components:
            child_runnable = self.build_runnable(child, runnable)
            runnable.add_child(child.id, child_runnable)

            for children in component.children:
                #GG - These conditions need more debugging.
                if children.type in child.types:
                    runnable.add_child_typeref(children.type, child_runnable)
                if children.multiple:
                    if children.type in child.types:
                        runnable.add_child_to_group(children.name, child_runnable)
                else:
                    if child_runnable.id == children.name:
                        runnable.add_child_typeref(children.name, child_runnable)

        for attachment in component.attachments:
            runnable.make_attachment(attachment.type, attachment.name)

        self.build_structure(component, runnable, component.structure)

        dynamics = component.dynamics
        self.add_dynamics_2(component, runnable,
                            dynamics, dynamics)
        for regime in dynamics.regimes:
            self.add_dynamics_2(component, runnable, regime, dynamics)

            if regime.name not in runnable.regimes:
                runnable.add_regime(RunnableRegime(regime.name))
            r = runnable.regimes[regime.name]
            suffix = '_regime_' + regime.name


            r.update_kinetic_scheme = runnable.__dict__['update_kinetic_scheme'
                                                        + suffix]

        self.add_recording_behavior(component, runnable)

        self.current_data_output = data_output_backup
        self.current_record_target = record_target_backup

        return runnable

    def build_structure(self, component, runnable, structure):
        """
        Adds structure to a runnable component based on the structure
        specifications in the component model.

        @param component: Component model containing structure specifications.
        @type component: lems.model.component.FatComponent

        @param runnable: Runnable component to which structure is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param structure: The structure object to be used to add
        structure code in the runnable component.
        @type structure: lems.model.structure.Structure
        """

        # Process single-child instantiations
        for ch in structure.child_instances:
            child_runnable = self.build_runnable(ch.referenced_component, runnable)
            runnable.add_child(child_runnable.id, child_runnable)

            runnable.add_child_typeref(ch.component, child_runnable)
            
        # Process multi-child instatiantions
        for mi in structure.multi_instantiates:
            template = self.build_runnable(mi.component,
                                           runnable)

            for i in range(mi.number):
                instance = copy.deepcopy(template)
                instance.id = "{0}__{1}__{2}".format(component.id,
                                                     template.id,
                                                     i)
                runnable.array.append(instance)

        # Process foreach statements
        if structure.for_each:
            self.build_foreach(component, runnable, structure)

        # Process event connections
        for ec in structure.event_connections:
            #print("event_connections  {0}".format(ec.toxml()))
            source = runnable.parent.resolve_path(ec.from_)
            target = runnable.parent.resolve_path(ec.to)

            if ec.receiver:
                receiver_template = self.build_runnable(ec.receiver,
                                                            target)
                receiver = copy.deepcopy(receiver_template)
                receiver.id = "{0}__{1}__".format(component.id,
                                                  receiver_template.id)

                target.add_attachment(receiver, ec.receiver_container)
                target.add_child(receiver_template.id, receiver)
                target = receiver

            ### TODO: recheck retrieving portnames from target_port etc.
            source_port = None #ec.source_port.name if ec.source_port else None
            target_port = None #ec.target_port.name if ec.target_port else None
            
            if not source_port:
                if len(source.event_out_ports) == 1:
                    source_port = source.event_out_ports[0]
                else:
                    raise SimBuildError(("No source event port "
                                         "uniquely identifiable"
                                         " in '{0}'").format(source.id))
            if not target_port:
                if len(target.event_in_ports) == 1:
                    target_port = target.event_in_ports[0]
                else:
                    raise SimBuildError(("No destination event port "
                                         "uniquely identifiable "
                                         "in '{0}'").format(target.id))
                   
            source.register_event_out_callback(\
                source_port, lambda: target.inc_event_in(target_port))

    def build_foreach(self, component, runnable, foreach, name_mappings = {}):
        """
        Iterate over ForEach constructs and process nested elements.

        @param component: Component model containing structure specifications.
        @type component: lems.model.component.FatComponent

        @param runnable: Runnable component to which structure is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param foreach: The ForEach structure object to be used to add
        structure code in the runnable component.
        @type foreach: lems.model.structure.ForEach
        """

        # Process foreach statements
        for fe in foreach.foreach:
            target_array = runnable.resolve_path(fe.target)

            for target_runnable in target_array:
                name_mappings[fe.name] = target_runnable
                self.build_foreach(component, runnable, fe, name_mappings)

        # Process event connections
        for event in foreach.event_connections:
            source = name_mappings[event.source_path]
            target = name_mappings[event.target_path]

            source_port = context.lookup_text_parameter(event.source_port.name)
            target_port = context.lookup_text_parameter(event.target_port.name)

            if source_port == None:
                if len(source.event_out_ports) == 1:
                    source_port = source.event_out_ports[0]
                else:
                    raise SimBuildError(("No source event port "
                                         "uniquely identifiable"
                                         " in '{0}'").format(source.id))
            if target_port == None:
                if len(target.event_in_ports) == 1:
                    target_port = target.event_in_ports[0]
                else:
                    raise SimBuildError(("No destination event port uniquely"
                                         "identifiable in '{0}'").format(target.id))

            source.register_event_out_callback(\
                source_port, lambda: target.inc_event_in(target_port))


    def add_dynamics_1(self, component, runnable, regime, dynamics):
        """
        Adds dynamics to a runnable component based on the dynamics
        specifications in the component model.

        This method builds dynamics necessary for building child components.

        @param component: Component model containing dynamics specifications.
        @type component: lems.model.component.FatComponent

        @param runnable: Runnable component to which dynamics is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param regime: The dynamics regime to be used to generate
        dynamics code in the runnable component.
        @type regime: lems.model.dynamics.Regime

        @param dynamics: Shared dynamics specifications.
        @type dynamics: lems.model.dynamics.Regime

        @raise SimBuildError: Raised when a time derivative expression refers
        to an undefined variable.

        @raise SimBuildError: Raised when there are invalid time
        specifications for the <Run> statement.

        @raise SimBuildError: Raised when the component reference for <Run>
        cannot be resolved.
        """

        if isinstance(regime, Dynamics) or regime.name == '':
            suffix = ''
        else:
            suffix = '_regime_' + regime.name

        if isinstance(regime, Regime) and regime.initial:
            runnable.new_regime = regime.name

        # Process state variables
        for sv in regime.state_variables:
            runnable.add_instance_variable(sv.name, 0)

        # Process time derivatives
        time_step_code = []
        for td in regime.time_derivatives:
            if td.variable not in regime.state_variables and td.variable not in dynamics.state_variables:
                raise SimBuildError(('Time derivative for undefined state '
                                     'variable {0}').format(tdn))

            exp = self.build_expression_from_tree(runnable,
                                                  regime,
                                                  td.expression_tree)
            time_step_code += ['self.{0} += dt * ({1})'.format(td.variable,
                                                               exp)]
        runnable.add_method('update_state_variables' + suffix, ['self', 'dt'],
                            time_step_code)

        # Process derived variables
        derived_variable_code = []
        derived_variables_ordering = order_derived_variables(regime)
        for dvn in derived_variables_ordering: #regime.derived_variables:
            dv = dynamics.derived_variables[dvn]
            runnable.add_derived_variable(dv.name)
            if dv.value:
                derived_variable_code += ['self.{0} = ({1})'.format(
                        dv.name,
                        self.build_expression_from_tree(runnable,
                                                        regime,
                                                        dv.expression_tree))]
            elif dv.select:
                if dv.reduce:
                    derived_variable_code += self.build_reduce_code(dv.name,
                                                                    dv.select,
                                                                    dv.reduce)
                else:
                    derived_variable_code += ['self.{0} = (self.{1})'.format(
                            dv.name,
                            dv.select.replace('/', '.'))]
            else:
                raise SimBuildError(('Inconsistent derived variable settings'
                                     'for {0}').format(dvn))
        runnable.add_method('update_derived_variables' + suffix, ['self'],
                            derived_variable_code)

        # Process event handlers
        pre_event_handler_code = []
        post_event_handler_code = []
        startup_event_handler_code = []
        on_entry_added = False
        for eh in regime.event_handlers:
            if isinstance(eh, OnStart):
                startup_event_handler_code += self.build_event_handler(runnable,
                                                                       regime,
                                                                       eh)
            elif isinstance(eh, OnCondition):
                post_event_handler_code += self.build_event_handler(runnable,
                                                                    regime,
                                                                    eh)
            else:
                if isinstance(eh, OnEntry):
                    on_entry_added = True
                pre_event_handler_code += self.build_event_handler(runnable,
                                                                   regime,
                                                                   eh)
        if isinstance(regime, Regime) and not on_entry_added:
            pre_event_handler_code += self.build_event_handler(runnable, regime, OnEntry())
            
        runnable.add_method('run_startup_event_handlers' + suffix, ['self'],
                            startup_event_handler_code)
        runnable.add_method('run_preprocessing_event_handlers' + suffix, ['self'],
                            pre_event_handler_code)
        runnable.add_method('run_postprocessing_event_handlers' + suffix, ['self'],
                            post_event_handler_code)

    def add_dynamics_2(self, component, runnable, regime, dynamics):
        """
        Adds dynamics to a runnable component based on the dynamics
        specifications in the component model.

        This method builds dynamics dependent on child components.

        @param component: Component model containing dynamics specifications.
        @type component: lems.model.component.FatComponent

        @param runnable: Runnable component to which dynamics is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param regime: The dynamics regime to be used to generate
        dynamics code in the runnable component.
        @type regime: lems.model.dynamics.Regime

        @param dynamics: Shared dynamics specifications.
        @type dynamics: lems.model.dynamics.Regime

        @raise SimBuildError: Raised when a time derivative expression refers
        to an undefined variable.

        @raise SimBuildError: Raised when there are invalid time
        specifications for the <Run> statement.

        @raise SimBuildError: Raised when the component reference for <Run>
        cannot be resolved.
        """

        if isinstance(regime, Dynamics) or regime.name == '':
            suffix = ''
        else:
            suffix = '_regime_' + regime.name

        # Process kinetic schemes
        ks_code = []
        for ksn in regime.kinetic_schemes:
            ks = regime.kinetic_schemes[ksn]

            try:
                nodes = {node.id:node for node in runnable.__dict__[ks.nodes]}
                edges = runnable.__dict__[ks.edges]

                for edge in edges:
                    from_ = edge.__dict__[ks.edge_source]
                    to = edge.__dict__[ks.edge_target]

                    ks_code += [('self.{0}.{2} += dt * (-self.{3}.{4} * self.{0}.{2}_shadow'
                                 ' + self.{3}.{5} * self.{1}.{2}_shadow)').format(
                        from_, to, ks.state_variable, edge.id,
                        ks.forward_rate, ks.reverse_rate)]

                    ks_code += [('self.{1}.{2} += dt * (self.{3}.{4} * self.{0}.{2}_shadow'
                                 ' - self.{3}.{5} * self.{1}.{2}_shadow)').format(
                        from_, to, ks.state_variable, edge.id,
                        ks.forward_rate, ks.reverse_rate)]

                ks_code += ['sum = 0']
                for node in nodes:
                    nodes[node].__dict__[ks.state_variable] = 1.0 / len(nodes)
                    nodes[node].__dict__[ks.state_variable + '_shadow'] = 1.0 / len(nodes)
                    ks_code += ['sum += self.{0}.{1}'.format(node, ks.state_variable)]

                for node in nodes:
                    ks_code += ['self.{0}.{1} /= sum'.format(node, ks.state_variable)]

                for node in nodes:
                    ks_code += [('self.{0}.{1}_shadow = '
                                 'self.{0}.{1}').format(node,
                                                        ks.state_variable)]

            except Exception as e:
                raise SimBuildError(("Unable to construct kinetic scheme '{0}' "
                                     "for component '{1}' - {2}").format(ks.name,
                                                                         component.id,
                                                                         str(e)))

        runnable.add_method('update_kinetic_scheme' + suffix, ['self', 'dt'],
                            ks_code)

    def process_simulation_specs(self, component, runnable, simulation):
        """
        Process simulation-related aspects to a runnable component based on the
        dynamics specifications in the component model.

        @param component: Component model containing dynamics specifications.
        @type component: lems.model.component.FatComponent

        @param runnable: Runnable component to which dynamics is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @param simulation: The simulation-related aspects to be implemented
        in the runnable component.
        @type simulation: lems.model.simulation.Simulation

        @raise SimBuildError: Raised when a time derivative expression refers
        to an undefined variable

        @raise SimBuildError: Raised when there are invalid time
        specifications for the <Run> statement.

        @raise SimBuildError: Raised when the component reference for <Run>
        cannot be resolved.
        """

        # Process runs
        for run in simulation.runs:
            cid = run.component.id + '_' + component.id

            target = self.build_runnable(run.component, runnable, cid)
            self.sim.add_runnable(target)
            self.current_record_target = target

            target.configure_time(run.increment,
                                  run.total)


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
        elif op == '.ge.' or op == '.geq.':
            return '>='
        elif op == '.lt.':
            return '<'
        elif op == '.le.':
            return '<='
        elif op == '.eq.':
            return '=='
        elif op == '.ne.':
            return '!='
        elif op == '^':
            return '**'
        elif op == '.and.':
            return 'and'
        elif op == '.or.':
            return 'or'
        else:
            return op

    def convert_func(self, func):
        """
        Converts NeuroML arithmetic/logical functions to python equivalents.

        @param func: NeuroML function
        @type func: string


        @return: Python operator
        @rtype: string
        """

        if func == 'ln':
            return 'log'
        else:
            return func

    def build_expression_from_tree(self, runnable, regime, tree_node):
        """
        Recursively builds a Python expression from a parsed expression tree.

        @param runnable: Runnable object to which this expression would be added.
        @type runnable: lems.sim.runnable.Runnable

        @param regime: Dynamics regime being built.
        @type regime: lems.model.dynamics.Regime

        @param tree_node: Root node for the tree from which the expression
        is to be built.
        @type tree_node: lems.parser.expr.ExprNode

        @return: Generated Python expression.
        @rtype: string
        """

        component_type = self.model.component_types[runnable.component.type]
        dynamics = component_type.dynamics
        
        if tree_node.type == ExprNode.VALUE:
            if tree_node.value[0].isalpha():
                if tree_node.value == 't':
                    return 'self.time_completed'
                elif tree_node.value in component_type.requirements:
                    var_prefix = 'self'
                    v = tree_node.value

                    r = runnable

                    while (v not in r.instance_variables and
                           v not in r.derived_variables):
                        var_prefix = '{0}.{1}'.format(var_prefix, 'parent')
                        r = r.parent
                        if r == None:
                            raise SimBuildError("Unable to resolve required "
                                                "variable '{0}'".format(v))

                    return '{0}.{1}'.format(var_prefix, v)
                elif (tree_node.value in dynamics.derived_variables or (regime is not None and tree_node.value in regime.derived_variables)):
                    return 'self.{0}'.format(tree_node.value)
                else:
                    return 'self.{0}_shadow'.format(tree_node.value)
            else:
                return tree_node.value
        elif tree_node.type == ExprNode.FUNC1:
            return '({0}({1}))'.format(\
                self.convert_func(tree_node.func),
                self.build_expression_from_tree(runnable,
                                                regime,
                                                tree_node.param))
        else:
            return '({0}) {1} ({2})'.format(\
                self.build_expression_from_tree(runnable,
                                                regime,
                                                tree_node.left),
                self.convert_op(tree_node.op),
                self.build_expression_from_tree(runnable,
                                                regime,
                                                tree_node.right))

    def build_event_handler(self, runnable, regime, event_handler):
        """
        Build event handler code.

        @param event_handler: Event handler object
        @type event_handler: lems.model.dynamics.EventHandler

        @return: Generated event handler code.
        @rtype: list(string)
        """

        if isinstance(event_handler, OnCondition):
            return self.build_on_condition(runnable, regime, event_handler)
        elif isinstance(event_handler, OnEvent):
            return self.build_on_event(runnable, regime, event_handler)
        elif isinstance(event_handler, OnStart):
            return self.build_on_start(runnable, regime, event_handler)
        elif isinstance(event_handler, OnEntry):
            return self.build_on_entry(runnable, regime, event_handler)
        else:
            return []

    def build_on_condition(self, runnable, regime, on_condition):
        """
        Build OnCondition event handler code.

        @param on_condition: OnCondition event handler object
        @type on_condition: lems.model.dynamics.OnCondition

        @return: Generated OnCondition code
        @rtype: list(string)
        """

        on_condition_code = []

        on_condition_code += ['if {0}:'.format(\
            self.build_expression_from_tree(runnable,
                                            regime,
                                            on_condition.expression_tree))]

        for action in on_condition.actions:
            code = self.build_action(runnable, regime, action)
            for line in code:
                on_condition_code += ['    ' + line]

        return on_condition_code

    def build_on_event(self, runnable, regime, on_event):
        """
        Build OnEvent event handler code.

        @param on_event: OnEvent event handler object
        @type on_event: lems.model.dynamics.OnEvent

        @return: Generated OnEvent code
        @rtype: list(string)
        """

        on_event_code = []

        on_event_code += ['count = self.event_in_counters[\'{0}\']'.\
                          format(on_event.port),
                          'while count > 0:',
                          '    count -= 1']
        for action in on_event.actions:
            code = self.build_action(runnable, regime, action)
            for line in code:
                on_event_code += ['    ' + line]

        on_event_code += ['self.event_in_counters[\'{0}\'] = 0'.\
                          format(on_event.port),]

        return on_event_code

    def build_on_start(self, runnable, regime, on_start):
        """
        Build OnStart start handler code.

        @param on_start: OnStart start handler object
        @type on_start: lems.model.dynamics.OnStart

        @return: Generated OnStart code
        @rtype: list(string)
        """

        on_start_code = []

        for action in on_start.actions:
            code = self.build_action(runnable, regime, action)
            for line in code:
                on_start_code += ['    ' + line]

        return on_start_code

    def build_on_entry(self, runnable, regime, on_entry):
        """
        Build OnEntry start handler code.

        @param on_entry: OnEntry start handler object
        @type on_entry: lems.model.dynamics.OnEntry

        @return: Generated OnEntry code
        @rtype: list(string)
        """

        on_entry_code = []

        on_entry_code += ['if self.current_regime != self.last_regime:']
        on_entry_code += ['    self.last_regime = self.current_regime']

        for action in on_entry.actions:
            code = self.build_action(runnable, regime, action)
            for line in code:
                on_entry_code += ['    ' + line]

        return on_entry_code

    def build_action(self, runnable, regime, action):
        """
        Build event handler action code.

        @param action: Event handler action object
        @type action: lems.model.dynamics.Action

        @return: Generated action code
        @rtype: string
        """

        if isinstance(action, StateAssignment):
            return self.build_state_assignment(runnable, regime, action)
        if isinstance(action, EventOut):
            return self.build_event_out(action)
        if isinstance(action, Transition):
            return self.build_transition(action)
        else:
            return ['pass']

    def build_state_assignment(self, runnable, regime, state_assignment):
        """
        Build state assignment code.

        @param state_assignment: State assignment object
        @type state_assignment: lems.model.dynamics.StateAssignment

        @return: Generated state assignment code
        @rtype: string
        """

        return ['self.{0} = {1}'.format(\
            state_assignment.variable,
            self.build_expression_from_tree(runnable,
                                            regime,
                                            state_assignment.expression_tree))]

    def build_event_out(self, event_out):
        """
        Build event out code.

        @param event_out: event out object
        @type event_out: lems.model.dynamics.EventOut

        @return: Generated event out code
        @rtype: string
        """

        event_out_code = ['if "{0}" in self.event_out_callbacks:'.format(event_out.port),
                          '    for c in self.event_out_callbacks[\'{0}\']:'.format(event_out.port),
                          '        c()']

        return event_out_code

    def build_transition(self, transition):
        """
        Build regime transition code.

        @param transition: Transition object
        @type transition: lems.model.dynamics.Transition

        @return: Generated transition code
        @rtype: string
        """

        return ["self.new_regime = '{0}'".format(transition.regime)]

    def build_reduce_code(self, result, select, reduce):
        """
        Builds a reduce operation on the selected target range.
        """

        select = select.replace('/', '.')
        select = select.replace(' ', '')
        if reduce == 'add':
            reduce_op = '+'
            acc_start = 0
        else:
            reduce_op = '*'
            acc_start = 1

        bits = select.split('[*]')

        code = ['self.{0} = {1}'.format(result, acc_start)]
        code += ['self.{0}_shadow = {1}'.format(result, acc_start)]

        code += ['try:']

        if len(bits) == 1:
            target = select
            code += ['    self.{0} = {1}'.format(result, target)]
            code += ['    self.{0}_shadow = {1}'.format(result, target)]
        elif len(bits) == 2:
            array = bits[0]
            ref = bits[1]

            code += ['    acc = {0}'.format(acc_start)]
            code += ['    for o in self.{0}:'.format(array)]
            code += ['        acc = acc {0} o{1}'.format(reduce_op, ref)]
            code += ['    self.{0} = acc'.format(result)]
            code += ['    self.{0}_shadow = acc'.format(result)]
        else:
            raise SimbuildError("Invalid reduce target - '{0}'".format(select))

        code += ['except:']
        code += ['    pass']

        return code

    def add_recording_behavior(self, component, runnable):
        """
        Adds recording-related dynamics to a runnable component based on
        the dynamics specifications in the component model.

        @param component: Component model containing dynamics specifications.
        @type component: lems.model.component.FatComponent runnable: Runnable component to which dynamics is to be added.
        @type runnable: lems.sim.runnable.Runnable

        @raise SimBuildError: Raised when a target for recording could not be
        found.
        """

        simulation = component.simulation

        for rec in simulation.records:
            self.current_record_target.add_variable_recorder(self.current_data_output, rec)

############################################################

def order_derived_parameters(component):
    """
    Finds ordering of derived_parameters.

    @param component: Component containing derived parameters.
    @type component: lems.model.component.Component

    @return: Returns ordered list of derived parameters.
    @rtype: list(string)

    @raise SimBuildError: Raised when a proper ordering of derived
    parameters could not be found.
    """

    if len(component.derived_parameters) == 0:
        return []
    
    ordering = []
    dps = []
    
    for dp in component.derived_parameters:
        dps.append(dp.name)
    print dps
            
    maxcount = 5

    count = maxcount

    while count > 0 and dps != []:
        count = count - 1

        for dp1 in dps:
            #exp_tree = regime.derived_variables[dv1].expression_tree
            value = component.derived_parameters[dp1].value
            found = False
            for dp2 in dps:
                if dp1 != dp2 and dp2 in value:
                    found = True
            if not found:
                ordering.append(dp1)
                del dps[dps.index(dp1)]
                count = maxcount
                break

    if count == 0:
        raise SimBuildError(("Unable to find ordering for derived "
                             "parameter in component '{0}'").format(component))

    #return ordering + dvsnoexp
    return ordering


def order_derived_variables(regime):
    """
    Finds ordering of derived_variables.

    @param regime: Dynamics Regime containing derived variables.
    @type regime: lems.model.dynamics.regime

    @return: Returns ordered list of derived variables.
    @rtype: list(string)

    @raise SimBuildError: Raised when a proper ordering of derived
    variables could not be found.
    """

    ordering = []
    dvs = []
    dvsnoexp = []
    maxcount = 5

    for dv in regime.derived_variables:
        if dv.expression_tree == None:
            dvsnoexp.append(dv.name)
        else:
            dvs.append(dv.name)

    count = maxcount

    while count > 0 and dvs != []:
        count = count - 1

        for dv1 in dvs:
            exp_tree = regime.derived_variables[dv1].expression_tree
            found = False
            for dv2 in dvs:
                if dv1 != dv2 and is_var_in_exp_tree(dv2, exp_tree):
                    found = True
            if not found:
                ordering.append(dv1)
                del dvs[dvs.index(dv1)]
                count = maxcount
                break

    if count == 0:
        raise SimBuildError(("Unable to find ordering for derived "
                             "variables in regime '{0}'").format(regime.name))

    #return ordering + dvsnoexp
    return dvsnoexp + ordering

def is_var_in_exp_tree(var, exp_tree):
    node = exp_tree

    if node.type == ExprNode.VALUE:
        if node.value == var:
            return True
        else:
            return False
    elif node.type == ExprNode.OP:
        if is_var_in_exp_tree(var, node.left):
            return True
        else:
            return is_var_in_exp_tree(var, node.right)
    elif node.type == ExprNode.FUNC1:
        return is_var_in_exp_tree(var, node.param)
    else:
        return False

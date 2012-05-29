"""
Model storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.errors import ModelError
from pylems.model.context import Contextual
from pylems.model.parameter import Parameter

import re

class Model(Contextual):
    """
    Store the model read from a LEMS file.
    """

    def __init__(self):
        """
        Constructor.
        """

        super(Model, self).__init__('__model__')
        
        self.default_runs = []
        """ Names of simulations to run.
        @type: string """

        self.dimensions = None
        """ Dictionary of references to dimensions defined in the model.
        @type: dict(string -> pylems.model.simple.Dimension) """

        self.units = None
        """ Dictionary of references to units defined in the model.
        @type: dict(string -> pylems.model.simple.Unit) """

        self.context = None
        """ Global (root) context.
        @type: pylems.model.context.Context """

    def add_default_run(self, default_run):
        """
        Add the name of the component to run to the list of components to
        run by default.
        
        @param default_run: Name of a simulation to run by default
        @type default_run: string """
        self.default_runs += [default_run]

    def add_dimension(self, dimension):
        """
        Adds a dimension to the list of defined dimensions.

        @param dimension: Dimension to be added to the model.
        @type dimension: pylems.base.units.Dimension

        @raise ModelError: Raised when the dimension is already defined.
        """

        if self.dimensions == None:
            self.dimensions = dict()

        if dimension.name in self.dimensions:
            self.raise_error('Duplicate dimension - ' + dimension.name,
                             self.context)
        else:
            self.dimensions[dimension.name] = dimension
        
    def add_unit(self, unit):
        """
        Adds a unit to the list of defined units.

        @param unit: Unit to be added to the model.
        @type unit: pylems.base.units.Unit

        @raise ModelError: Raised when the unit is already defined.
        """

        if self.units == None:
            self.units = dict()

        if unit.symbol in self.units:
            self.raise_error('Duplicate unit - ' + unit.symbol, self.context)
        else:
            self.units[unit.symbol] = unit

    def resolve_parameter_value(self, parameter, context):
        """
        Resolves the numeric value of a parameter based on the given value
        in terms of the symbols and dimensions defined in the model.

        @param parameter: Parameter object to be resolved.
        @type parameter: pylems.model.parameter.Parameter

        @param context: Context containing the parameter
        @type context: pylems.model.context.Context

        @raise ModelError: Raised when the value of the parameter is not set.

        @raise ModelError: Raised when the unit symbol does not match the
        parameter's dimension.

        @raise ModelError: Raised when the unit symbol is undefined.
        """
        
        if parameter.value == None:
            self.raise_error('Parameter {0} not initialized'.format(\
                parameter.name), context)

        number = float(re.split('[a-zA-z]+', parameter.value)[0].strip())
        sym = re.split('[^a-zA-z]+', parameter.value)[1].strip()

        if sym == '':
            parameter.numeric_value = number
        else:
            if sym in self.units:
                unit = self.units[sym]
                if parameter.dimension != unit.dimension:
                    if parameter.dimension == '*':
                        parameter.dimension = unit.dimension
                    else:
                        self.raise_error(('Unit symbol {0} cannot '
                                         'be used for dimension {1}').format(\
                                             sym, parameter.dimension),
                                         context)
                parameter.numeric_value = number * (10 ** unit.pow10)
            else:
                self.raise_error('Unknown unit symbol {0}'.format(sym),
                                 context)

    def resolve_extended_component_type(self, context, component_type):
        """
        Resolves the specified component type's parameters from it's base
        component type.

        @param context: Context object containing the component type.
        @type context: pylems.model.context.Context

        @param component_type: Component type to be resolved.
        @type component_type: pylems.model.component.ComponentType

        @raise ModelError: Raised when the base component type cannot be
        resolved.

        @raise ModelError: Raised when a parameter in the base component type
        is redefined in this component type.
        """
        
        base_type = context.lookup_component_type(component_type.extends)
        if base_type == None:
            self.raise_error('Base type {0} not found for component type {1}'.
                             format(component_type.extends,
                                    component_type.name),
                             context)
        if base_type.extends:
            self.resolve_extended_component_type(context, base_type)

        this_context = component_type.context
        base_context = base_type.context

        for pn in base_context.parameters:
            if pn in this_context.parameters:
                pt = this_context.parameters[pn]

                if pt.dimension == '__dimension_inherited__':
                    pb = base_context.parameters[pn]
                    this_context.parameters[pn] = Parameter(pt.name,
                                                            pb.dimension,
                                                            pt.fixed,
                                                            pt.value)
                else:
                    self.raise_error(('Parameter {0} in {1} is redefined ' +
                                     'in {2}').format(pn, base_type.name,
                                                      component_type.name),
                                     context)
            else:
                this_context.parameters[pn] = base_context.parameters[pn].\
                                              copy()

        component_type.extends = None

    def resolve_extended_component(self, context, component):
        """
        Resolves the specified component's parameters from it's base
        component.

        @param context: Context object containing the component.
        @type context: pylems.model.context.Context

        @param component: Component to be resolved.
        @type component: pylems.model.component.Component

        @raise ModelError: Raised when the base component cannot be
        resolved.

        @raise ModelError: Raised when a parameter in the base component
        is redefined in this component.

        @note: Consider changing Component.id to Component.name and merging
        this method with resolve_extended_component_type.
        """
        
        base = context.lookup_component(component.extends)
        if base == None:
            self.raise_error('Base component {0} not found for component {1}'.
                             format(component.extends,
                                    component.id),
                             context)
        if base.extends:
            self.resolve_extended_component(context, base)

        this_context = component.context
        base_context = base.context

        for pn in base_context.parameters:
            if pn in this_context.parameters:
                pt = this_context.parameters[pn]

                if pt.dimension == '__dimension_inherited__':
                    pb = base_context.parameters[pn]
                    this_context.parameters[pn] = Parameter(pt.name,
                                                            pb.dimension,
                                                            pt.fixed,
                                                            pt.value)
                else:
                    self.raise_error(('Parameter {0} in {1} is redefined '
                                     'in {2}').format(pn, base_type.name,
                                                      component_type.name),
                                     context)
            else:
                this_context.parameters[pn] = base_context.parameters[pn].\
                                              copy()

        component.component_type = base.component_type
        component.extends = None

    def resolve_component_structure_from_type(self,
                                              comp_context,
                                              type_context,
                                              component):
        """
        Resolves the specified component's structure from component type.

        @param comp_context: Component's context object.
        @type comp_context: pylems.model.context.Context

        @param type_context: Component type's context object.
        @type type_context: pylems.model.context.Context

        @param component: Component to be resolved.
        @type component: pylems.model.component.Component

        @raise ModelError: Raised when the component type cannot be
        resolved.
        """

        comp_str = comp_context.structure
        type_str = type_context.structure
        
        comp_str.event_connections = type_str.event_connections

        for c in type_str.single_child_defs:
            raise ModelError('TODO')

        for c in type_str.multi_child_defs:
            n = type_str.multi_child_defs[c]
            if c in comp_context.component_refs:
                component = comp_context.component_refs[c]
                if n in comp_context.parameters:
                    number = int(comp_context.parameters[n].numeric_value)
                    comp_str.add_multi_child_def(component, number)
                else:
                    raise ModelError("Trying to multi-instantiate using an "
                                     "invalid number parameter '{0}'".\
                                     format(n))
            else:
                raise ModelError("Trying to multi-instantiate from an "
                                 "invalid component reference '{0}'".format(\
                                     c))


    def resolve_component_from_type(self, context, component):
        """
        Resolves the specified component's parameters from component type.

        @param context: Context object containing the component.
        @type context: pylems.model.context.Context

        @param component: Component to be resolved.
        @type component: pylems.model.component.Component

        @raise ModelError: Raised when the component type cannot be
        resolved.
        """

        component_type = context.lookup_component_type(
            component.component_type)
            
        if component_type == None:
            print component.id, component.component_type
            self.raise_error('Type {0} not found for component {1}'.
                             format(component.component_type,
                                    component.id),
                             context)

        this_context = component.context
        type_context = component_type.context

        for pn in type_context.parameters:
            pt = type_context.parameters[pn]
            if pn in this_context.parameters:
                pc = this_context.parameters[pn]

                if pc.value:
                    value = pc.value
                else:
                    value = pt.value
                    
                if pc.dimension == '__dimension_inherited__':
                    if pt.fixed:
                        np = Parameter(pn, pt.dimension, pt.fixed, value)
                    else:
                        np = Parameter(pn, pt.dimension, pc.fixed, value)
                    this_context.parameters[pn] = np
            else:
                this_context.parameters[pn] = pt.copy()

            self.resolve_parameter_value(this_context.parameters[pn],
                                         this_context)

        for pn in this_context.parameters:
            pc = this_context.parameters[pn]
            if pc.dimension == '__dimension_inherited__':
                if pn in type_context.texts:
                    pc.dimension = '__text__'
                    this_context.texts[pn] = type_context.texts[pn]
                elif pn in type_context.paths:
                    pc.dimension = '__path__'
                    this_context.paths[pn] = type_context.paths[pn]
                elif pn in type_context.links:
                    pc.dimension = '__link__'
                    this_context.links[pn] = type_context.links[pn]
                elif pn in type_context.component_refs:
                    pc.dimension = '__component_ref__'
                    cf = type_context.component_refs[pn]
                    this_context.component_refs[pn] = pc.value

        for bpn in type_context.behavior_profiles:
            bp = type_context.behavior_profiles[bpn].copy()
            this_context.behavior_profiles[bpn] = bp
                
            if bpn == type_context.selected_behavior_profile.name:
                this_context.selected_behavior_profile = bp
                    
        for port in type_context.event_in_ports:
            this_context.event_in_ports.append(port)
        for port in type_context.event_out_ports:
            this_context.event_out_ports.append(port)

        
        self.resolve_component_structure_from_type(this_context,
                                                   type_context,
                                                   component)

    def resolve_regime(self, context, regime):
        """
        Resolves name references in the given behavior regime to actual
        objects.

        @param context: Current context.
        @type context: pylems.model.context.Context

        @param regime: Behavior regime to be resolved.
        @type regime: pylems.model.behavior.Behavior

        @raise ModelError: Raised when the quantity to be recorded is not a
        path.

        @raise ModelError: Raised when the color specified is not a text
        entity.
        """

        # Resolve record statements
        for idx in regime.records:
            record = regime.records[idx]

            if record.quantity in context.parameters and \
               record.scale in context.parameters and \
               record.color in context.parameters:
                qp = context.parameters[record.quantity]
                sp = context.parameters[record.scale]
                cp = context.parameters[record.color]

                if qp.dimension != '__path__':
                    self.raise_error('<Record>: The quantity to be recorded'
                                     'must be a path',
                                     context)
                if cp.dimension != '__text__':
                    self.raise_error('<Record>: The color to be used must be '
                                     'a reference to a text variable',
                                     context)
                record.quantity = qp.value
                record.scale = sp.value
                record.color = cp.value
                record.numeric_scale = sp.numeric_value

    def resolve_behavior_profile(self, context, behavior):
        """
        Resolves name references in the given behavior profile to actual
        objects.

        @param context: Current context.
        @type context: pylems.model.context.Context

        @param behavior: Behavior profile to be resolved.
        @type behavior: pylems.model.behavior.Behavior
        """

        self.resolve_regime(context, behavior.default_regime)
        
        for rn in behavior.regimes:
            self.resolve_regime(context, regime)
            
    def resolve_component(self, context, component):
        """
        Resolves the specified component.

        @param context: Context object containing the component.
        @type context: pylems.model.context.Context

        @param component: Component to be resolved.
        @type component: pylems.model.component.Component

        @raise ModelError: Raised when the dimension for a parameter cannot
        be resolved.
        """

        self.resolve_context(component.context)
        if component.extends:
            self.resolve_extended_component(context, component)
        self.resolve_component_from_type(context, component)
        for pn in component.context.parameters:
            p = component.context.parameters[pn]
            if p.dimension == '__dimension_inherited__':
                self.raise_error(('The dimension for parameter {0} in '
                                  'component {1} could not be resolved').\
                                 format(pn, component.id),
                                 component.context)

        # Resolve behavior
        for bpn in component.context.behavior_profiles:
            bp = component.context.behavior_profiles[bpn]
            self.resolve_behavior_profile(component.context, bp)

    def resolve_child(self, context, child):
        """
        Resolves the specified child component.

        @param context: Context object containing the component.
        @type context: pylems.model.context.Context

        @param child: Child component to be resolved.
        @type child: pylems.model.component.Component

        @raise ModelError: Raised when the parent component cannot be
        resolved.

        @raise ModelError: Raised when the component type for the parent
        component cannot be resolved.
        """

        parent = context.lookup_component(context.name)
        if parent == None:
            self.raise_error('Unable to resolve component \'{0}\''.\
                             format(context.name))
        parent_type = context.lookup_component_type(parent.component_type)
        if parent_type == None:
            self.raise_error('Unable to resolve component type \'{0}\''.\
                             format(parent.component_type))

        ptctx = parent_type.context

        if child.id in ptctx.child_defs:
            if child.component_type == '__type_inherited__':
                child.component_type = ptctx.child_defs[child.id]
            else:
                raise Exception('TODO')
            context.add_component(child)
        else:
            for cdn in ptctx.children_defs:
                cdt = ptctx.children_defs[cdn]
                if child.component_type == cdt:
                    context.add_component(child)
                    break

    def resolve_context(self, context):
        """
        Resolves name references in the given context to actual objects.

        @param context: Context to be resolved.
        @type context: pylems.model.context.Context

        @raise ModelError: Raised when the dimension for a parameter cannot
        be resolved.
        """
        
        # Resolve component-types
        for ctn in context.component_types:
            component_type = context.component_types[ctn]
            self.resolve_context(component_type.context)
            if component_type.extends:
                self.resolve_extended_component_type(context, component_type)
            
        # Resolve children
        if context.children:
            for child in context.children:
                self.resolve_child(context, child)

        # Resolve components
        for cid in context.components:
            component = context.components[cid]
            self.resolve_component(context, component)

    def resolve_model(self):
        """
        Resolves name references in the model to actual objects.

        @raise ModelError: Raised when the dimension for a given unit cannot
        be resolved.
        """
        
        # Verify dimensions for units
        for symbol in self.units:
            dimension = self.units[symbol].dimension
            if dimension not in self.dimensions:
                self.raise_error('Dimension {0} not defined for unit {1}'\
                                 .format(dimension, symbol),
                                 self.context)

        # Resolve global context
        self.resolve_context(self.context)

    def raise_error(self, message, context):
        s = 'Caught ModelError in lems'

        context_name_stack = []
        while context != None:
            context_name_stack.insert(0, context.name)
            context = context.parent

        for context_name in context_name_stack:
            s += '.' + context_name
            
        s += ':\n  ' + message

        raise ModelError(s)
    
    #####################################################################33

    tab = '  '

    def regime2str(self, regime, prefix):
        s = ''
        if regime.state_variables:
            s += prefix + Model.tab + 'State variables:\n'
            for svn in regime.state_variables:
                sv = regime.state_variables[svn]
                s += prefix + Model.tab*2 + sv.name
                if sv.exposure:
                    s += ' (exposed as ' + sv.exposure + ')'
                s += ': ' + sv.dimension + '\n'

        if regime.time_derivatives:
            s += prefix + Model.tab + 'Time derivatives:\n'
            for tdv in regime.time_derivatives:
                td = regime.time_derivatives[tdv]
                s += prefix + Model.tab*2 + td.variable + ' = ' + td.value\
                     + ' | ' + str(td.expression_tree) + '\n'

        if regime.event_handlers:
            s += prefix + Model.tab + 'Event Handlers:\n'
            for eh in regime.event_handlers:
                s += prefix + Model.tab*2 + str(eh) + '\n'
                if eh.actions:
                    s += prefix + Model.tab*3 + 'Actions:\n'
                    for a in eh.actions:
                        s += prefix + Model.tab*4 + str(a) + '\n'

        if regime.runs:
            s += prefix + Model.tab + 'Runs:\n'
            for r in regime.runs:
                run = regime.runs[r]
                s += prefix + Model.tab*2 + run.component + ': ' + \
                     run.variable + ' ' + run.increment + ' ' + run.total + \
                     '\n'

        if regime.records:
            s += prefix + Model.tab + 'Recorded variables:\n'
            for rn in regime.records:
                rec = regime.records[rn]
                s += prefix + Model.tab*2 + rec.quantity + ': '
                s += rec.scale
                if rec.numeric_scale:
                    s += ' (' + str(rec.numeric_scale) + ')'
                s += ', ' + rec.color + '\n'
                
        if regime.shows:
            s += prefix + Model.tab + 'Shows:\n'
            for sn in regime.shows:
                sh = regime.shows[sn]
                s += prefix + Model.tab*2 + rec.src + '\n'
                
        return s
    
    def behavior2str(self, behavior, prefix):
        s = prefix
        if behavior.name != '':
            s += name
        else:
            s += '*'
        s += '\n'

        if behavior.default_regime:
            s += prefix + Model.tab + 'Default regime:\n'
            s += self.regime2str(behavior.default_regime,
                                 prefix + Model.tab)

        return s

    def structure2str(self, structure, prefix):
        s = prefix + 'Structure:\n'

        if structure.event_connections:
            s += prefix + Model.tab + 'Event connections:\n'
            for conn in structure.event_connections:
                (from_, fromport, to, toport) = conn
                s += prefix + Model.tab*2 + '{0}:{1} -> {2}:{3}\n'.format(\
                    from_, fromport, to, toport)

        if structure.single_child_defs:
            s += prefix + Model.tab + 'Single child instantiations:\n'
            for c in structure.single_child_defs:
                s += prefix + Model.tab*2 + c + '\n'

        if structure.multi_child_defs:
            s += prefix + Model.tab + 'Multi child instantiations:\n'
            for c in structure.multi_child_defs:
                s += prefix + Model.tab*2 + '{0} * {1}\n'.format(\
                    c, structure.multi_child_defs[c])

                
        return s

    def context2str(self, context, prefix):
        s = ''
        prefix = prefix + Model.tab
        if context.component_types:
            s += prefix + 'Component types:\n'
            for tn in context.component_types:
                t = context.component_types[tn]
                s += prefix + Model.tab + t.name
                if t.extends:
                    s += ' (extends ' + t.extends + ')'
                s += '\n'
                s += self.context2str(t.context, prefix + Model.tab)

        if context.components:
            s += prefix + 'Components:\n'
            for cn in context.components:
                c = context.components[cn]
                s += prefix + Model.tab + c.id
                if c.component_type:
                    s += ': ' + c.component_type + '\n'
                else:
                    s+= ' (extends ' + c.extends + ')' + '\n'
                s += self.context2str(c.context, prefix + Model.tab)

        if context.component_refs:
            s += prefix + 'Component references:\n'
            for cref in context.component_refs:
                t = context.component_refs[cref]
                s += prefix + Model.tab + cref + ': ' + t + '\n'

        if context.child_defs:
            s += prefix + 'Child definitions:\n'
            for cref in context.child_defs:
                t = context.child_defs[cref]
                s += prefix + Model.tab + cref + ': ' + t + '\n'

        if context.children_defs:
            s += prefix + 'Children definitions:\n'
            for cref in context.children_defs:
                t = context.children_defs[cref]
                s += prefix + Model.tab + cref + ': ' + t + '\n'

        if context.children:
            s += prefix + 'Children:\n'
            for child in context.children:
                s += prefix + Model.tab + child.id + ': ' + \
                     child.component_type + '\n'

        if context.parameters:
            s += prefix + 'Parameters:\n'
            for pn in context.parameters:
                p = context.parameters[pn]
                s += prefix + Model.tab + p.name
                s += ': ' + p.dimension
                if p.value:
                    s += ': ' + str(p.value)
                    if p.fixed:
                        s += ' (fixed)'
                if p.numeric_value:
                    s += ' - ' + str(p.numeric_value)
                s += '\n'

        if context.exposures:
            s += prefix + 'Exposures:\n'
            for name in context.exposures:
                s += prefix + Model.tab + name + '\n'

        if context.texts:
            s += prefix + 'Text variables:\n'
            for name in context.texts:
                value = context.texts[name]
                s += prefix + Model.tab + name
                if value:
                    s += ': ' + value + '\n'
                else:
                    s += '\n'

        if context.paths:
            s += prefix + 'Path variables:\n'
            for name in context.paths:
                value = context.paths[name]
                s += prefix + Model.tab + name
                if value:
                    s += ': ' + value + '\n'
                else:
                    s += '\n'

        if context.behavior_profiles:
            s += prefix + 'Behavior profiles:\n'
            for name in context.behavior_profiles:
                behavior = context.behavior_profiles[name]
                s += self.behavior2str(behavior, prefix + Model.tab*2)

        if context.event_in_ports:
            s += prefix + 'Event in ports:\n'
            for port in context.event_in_ports:
                s += prefix + Model.tab + port + '\n'

        if context.event_out_ports:
            s += prefix + 'Event out ports:\n'
            for port in context.event_in_ports:
                s += prefix + Model.tab + port + '\n'

        if context.structure:
            s += self.structure2str(context.structure, prefix)
            
        return s
    
    def __str__(self):
        s = ''

        s += 'Default run:\n'
        for run in self.default_runs:
            s += Model.tab + run + '\n'
        
        s += 'Dimensions:\n'
        if self.dimensions != None:
            for d in self.dimensions:
                s += Model.tab + d + '\n'

        s += 'Units:\n'
        if self.units != None:
            for u in self.units:
                s += Model.tab + u + '\n'

        if self.context:
            s += 'Global context:\n'
            s += self.context2str(self.context, '')
            
        return s

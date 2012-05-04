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
            raise ModelError('Duplicate dimension - ' + dimension.name)
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
            raise ModelError('Duplicate unit - ' + unit.symbol)
        else:
            self.units[unit.symbol] = unit

    def resolve_parameter_value(self, parameter):
        """
        Resolves the numeric value of a parameter based on the given value
        in terms of the symbols and dimensions defined in the model.

        @param parameter: Parameter object to be resolved.
        @type parameter: pylems.model.parameter.Parameter

        @raise ModelError: Raised when the value of the parameter is not set.

        @raise ModelError: Raised when the unit symbol does not match the
        parameter's dimension.

        @raise ModelError: Raised when the unit symbol is undefined.
        """
        
        if parameter.value == None:
            raise ModelError('Parameter {0} not initialized'.format(\
                parameter.name))

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
                        raise ModelError(('Unit symbol {0} cannot '
                                         'be used for dimension {1}').format(\
                                             sym, parameter.dimension))
                parameter.numeric_value = number * (10 ** unit.pow10)
            else:
                raise ModelError('Unknown unit symbol {0}'.format(sym))

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
            raise ModelError('Base type {0} not found for component type {1}'.
                             format(component_type.extends,
                                    component_type.name))
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
                    raise ModelError(('Parameter {0} in {1} is redefined ' +
                                     'in {2}').format(pn, base_type.name,
                                                      component_type.name))
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
        is redefined in this component type.

        @note: Consider changing Component.id to Component.name and merging
        this method with resolve_extended_component_type.
        """
        
        base = context.lookup_component(component.extends)
        if base == None:
            raise ModelError('Base component {0} not found for component {1}'.
                             format(component.extends,
                                    component.id))
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
                    raise ModelError(('Parameter {0} in {1} is redefined ' +
                                     'in {2}').format(pn, base_type.name,
                                                      component_type.name))
            else:
                this_context.parameters[pn] = base_context.parameters[pn].\
                                              copy()

        component.extends = None

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
            raise ModelError('Type {0} not found for component {1}'.
                             format(component.component_type, component.id))

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

            self.resolve_parameter_value(this_context.parameters[pn])

        for pn in this_context.parameters:
            pc = this_context.parameters[pn]
            if pc.dimension == '__dimension_inherited__':
                if pn in type_context.texts:
                    pc.dimension = '__text__'
                    this_context.texts[pn] = type_context.texts[pn]
                elif pn in type_context.paths:
                    pc.dimension = '__path__'
                    this_context.paths[pn] = type_context.paths[pn]
                elif pn in type_context.component_refs:
                    pc.dimension = '__component_ref__'
                    cf = type_context.component_refs[pn]
                    this_context.component_refs[pn] = pc.value

        this_context.behavior_profiles = type_context.behavior_profiles
        bpn = type_context.selected_behavior_profile
        this_context.selected_behavior_profile = bpn
                                                    

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
            
        # Resolve components
        for cid in context.components:
            component = context.components[cid]
            self.resolve_context(component.context)
            self.resolve_component_from_type(context, component)
            if component.extends:
                self.resolve_extended_component(context, component)
            for pn in component.context.parameters:
                p = component.context.parameters[pn]
                if p.dimension == '__dimension_inherited__':
                    raise ModelError(('The dimension for parameter {0} in '
                                      'component {1} could not be resolved').\
                                     format(pn, component.id))
                    pass
                                     

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
                raise ModelError('Dimension {0} not defined for unit {1}'\
                                 .format(dimension, symbol))

        # Resolve global context
        self.resolve_context(self.context)
    
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
                td = regime.time_derivatives[tdv]
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

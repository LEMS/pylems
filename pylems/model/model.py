"""
Model storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.errors import ModelError
from pylems.model.context import Contextual

class Model(Contextual):
    """
    Store the model read from a LEMS file.
    """

    def __init__(self):
        """
        Constructor.
        """

        super(Model, self).__init__()
        
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

    def resolve_context(self, model):
        pass
    
    def resolve_model(self):
        pass

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
                s += prefix + Model.tab*2 + run.component + '\n'

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
                s += '\n'

        if context.exposures:
            s += prefix + 'Exposures:\n'
            for name in context.exposures:
                s += prefix + Model.tab + name + '\n'

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

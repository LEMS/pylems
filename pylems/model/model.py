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

    default_run = ''
    """ Name of the default simulation to run.
    @type: string """

    dimensions = None
    """ Dictionary of references to dimensions defined in the model.
    @type: dict(string -> pylems.model.simple.Dimension) """

    units = None
    """ Dictionary of references to units defined in the model.
    @type: dict(string -> pylems.model.simple.Unit) """

    context = None
    """ Root context
    @type: pylems.model.context.Context """

    def set_default_run(self, default_run):
        """
        Set the name of the default simulation to run.
        
        @param default_run: Name of a simulation to run by default
        @type default_run: string """
        self.default_run = default_run

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

    def __str__(self):
        s = ''

        s += 'Default run: ' + self.default_run + '\n'
        
        s += 'Dimensions:\n'
        if self.dimensions != None:
            for d in self.dimensions:
                s += '  ' + d + '\n'

        s += 'Units:\n'
        if self.units != None:
            for u in self.units:
                s += '  ' + u + '\n'

        if self.context:
            if self.context.component_types:
                s += 'Component types:\n'
                for tn in self.context.component_types:
                    t = self.context.component_types[tn]
                    s += '  ' + t.name
                    print t.name,t.extends
                    if t.extends:
                        s += ' extends ' + t.extends.name
                    s += '\n'

                    if t.parameter_types:
                        for pn in t.parameter_types:
                            p = t.parameter_types[pn]
                            s += '    ' + p.name + ': ' + p.dimension.name + '\n'

            
        return s

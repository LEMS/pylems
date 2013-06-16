"""
Behavioral dynamics.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase
from lems.util import Map

class StateVariable(LEMSBase):
    """
    Store the specification of a state variable.
    """

    def __init__(self, name, dimension, exposure = None):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        self.name = name
        """ Name of the state variable.
        @type: str """

        self.dimension = dimension
        """ Dimension of the state variable.
        @type: str """

        self.exposure = exposure
        """ Exposure name for the state variable.
        @type: str """

class DerivedVariable(LEMSBase):
    """
    Store the specification of a derived variable.
    """

    def __init__(self, name, **params):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        self.name = name
        """ Name of the derived variable.
        @type: str """

        self.dimension = params['dimension'] if 'dimension' in params else None
        """ Dimension of the derived variable or None if computed.
        @type: str """

        self.exposure = params['exposure'] if 'exposure' in params else None
        """ Exposure name for the derived variable.
        @type: str """

        self.select = params['select'] if 'select' in params else None
        """ Selection path/expression for the derived variable.
        @type: str """

        self.value = params['value'] if 'value' in params else None
        """ Value of the derived variable.
        @type: str """

        self.reduce = params['reduce'] if 'reduce' in params else None
        """ Reduce method for the derived variable.
        @type: str """

        self.required = params['required'] if 'required' in params else None
        """ Requried or not.
        @type: str """

class TimeDerivative(LEMSBase):
    """
    Store the specification of a time derivative specifcation.
    """

    def __init__(self, variable, value):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        self.variable = variable
        """ Name of the variable for which the time derivative is being specified..
        @type: str """

        self.value = value
        """ Derivative expression.
        @type: str """
        

class Regime(LEMSBase):
    """
    Stores a single behavioral regime for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.state_variables = Map()
        """ Map of state variables in this behavior regime.
        @type: dict(str -> lems.model.dynamics.StateVariable """

        self.derived_variables = Map()
        """ Map of derived variables in this behavior regime.
        @type: dict(str -> lems.model.dynamics.DerivedVariable """

        self.time_derivatives = Map()
        """ Map of time derivatives in this behavior regime.
        @type: dict(str -> lems.model.dynamics.TimeDerivative) """

    def add_state_variable(self, sv):
        """
        Adds a state variable to this behavior regime.

        @param sv: State variable.
        @type sv: lems.model.dynamics.StateVariable
        """

        self.state_variables[sv.name] = sv
        
    def add_derived_variable(self, dv):
        """
        Adds a derived variable to this behavior regime.

        @param dv: Derived variable.
        @type dv: lems.model.dynamics.DerivedVariable
        """

        self.derived_variables[dv.name] = dv
        
    def add_time_derivative(self, td):
        """
        Adds a time derivative to this behavior regime.

        @param td: Time derivative.
        @type td: lems.model.dynamics.TimeDerivative
        """

        self.time_derivatives[td.variable] = td
        

class Dynamics(Regime):
    """
    Stores behavioral dynamics specification for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        Regime.__init__(self)

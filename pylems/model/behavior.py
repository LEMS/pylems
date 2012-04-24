"""
Behavior storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.parser.expr import ExprParser

class StateVariable(PyLEMSBase):
    """
    Stores the definition of a state variable.
    """

    def __init__(self, name, exposure, dimension):
        """
        Constructor.

        @param name: Name (internal) of the state variable.
        @type name: string

        @param exposure: Name (external) of the state variable.
        @type exposure: string

        @param dimension: Dimension of the state variable.
        @type dimension: string
        """

        self.name = name
        """ Internal name of the state variable. This is the name used to refer
        to this variable inside the <Behavior> element.
        @type: string """
        
        self.exposure = exposure
        """ Exposure name of the state variable. This is the name used to refer
        to this variable from other objects.
        @type: string """
        
        self.dimension = dimension
        """ Dimension of this state variable.
        @type: string """

class TimeDerivative(PyLEMSBase):
    """
    Stores the time derivative expression for a given state variable.
    """

    def __init__(self, variable, value):
        """
        Constructor.

        @param variable: Name of the state variable
        @type variable: string

        @param value: Time derivative expression of the given state variable.
        @type value: string
        """

        self.variable = variable
        """ State variable whose time derivative is stored in this object.
        @type: string """

        self.value = value
        """ Time derivative expression for the state variable.
        @type: string """

        self.expression_tree = ExprParser(value).parse()
        """ Parse tree for the time derivative expression.
        @type: pylems.parser.expr.ExprNode """

class Action(PyLEMSBase):
    """
    Base class for an event action.
    """
    
    STATE_ASSIGNMENT = 1
    EVENT_OUT = 2

    def __init__(self, type):
        self.type = type
        """ Type of action.
        @type: enum(Action.STATEASSIGNMENT, Action.EVENT_OUT) """

class StateAssignment(Action):
    """
    Stores a state assignment expression.
    """

    def __init__(self, variable, value):
        """
        Constructor.

        @param variable: Name of the state variable
        @type variable: string

        @param value: Assignment expression of the given state variable.
        @type value: string
        """

        Action.__init__(self. Action.STATE_ASSIGNMENT)

        self.variable = variable
        """ State variable whose assignment expression is stored in this object.
        @type: string """

        self.value = value
        """ Assignment expression for the state variable.
        @type: string """

        self.expression_tree = ExprParser(value).parse()
        """ Parse tree for the assignment expression.
        @type: pylems.parser.expr.ExprNode """

class Event(PyLEMSBase):
    pass

class OnStart(Event):
    pass

class OnCondition(Event):
    pass

class Behavior(PyLEMSBase):
    """
    Stores the behavior characteristics for an object.
    """

    def __init__(self, name):
        """
        Constructor.
        """
        
        self.name = name
        """ Name of this behavior profile.
        @type: string """

        self.state_variables = None
        """ Dictionary of state variables defined in this behavior profile.
        @type: dict(string -> pylems.model.behavior.StateVariable) """
    
        self.time_derivatives = None
        """ Dictionary of time derivatives defined in this behavior profile.
        @type: dict(string -> pylems.model.behavior.TimeDerivative) """
    
    def add_state_variable(self, name, exposure, dimension):
        """
        Adds a state variable to the behavior current object.

        @param name: Name of the state variable.
        @type name: string

        @param exposure: Exposed name of the state variable.
        @type exposure: string

        @param dimension: Dimension ofthe state variable.
        @type dimension: string

        @raise ModelError: Raised when the state variable is already
        defined in this behavior profile.
        """

        if self.state_variables != None and name in self.state_variables:
            raise ModelError('Duplicate state variable ' + name)

        if self.state_variables == None:
            self.state_variables = dict()

        self.state_variables[name] = StateVariable(name, exposure, dimension)

    def add_time_derivative(self, variable, value):
        """
        Adds a state variable to the behavior current object.

        @param variable: Name of the state variable whose time derivative
        is being specified.
        @type variable: string

        @param value: Time derivative expression.
        @type value: string

        @raise ModelError: Raised when the time derivative for this state
        variable is already defined in this behavior profile.
        """

        if self.time_derivatives != None and variable in self.time_derivatives:
            raise ModelError('Duplicate time derivative for ' + variable)

        if self.time_derivatives == None:
            self.time_derivatives = dict()

        self.time_derivatives[variable] = TimeDerivative(variable, value)

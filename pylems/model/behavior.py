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

class Run(PyLEMSBase):
    """
    Stores the description of an object to be run according to an independent
    variable (usually time).
    """

    def __init__(self, component, variable, increment, total):
        """
        Constructor.

        @param component: Name of the target component to be run according to
        the specification given for an independent state variable.
        @type component: string
        
        @param variable: The name of an independent state variable according to
        which the target component will be run.
        @type variable: string

        @param increment: Increment of the state variable on each step.
        @type increment: string

        @param total: Final value of the state variable.
        @type total: string
        """
        
        self.component = component
        """ Name of the target component to be run according to the
        specification given for an independent state variable.
        @type: string """
        
        self.variable = variable
        """ The name of an independent state variable according to which the
        target component will be run.
        @type: string """
        
        self.increment = increment
        """ Increment of the state variable on each step.
        @type: string """
        
        self.total = total
        """ Final value of the state variable.
        @type: string """
        

class Record(PyLEMSBase):
    def __init__(self, quantity, scale, color, save):
        self.quantity = quantity
        self.scale = scalte
        self.color = color
        self.save = save

class Show(PyLEMSBase):
    def __init__(self, scale, src):
        self.scale = scale
        self.src = src
    
class EventHandler(PyLEMSBase):
    """
    Base class for event an handler.
    """

    ON_START = 1
    ON_ENTRY = 2
    ON_EVENT = 3
    ON_CONDITION = 4

    def __init__(self, type):
        """
        Constructor.

        @param type: Type of event.
        @type type: enum(EventHandler.ONSTART, EventHandler.ON_ENTRY,
        EventHandler.ON_EVENT and EventHandler.ON_CONDITION)
        """
        
        self.type = type
        """ Type of event.
        @type: enum(EventHandler.ONSTART, EventHandler.ON_ENTRY,
        EventHandler.ON_EVENT and EventHandler.ON_CONDITION) """

        self.actions = None
        "List of actions to be performed on the occurence of the event."

    def add_action(self, action):
        """
        Adds an action to the list of actions.

        @param action: Action to be performed.
        @type action: pylems.model.behavior.Action
        """

        if self.actions == None:
            self.actions = []

        self.actions += [action]

    def check_for_event(self):
        """
        Check for the event. If this function returns true, the corresponding
        event actions will be executed.

        @return: Check if the event has occurred.
        @rtype: Boolean

        @note: This function must be overridden. Maybe when building the
        simulator?
        """

        return False
    
class OnStart(EventHandler):
    pass
    
class OnEntry(EventHandler):
    pass
    
class OnEvent(EventHandler):
    pass
    
class OnCondition(EventHandler):
    """
    Event handler for a condition check.
    """

    def __init__(self, test):
        """
        Constructor.

        @param test: Test expression.
        @type test: string
        """

        EventHandler.__init__(self, EventHandler.ON_CONDITION)

        self.test = test
        """ Test expression.
        @type: string """

        self.expression_tree = ExprParser(test).parse()
        """ Parse tree for the test expression.
        @type: pylems.parser.expr.ExprNode """

    def __str__(self):
        """ Generates a string representation of this condition."""
        
        return 'OnCondition: ' + self.test + ' | ' +\
               str(self.expression_tree)
        
class Action(PyLEMSBase):
    """
    Base class for an event action.
    """
    
    STATE_ASSIGNMENT = 1
    EVENT_OUT = 2
    TRANSITION = 3

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

        Action.__init__(self, Action.STATE_ASSIGNMENT)

        self.variable = variable
        """ State variable whose assignment expression is stored in this object.
        @type: string """

        self.value = value
        """ Assignment expression for the state variable.
        @type: string """

        self.expression_tree = ExprParser(value).parse()
        """ Parse tree for the assignment expression.
        @type: pylems.parser.expr.ExprNode """

    def __str__(self):
        """ Generates a string representation of this state assigment """

        return self.variable + ' <- ' + self.value + ' | ' + \
               str(self.expression_tree)

class Regime(PyLEMSBase):
    """
    Store a behavior regime for a component type.
    """

    def __init__(self, name, initial = False):
        """
        Constructor.

        @param name: Name of the behavior regime.
        @type name: string

        @param initial: Is this the initial regime? Default: False
        @type initial: Boolean
        """
        
        self.name = name
        """ Name of this ehavior regime.
        @type: string """

        self.initial = initial
        """ Is this an initial regime?
        @type: Boolean """

        self.state_variables = {}
        """ Dictionary of state variables defined in this behavior regime.
        @type: dict(string -> pylems.model.behavior.StateVariable) """
    
        self.time_derivatives = {}
        """ Dictionary of time derivatives defined in this behavior regime.
        @type: dict(string -> pylems.model.behavior.TimeDerivative) """

        self.event_handlers = []
        """ List of event handlers defined in this behavior regime.
        @type: list(EventHandler) """

        self.runs = {}
        """ Dictionary of runs in this behavior profile.
        @type: dict(string -> pylems.model.behavior.Run) """

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
        defined in this behavior regime.
        """

        if name in self.state_variables:
            raise ModelError('Duplicate state variable ' + name)

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
        variable is already defined in this behavior regime.
        """

        if variable in self.time_derivatives:
            raise ModelError('Duplicate time derivative for ' + variable)

        self.time_derivatives[variable] = TimeDerivative(variable, value)
    
    def add_event_handler(self, event_handler):
        """
        Adds a state variable to the behavior current object.

        @param event_handler: Event handler object.
        @type event_handler: pylems.model.behavior.EventHandler
        """

        self.event_handlers += [event_handler]

    def add_run(self, component, variable, increment, total):
        """
        Adds a runnable target component definition to the list of runnable
        components stored in this context.

        @param component: Name of the target component to be run.
        @type component: string

        @param variable: Name of an indendent state variable used to control
        the target component (usually time).
        @type variable: string

        @param increment: Value by which the control variable is to be
        incremented in each step.
        @type increment: string

        @param total: End value for the control variable.
        @type total: string
        """

        if component in self.runs:
            raise ModelError('Duplicate run for ' + component)

        self.runs[component] = Run(component, variable, increment, total)

class Behavior(PyLEMSBase):
    """
    Stores the behavior characteristics for a component type.
    """

    def __init__(self, name):
        """
        Constructor.
        """
        
        self.name = name
        """ Name of this behavior profile.
        @type: string """

        self.default_regime = Regime('')
        """ Default behavior regime for this behavior profile. This regime
        is used to store behavior object not defined within a named regime.
        @type: pylems.model.behavior.Regime """

        self.current_regime = None
        """ Currently active behavior regime for this behavior profile.
        @type: pylems.model.behavior.Regime """

        self.regimes = dict()
        """ Dictionary of regimes in this behavior profile.
        @type: dict(string -> pylems.model.behavior.Regime) """

    def add_regime(self, name, initial = False):
        """
        Adds a behavior regime to the list of regimes in this behavior
        profile.

        @param name: Name of the behavior regime.
        @type name: string

        @param initial: Is this the initial regime? Default: False
        @type initial: Boolean
        """
        
        if name in self.regimes:
            raise ModelError('Duplicate regime ' + name)

        if initial:
            for rn in self.regimes:
                if self.regimes[rn].initial:
                    raise('Cannot define two initial regimes in the same' +
                          ' behavior profile')
            
        regime = Regime(name, initial)
        if initial:
            self.current_regime = regime
        
        self.regimes[name] = regime

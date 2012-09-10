"""
Component behavior storage.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import PyLEMSBase
from lems.base.errors import ModelError,ParseError
from lems.parser.expr import ExprParser

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
        """ Internal name of the state variable. This is the name used to
        refer to this variable inside the <Behavior> element.
        @type: string """
        
        self.exposure = exposure
        """ Exposure name of the state variable. This is the name used to
        refer to this variable from other objects.
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

        try:
            self.expression_tree = ExprParser(value).parse()
            """ Parse tree for the time derivative expression.
            @type: pylems.parser.expr.ExprNode """
        except:
            raise ParseError("Parse error when parsing value expression "
                             "'{0}' for derived variable {1}".format(\
                                 self.value,
                                 self.variable))

class DerivedVariable(PyLEMSBase):
    """
    Stores the definition of a derived variable.
    """

    def __init__(self, name, exposure, dimension, value, select, reduce):
        """
        Constructor.

        @param name: Name (internal) of the derived variable.
        @type name: string

        @param exposure: Name (external) of the derived variable.
        @type exposure: string

        @param dimension: Dimension of the derived variable.
        @type dimension: string

        @param value: Value expression for the derived variable.
        @type value: string

        @param select: Target component selection for reduction operations.
        @type select: string

        @param reduce: Reduce operation.
        @type reduce: string
        """

        self.name = name
        """ Internal name of the derived variable. This is the name used to
        refer to this variable inside the <Behavior> element.
        @type: string """
        
        self.exposure = exposure
        """ Exposure name of the derived variable. This is the name used to
        refer to this variable from other objects.
        @type: string """
        
        self.dimension = dimension
        """ Dimension of this derived variable.
        @type: string """

        self.value = value
        """ Expression used for computing the value of the derived variable.
        @type: string """

        self.select = select
        """ Selected target object for the reduce operation.
        @type: string """
        
        self.reduce = reduce
        """ Reduce operation to be applied over the selected target.
        @type: string """

        if value != None:
            try:
                self.expression_tree = ExprParser(value).parse()
                """ Parse tree for the time derivative expression.
                @type: pylems.parser.expr.ExprNode """
            except:
                raise ParseError("Parse error when parsing value expression "
                                 "'{0}' for derived variable {1}".format(\
                                     self.value,
                                     self.name))
        else:
            self.expression_tree = None
                

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
        
        @param variable: The name of an independent state variable according
        to which the target component will be run.
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
    """
    Stores the parameters of a <Record> statement.
    """
    
    def __init__(self, quantity, scale, color):
        self.quantity = quantity
        self.scale = scale
        self.color = color

        self.numeric_scale = None
        
class Show(PyLEMSBase):
    """
    Stores the parameters of a <Show> statement.
    """
    
    def __init__(self, src, scale):
        self.src = src
        self.scale = scale
    
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
    """
    Stores the parameters of an <OnStart> statement.
    """

    def __init__(self):
        """
        Constructor.
        """

        EventHandler.__init__(self, EventHandler.ON_START)

    def __str__(self):
        """ Generates a string representation of this condition."""
        
        return 'OnStart'
        
class OnEntry(EventHandler):
    """
    Stores the parameters of an <OnEntry> statement.
    """

    def __init__(self):
        """
        Constructor.
        """

        EventHandler.__init__(self, EventHandler.ON_ENTRY)

    def __str__(self):
        """ Generates a string representation of this condition."""
        
        return 'OnEntry'
        
class OnEvent(EventHandler):
    """
    Stores the parameters of an <OnEvent> statement.
    """

    def __init__(self, port):
        """
        Constructor.

        @param port: The name of the event port to listen on.
        @type port: string
        """

        EventHandler.__init__(self, EventHandler.ON_EVENT)
        
        self.port = port
        """ The name of the event port to listen on.
        @type: string """

    def __str__(self):
        """ Generates a string representation of this condition."""
        
        return 'OnEvent: ' + self.port
    
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
        """
        Constructor.

        @param type: Type of action.
        @type type: enum(Action.STATEASSIGNMENT, Action.EVENT_OUT)
        """
        
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
        """ State variable whose assignment expression is stored in this
        object.
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

class EventOut(Action):
    """
    Stores a state assignment expression.
    """

    def __init__(self, port):
        """
        Constructor.

        @param port: Name of a port
        @type port: string
        """

        Action.__init__(self, Action.EVENT_OUT)

        self.port = port
        """ Name of the port to which the event needs to be sent.
        @type: string """

    def __str__(self):
        """ Generates a string representation of this state assigment """

        return 'Event -> ' + self.port

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

        self.derived_variables = {}
        """ Dictionary of derived variables defined in this behavior regime.
        @type: dict(string -> pylems.model.behavior.DerivedVariable) """
    
        self.event_handlers = []
        """ List of event handlers defined in this behavior regime.
        @type: list(EventHandler) """

        self.runs = {}
        """ Dictionary of runs in this behavior regime.
        @type: dict(string -> pylems.model.behavior.Run) """
        
        self.records = {}
        """ Dictionary of recorded variables in this behavior regime.
        @type: dict(string -> pylems.model.behavior.Record """

        self.shows = {}
        """ Dictionary of recorded variables in this behavior regime.
        @type: dict(string -> pylems.model.behavior.Record """

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
    
    def add_derived_variable(self, name, exposure, dimension,
                             value, select, reduce):
        """
        Adds a derived variable to the behavior current object.

        @param name: Name of the derived variable.
        @type name: string

        @param exposure: Exposed name of the derived variable.
        @type exposure: string

        @param dimension: Dimension ofthe derived variable.
        @type dimension: string

        @param value: Value expression for the derived variable.
        @type value: string

        @param select: Target component selection for reduction operations.
        @type select: string

        @param reduce: Reduce operation.
        @type reduce: string
        
        @raise ModelError: Raised when the derived variable is already
        defined in this behavior regime.
        """

        if name in self.derived_variables:
            raise ModelError("Duplicate derived variable '{0}'".format(name))

        if value == None and select == None and reduce == None:
            raise ModelError("Derived variable '{0}' must specify either a "
                             "value expression or a reduce "
                             "operation".format(name))

        if value != None and (select != None or reduce != None):
            raise ModelError("Derived variable '{0}' cannot specify both "
                             "value expressions or select/reduce "
                             "operations".format(name))
        
        if select == None and reduce != None:
            raise ModelError("Reduce target not specified for derived "
                             "variable '{0}'".format(name))

        self.derived_variables[name] = DerivedVariable(name, exposure,
                                                       dimension, value,
                                                       select, reduce)
        
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

    def add_record(self, quantity, scale, color):
        """
        Adds a record objects to the list of record objects in this behavior
        regime.

        @param quantity: Path to the quantity to be recorded
        @type quantity: string

        @param scale: Scale of the quantity to be recorded
        @type scale: string

        @param color: Color of the quantity to be recorded as a 24-bit hex
        RGB value (#RRGGBB)
        @type color: string
        """
        
        if quantity in self.records:
            raise ModelError('Duplicate record {0}'.format(quantity))
        
        self.records[quantity] = Record(quantity, scale, color)

    def add_show(self, src, scale):
        """
        Adds a record objects to the list of record objects in this behavior
        regime.

        @param src: Path to the element(s) that defines what should be shown
        @type src: string

        @param scale: Scale of the quantity to be recorded
        @type scale: string
        """
        
        if src in self.shows:
            raise ModelError('Duplicate show {0}'.format(quantity))
        
        self.shows[src] = Record(src, scale)

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

        self.regimes = {}
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

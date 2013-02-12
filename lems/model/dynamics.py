"""
Component dynamics storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.errors import ModelError,ParseError
from lems.parser.expr import ExprParser

from lems.base.util import merge_dict

class StateVariable(LEMSBase):
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
        refer to this variable inside the <Dynamics> element.
        @type: string """

        self.exposure = exposure
        """ Exposure name of the state variable. This is the name used to
        refer to this variable from other objects.
        @type: string """

        self.dimension = dimension
        """ Dimension of this state variable.
        @type: string """

class TimeDerivative(LEMSBase):
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
            @type: lems.parser.expr.ExprNode """
        except:
            raise ParseError("Parse error when parsing value expression "
                             "'{0}' for derived variable {1}".format(\
                                 self.value,
                                 self.variable))

class DerivedVariable(LEMSBase):
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
        refer to this variable inside the <Dynamics> element.
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
                @type: lems.parser.expr.ExprNode """
            except:
                raise ParseError("Parse error when parsing value expression "
                                 "'{0}' for derived variable {1}".format(\
                                     self.value,
                                     self.name))
        else:
            self.expression_tree = None


class EventHandler(LEMSBase):
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

        self.actions = []
        "List of actions to be performed on the occurence of the event."

    def add_action(self, action):
        """
        Adds an action to the list of actions.

        @param action: Action to be performed.
        @type action: lems.model.dynamics.Action
        """

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
        @type: lems.parser.expr.ExprNode """

    def __str__(self):
        """ Generates a string representation of this condition."""

        return 'OnCondition: ' + self.test + ' | ' +\
               str(self.expression_tree)

class Action(LEMSBase):
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
        @type: lems.parser.expr.ExprNode """

    def __str__(self):
        """ Generates a string representation of this state assigment """

        return self.variable + ' <- ' + self.value + ' | ' + \
               str(self.expression_tree)

class EventOut(Action):
    """
    Stores an event out operation.
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

class Transition(Action):
    """
    Stores an regime transition operation.
    """

    def __init__(self, regime):
        """
        Constructor.

        @param regime: Name of a dynamics regime
        @type regime: string
        """

        Action.__init__(self, Action.TRANSITION)

        self.regime = regime
        """ Name of the dynamics regime to switch to.
        @type: string """

    def __str__(self):
        """ Generates a string representation of this state assigment """

        return 'Regime -> ' + self.regime

class KineticScheme(LEMSBase):
    """
    Stores a kinetic scheme specification.
    """

    def __init__(self, name, nodes, state_variable,
                 edges, edge_source, edge_target,
                 forward_rate, reverse_rate):
        """
        Constructor.

        See instance variable documentation for info on parameters.
        """

        self.name = name
        """ Name of the kinetic scheme.
        @type: string """

        self.nodes = nodes
        """ Name of the children collection specifying the nodes
        for the kinetic scheme.
        @type: string """

        self.state_variable = state_variable
        """ Name of the state variable in the KS node specifying
        the value of the scheme.
        @type: string """

        self.edges = edges
        """ Name of the children collection specifying the edges
        for the kinetic scheme.
        @type: string """

        self.edge_source = edge_source
        """ Name of the link in a KS edge pointing to the source
        node for the edge.
        @type: string """

        self.edge_target = edge_target
        """ Name of the link in a KS edge pointing to the target
        node for the edge.
        @type: string """

        self.forward_rate = forward_rate
        """ Name of the state variable in a KS edge specifying
        forward rate for the edge.
        @type: string """

        self.reverse_rate = reverse_rate
        """ Name of the state variable in a KS edge specifying
        reverse rate for the edge.
        @type: string """

class Regime(LEMSBase):
    """
    Store a dynamics regime for a component type.
    """

    def __init__(self, name, initial = False):
        """
        Constructor.

        @param name: Name of the dynamics regime.
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
        """ Dictionary of state variables defined in this dynamics regime.
        @type: dict(string -> lems.model.dynamics.StateVariable) """

        self.time_derivatives = {}
        """ Dictionary of time derivatives defined in this dynamics regime.
        @type: dict(string -> lems.model.dynamics.TimeDerivative) """

        self.derived_variables = {}
        """ Dictionary of derived variables defined in this dynamics regime.
        @type: dict(string -> lems.model.dynamics.DerivedVariable) """

        self.event_handlers = []
        """ List of event handlers defined in this dynamics regime.
        @type: list(EventHandler) """

        self.kinetic_schemes = {}
        """ Dictionary of kinetic schemes defined in this dynamics regime.
        @type: dict(string -> lems.model.dynamics.KineticScheme) """

    def add_state_variable(self, name, exposure, dimension):
        """
        Adds a state variable to the dynamics current object.

        @param name: Name of the state variable.
        @type name: string

        @param exposure: Exposed name of the state variable.
        @type exposure: string

        @param dimension: Dimension ofthe state variable.
        @type dimension: string

        @raise ModelError: Raised when the state variable is already
        defined in this dynamics regime.
        """

        if name in self.state_variables:
            raise ModelError('Duplicate state variable ' + name)

        self.state_variables[name] = StateVariable(name, exposure, dimension)

    def add_time_derivative(self, variable, value):
        """
        Adds a state variable to the dynamics current object.

        @param variable: Name of the state variable whose time derivative
        is being specified.
        @type variable: string

        @param value: Time derivative expression.
        @type value: string

        @raise ModelError: Raised when the time derivative for this state
        variable is already defined in this dynamics regime.
        """

        if variable in self.time_derivatives:
            raise ModelError('Duplicate time derivative for ' + variable)

        self.time_derivatives[variable] = TimeDerivative(variable, value)

    def add_derived_variable(self, name, exposure, dimension,
                             value, select, reduce):
        """
        Adds a derived variable to the dynamics current object.

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
        defined in this dynamics regime.
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
        Adds a state variable to the dynamics current object.

        @param event_handler: Event handler object.
        @type event_handler: lems.model.dynamics.EventHandler
        """

        self.event_handlers += [event_handler]

    def add_kinetic_scheme(self, name, nodes, state_variable,
                           edges, edge_source, edge_target,
                           forward_rate, reverse_rate):
        """
        Constructor.

        See KineticScheme documentation for info on parameters.

        @raise ModelError: Raised if a kinetic scheme with the same
        name already exists in this behavior regime.
        """

        if name in self.kinetic_schemes:
            raise ModelError('Duplicate kinetic scheme ' + name)

        self.kinetic_schemes[name] = KineticScheme(name, nodes, state_variable,
                                                   edges, edge_source, edge_target,
                                                   forward_rate, reverse_rate)

    def merge(self, regime):
        """
        Merge another regime into this one.

        @param regime: Regime to be merged in.
        @type regime: lems.model.dynamics.Regime
        """

        merge_dict(self.state_variables, regime)
        merge_dict(self.time_derivatives, regime.time_derivatives)
        merge_dict(self.derived_variables, regime.derived_variables)

        self.event_handlers += regime.event_handlers

        merge_dict(self.kinetic_schemes, regime.kinetic_schemes)


class Dynamics(LEMSBase):
    """
    Stores the dynamic dynamics for a component type.
    """

    def __init__(self, name):
        """
        Constructor.
        """

        self.name = name
        """ Name of this dynamics profile.
        @type: string """

        self.default_regime = Regime('')
        """ Default dynamics regime for this dynamics profile. This regime
        is used to store dynamics object not defined within a named regime.
        @type: lems.model.dynamics.Regime """

        self.current_regime = None
        """ Currently active dynamics regime for this dynamics profile.
        @type: lems.model.dynamics.Regime """

        self.regimes = {}
        """ Dictionary of regimes in this dynamics profile.
        @type: dict(string -> lems.model.dynamics.Regime) """

    def add_regime(self, name, initial = False):
        """
        Adds a dynamics regime to the list of regimes in this dynamics
        profile.

        @param name: Name of the dynamics regime.
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
                          ' dynamics profile')

        regime = Regime(name, initial)
        if initial:
            self.current_regime = regime

        self.regimes[name] = regime

    def merge(self, dynamics):
        """
        Merge another dynamics profile into this one.

        @param dynamics: Dynamics profile to be merged in.
        @type dynamics: lems.model.dynamics.Dynamics
        """

        self.default_regime.merge(dynamics.default_regime)

        if not self.current_regime:
            self.current_regime = dynamics.current_regime

        for rn in dynamics.regimes:
            if rn in self.regimes:
                self.regimes[rn].merge(dynamics.regimes[rn])
            else:
                self.regimes[rn] = dynamics.regimes[rn]

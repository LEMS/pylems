"""
Behavioral dynamics of component types.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError

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
        """ Name of the variable for which the time derivative is being specified.
        @type: str """

        self.value = value
        """ Derivative expression.
        @type: str """
        
class Action(LEMSBase):
    """
    Base class for event handler actions.
    """

    pass

class StateAssignment(Action):
    """
    State assignment specification.
    """

    def __init__(self, variable, value):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        Action.__init__(self)

        self.variable = variable
        """ Name of the variable for which the time derivative is being specified.
        @type: str """

        self.value = value
        """ Derivative expression.
        @type: str """

class EventOut(Action):
    """
    Event transmission specification.
    """

    def __init__(self, port):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        
        Action.__init__(self)

        self.port = port
        """ Port on which the event comes in.
        @type: str """
        
class Transition(Action):
    """
    Regime transition specification.
    """

    def __init__(self, regime):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        
        Action.__init__(self)

        self.regime = regime
        """ Regime to transition to.
        @type: str """

class EventHandler(LEMSBase):
    """
    Base class for event handlers.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.actions = list()
        """ List of actions to be performed in response to this event.
        @type: list(lems.model.dynamics.Action) """

    def add_action(self, action):
        """
        Adds an action to this event handler.

        @param action: Action to be added.
        @type: action: lems.model.dynamics.Action
        """

        self.actions.append(action)

    def add(self, child):
        """
        Adds a typed child object to the event handler.

        @param child: Child object to be added.
        """

        if isinstance(child, Action):
            self.add_action(child)
        else:
            raise ModelError('Unsupported child element')
        
class OnStart(EventHandler):
    """
    Specification for event handler called upon initialization of the component.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        EventHandler.__init__(self)

class OnCondition(EventHandler):
    """
    Specification for event handler called upon satisfying a given condition.
    """

    def __init__(self, test):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        
        EventHandler.__init__(self)

        self.test = test
        """ Condition to be tested for.
        @type: str """

class OnEvent(EventHandler):
    """
    Specification for event handler called upon receiving en event sent by another component.
    """

    def __init__(self, port):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        
        EventHandler.__init__(self)

        self.port = port
        """ Port on which the event comes in.
        @type: str """

class OnEntry(EventHandler):
    """
    Specification for event handler called upon entry into a new behavior regime.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        EventHandler.__init__(self)

class KineticScheme(LEMSBase):
    """
    Kinetic scheme specifications.
    """

    def __init__(self, name, nodes, state_variable, 
                 edges, edge_source, edge_target,
                 forward_rate, reverse_rate):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """

        self.name = name
        """ Name of the kinetic scheme.
        @type: str """

        self.nodes = nodes
        """ Nodes to be used for the kinetic scheme.
        @type: str """

        self.state_variable = state_variable
        """ State variable updated by the kinetic scheme.
        @type: str """

        self.edges = edges
        """ Edges to be used for the kinetic scheme.
        @type: str """

        self.edge_source = edge_source
        """ Attribute that defines the source of the transition.
        @type: str """

        self.edge_target = edge_target
        """ Attribute that defines the target of the transition.
        @type: str """

        self.forward_rate = forward_rate
        """ Name of the forward rate exposure.
        @type: str """

        self.reverse_rate = reverse_rate
        """ Name of the reverse rate exposure.
        @type: str """

class Behavioral(LEMSBase):
    """
    Store dynamic behavioral attrubutes.
    """

    def __init__(self):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
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

        self.event_handlers = list()
        """ List of event handlers in this behaviour regime.
        @type: list(lems.model.dynamics.EventHandler) """

        self.kinetic_schemes = Map()
        """ Map of kinetic schemes in this behavior regime.
        @type: dict(str -> lems.model.dynamics.KineticScheme) """

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

    def add_event_handler(self, eh):
        """
        Adds an event handler to this behavior regime.

        @param eh: Event handler.
        @type eh: lems.model.dynamics.EventHandler
        """

        self.event_handlers.append(eh)

    def add_kinetic_scheme(self, ks):
        """
        Adds a kinetic scheme to this behavior regime.

        @param td: Kinetic scheme.
        @type td: lems.model.dynamics.KineticScheme
        """

        self.kinetic_schemes[ks.name] = ks

    def add(self, child):
        """
        Adds a typed child object to the behavioral object.

        @param child: Child object to be added.
        """

        if isinstance(child, StateVariable):
            self.add_state_variable(child)
        elif isinstance(child, DerivedVariable):
            self.add_derived_variable(child)
        elif isinstance(child, TimeDerivative):
            self.add_time_derivative(child)
        elif isinstance(child, EventHandler):
            self.add_event_handler(child)
        elif isinstance(child, KineticScheme):
            self.add_kinetic_scheme(child)
        else:
            raise ModelError('Unsupported child element')
        
class Regime(Behavioral):
    """
    Stores a single behavioral regime for a component type.
    """

    def __init__(self, name, initial = False):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """

        Behavioral.__init__(self)
        
        self.name = name
        """ Name of this behavior regime.
        @type: str """

        self.initial = initial
        """ Initial behavior regime.
        @type: bool """
        
class Dynamics(Behavioral):
    """
    Stores behavioral dynamics specification for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        Behavioral.__init__(self)

        self.regimes = Map()
        """ Map of behavior regimes.
        @type: Map(str -> lems.model.dynamics.Regime) """

    def add_regime(self, regime):
        """
        Adds a behavior regime to this dynamics object.

        @param regime: Behavior regime to be added.
        @type regime: lems.model.dynamics.Regime """

        self.regimes[regime.name] = regime

    def add(self, child):
        """
        Adds a typed child object to the dynamics object.

        @param child: Child object to be added.
        """

        if isinstance(child, Regime):
            self.add_regime(child)
        else:
            Behavioural.add(self, child)
        

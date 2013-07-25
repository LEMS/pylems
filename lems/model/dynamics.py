"""
Behavioral dynamics of component types.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError,ParseError
from lems.parser.expr import ExprParser

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

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<StateVariable name="{0}" dimension = "{1}"'.format(self.name, self.dimension) +\
          (' exposure="{0}"'.format(self.exposure) if self.exposure else '') +\
          '/>'

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

        self.expression_tree = None
        """ Parse tree for the time derivative expression.
        @type: lems.parser.expr.ExprNode """

        if self.value != None:
            try:
                self.expression_tree = ExprParser(self.value).parse()
            except:
                raise ParseError("Parse error when parsing value expression "
                                 "'{0}' for derived variable {1}",
                                 self.value, self.name)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<DerivedVariable name="{0}"'.format(self.name) +\
          (' dimension="{0}"'.format(self.dimension) if self.dimension else '') +\
          (' exposure="{0}"'.format(self.exposure) if self.exposure else '') +\
          (' select="{0}"'.format(self.select) if self.select else '') +\
          (' value="{0}"'.format(self.value) if self.value else '') +\
          (' reduce="{0}"'.format(self.reduce) if self.reduce else '') +\
          (' required="{0}"'.format(self.required) if self.required else '') +\
          '/>'

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

        self.expression_tree = None
        """ Parse tree for the time derivative expression.
        @type: lems.parser.expr.ExprNode """
        
        try:
            self.expression_tree = ExprParser(value).parse()
        except:
            raise ParseError("Parse error when parsing value expression "
                             "'{0}' for state variable {1}",
                             self.value, self.variable)
        
    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<TimeDerivative variable="{0}" value="{1}"/>'.format(self.variable, self.value)

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

        self.expression_tree = None
        """ Parse tree for the time derivative expression.
        @type: lems.parser.expr.ExprNode """

        try:
            self.expression_tree = ExprParser(value).parse()
        except:
            raise ParseError("Parse error when parsing state assignment "
                             "value expression "
                             "'{0}' for state variable {1}",
                             self.value, self.variable)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<StateAssignment variable="{0}" value="{1}"/>'.format(self.variable, self.value)


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
        
    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<EventOut port="{0}"/>'.format(self.port)

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

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<Transition regime="{0}"/>'.format(self.regime)

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

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        xmlstr = '<OnStart'

        chxmlstr = ''

        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnStart>'
        else:
            xmlstr += '/>'

        return xmlstr

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

        try:
            self.expression_tree = ExprParser(test).parse()
        except:
            raise ParseError("Parse error when parsing OnCondition test '{0}'",
                             test)
        
    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        xmlstr = '<OnCondition test="{0}"'.format(self.test)

        chxmlstr = ''

        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnCondition>'
        else:
            xmlstr += '/>'

        return xmlstr

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

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        xmlstr = '<OnEvent port="{0}"'.format(self.port)

        chxmlstr = ''

        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnEvent>'
        else:
            xmlstr += '/>'

        return xmlstr

class OnEntry(EventHandler):
    """
    Specification for event handler called upon entry into a new behavior regime.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        EventHandler.__init__(self)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        xmlstr = '<OnEntry'

        chxmlstr = ''

        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnEntry>'
        else:
            xmlstr += '/>'

        return xmlstr

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

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return ('<KineticScheme '
                'name="{0}" '
                'nodes="{1}" '
                'edges="{2}" '
                'stateVariable="{3}" '
                'edgeSource="{4}" '
                'edgeTarget="{5}" '
                'forwardRate="{6}" '
                'reverseRate="{7}"/>').format(self.name,
                                              self.nodes,
                                              self.edges,
                                              self.state_variable,
                                              self.edge_source,
                                              self.edge_target,
                                              self.forward_rate,
                                              self.reverse_rate)

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
        
    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        if isinstance(self, Dynamics):
            xmlstr = '<Dynamics'
        else:
            xmlstr = '<Regime name="{0}"'.format(self.name) +\
              (' initial="true"' if self.initial else '')

        chxmlstr = ''

        for state_variable in self.state_variables:
            chxmlstr += state_variable.toxml()

        for derived_variable in self.derived_variables:
            chxmlstr += derived_variable.toxml()

        for time_derivative in self.time_derivatives:
            chxmlstr += time_derivative.toxml()

        for event_handler in self.event_handlers:
            chxmlstr += event_handler.toxml()

        for kinetic_scheme in self.kinetic_schemes:
            chxmlstr += kinetic_scheme.toxml()

        if isinstance(self, Dynamics):
            for regime in self.regimes:
                chxmlstr += regime.toxml()
                
        if chxmlstr:
            xmlstr += '>' + chxmlstr + ('</Dynamics>' if isinstance(self, Dynamics) else '</Regime>')
        else:
            xmlstr += '/>'

        return xmlstr
                
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
        

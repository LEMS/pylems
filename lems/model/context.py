"""
Context storage

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.errors import ModelError
from lems.model.dynamics import Dynamics
from lems.model.structure import Structure
from lems.model.simulation import Simulation
from lems.model.parameter import Parameter

from lems.base.util import merge_dict, merge_ordered_dict

class Context(LEMSBase):
    """
    Stores the current type and variable context.
    """

    GLOBAL = 0
    """ Global context """

    COMPONENT_TYPE = 1
    """ Component type context """

    COMPONENT = 2
    """ Component context """

    def __init__(self, name, parent = None, context_type = GLOBAL):
        """
        Constructor
        """

        self.name = name
        """ Name identifying this context.
        @type: string """

        self.parent = parent
        """ Reference to parent context.
        @type: lems.model.context.Context """

        self.context_type = context_type
        """ Context type (Global, component type or component)
        @type: enum(Context.GLOBAL, Context.COMPONENT_TYPE or
        Context.COMPONENT_TYPE) """

        self.component_types = {}
        """ Dictionary of component types defined in this conext.
        @type: dict(string -> lems.model.component.ComponentType) """

        self.components = {}
        """ Dictionary of components defined in this context.
        @type: dict(string -> lems.model.component.Component) """

        self.components_ordering = []
        """ Ordering for components defined in this context.
        @type: list(string) """

        self.component_refs = {}
        """ Dictionary of component references defined in this context.
        @type: dict(string -> string) """

        self.child_defs = {}
        """ Dictionary of single-instance child object definitions in this
        context.
        @type: dict(string -> string) """

        self.children_defs = {}
        """ Dictionary of multi-instance child objects definitions in this
        context.
        @type: dict(string -> string) """

        self.children = []
        """ List of child objects defined in this context.
        @type: list(lems.model.component.Component) """

        self.parameters = {}
        """ Dictionary of references to parameters defined in this context.
        @type: dict(string -> lems.model.parameter.Parameter) """

        self.derived_parameters = {}
        """ Dictionary of references to derived parameters defined in
        this context.
        @type: dict(string -> lems.model.parameter.DerivedParameter) """

        self.dynamics_profiles = {}
        """ Stores the various dynamics profiles of the current object.
        @type: dict(string -> lems.model.dynamics.Dynamics) """

        self.selected_dynamics_profile = None
        """ Name of the dynamics dynamics profile.
        @type: lems.model.dynamics.Dynamics """

        self.exposures = set()
        """ List of names of exposed variables.
        @type: set(string) """

        self.requirements = {}
        """ List of names of required variables.
        @type: dict(string -> string) """

        self.texts = {}
        """ Dictionary of text parameters.
        @type: dict(string -> string) """

        self.paths = {}
        """ Dictionary of path parameters.
        @type: dict(string -> string) """

        self.links = {}
        """ Dictionary of link parameters.
        @type: dict(string -> string) """

        self.event_in_ports = set()
        """ List of incoming event port names.
        @type: set(string) """

        self.event_out_ports = set()
        """ List of outgoing event port names.
        @type: set(string) """

        self.structure = Structure()
        """ Structure object detailing structural aspects of this component.
        @type: lems.model.structure.Structure """

        self.simulation = Simulation()
        """ Simulation object detailing simulation-related aspects of this component.
        @type: lems.model.simulation.Simulation """

        self.attachments = dict()
        """ Dictionary of attachments in this component-type
        @type: dict(string -> string """


    def add_component_type(self, component_type):
        """
        Adds a component type to the list of defined component types in the
        current context.

        @param component_type: Component type to be added
        @type component_type: lems.model.component.ComponentType

        @raise ModelError: Raised when the component type is already defined
        in the current context.
        """

        if component_type.name in self.component_types:
            raise ModelError("Duplicate component type '{0}'".format(\
                component_type.name))

        self.component_types[component_type.name] = component_type

    def add_component(self, component):
        """
        Adds a component to the list of defined components in the current
        context.

        @param component: Component to be added
        @type component: lems.model.component.ComponentType

        @raise ModelError: Raised when the component is already defined in the
        current context.
        """

        if component.id in self.components:
            raise ModelError("Duplicate component '{0}'".format(component.id))

        self.components[component.id] = component
        self.components_ordering.append(component.id)

    def add_component_ref(self, name, type):
        """
        Adds a component reference to the list of defined component
        references in the current context.

        @param name: Name of the component reference.
        @type name: string

        @param type: Type of the component reference.
        @type type: string

        @raise ModelError: Raised when the component reference is already
        defined in the current context.
        """

        if name in self.component_refs:
            raise ModelError("Duplicate component reference '{0}'".format(\
                name))

        self.component_refs[name] = type

    def add_child(self, child):
        """
        Adds a child object to the list of child objects in the
        current context.

        @param child: Child object.
        @type child: lems.model.component.Component

        @raise ModelError: Raised when a child is instantiated inside a
        component type.
        """

        if self.context_type == Context.COMPONENT_TYPE:
            raise ModelError("Child definition '{0}' not permitted in "
                             "component type definition '{1}'".format(\
                                 child.id, self.name))

        self.children.append(child)


    def add_child_def(self, name, type):
        """
        Adds a child object definition to the list of single-instance child
        object definitions in the current context.

        @param name: Name of the child object.
        @type name: string

        @param type: Type of the child object.
        @type type: string

        @raise ModelError: Raised when the definition is already in the
        current context.
        """

        if name in self.child_defs:
            raise ModelError("Duplicate child definition '{0}'".format(name))

        self.child_defs[name] = type

    def add_children_def(self, name, type):
        """
        Adds a child object definition to the list of multi-instance child
        object definitions in the current context.

        @param name: Name of the child object.
        @type name: string

        @param type: Type of the child object.
        @type type: string

        @raise ModelError: Raised when the definition is already in the
        current context.
        """

        if name in self.children_defs:
            raise ModelError("Duplicate children definition '{0}'".format(\
                name))

        self.children_defs[name] = type

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of defined parameters in the current
        context.

        @param parameter: Parameter to be added
        @type parameter: lems.model.parameter.Parameter

        @raise ModelError: Raised when the parameter is already defined in the
        current context.
        """

        if parameter.name in self.parameters:
            raise ModelError("Duplicate parameter '{0}'".format(\
                parameter.name))

        self.parameters[parameter.name] = parameter

    def add_derived_parameter(self, parameter):
        """
        Adds a parameter to the list of defined parameters in the current
        context.

        @param parameter: Parameter to be added
        @type parameter: lems.model.parameter.DerivedParameter

        @raise ModelError: Raised when the parameter is already defined in the
        current context.
        """

        if parameter.name in self.derived_parameters:
            raise ModelError("Duplicate derived parameter '{0}'".format(
                parameter.name))

        self.derived_parameters[parameter.name] = parameter

    def add_dynamics_profile(self, name):
        """
        Adds a dynamics profile to the current context.

        @param name: Name of the dynamics profile.
        @type name: string
        """

        if name in self.dynamics_profiles:
            raise ModelError("Duplicate dynamics profile '{0}'".format(name))

        self.dynamics_profiles[name] = Dynamics(name)
        self.select_dynamics_profile(name)

    def select_dynamics_profile(self, name):
        """
        Selects a dynamics profile by name.

        @param name: Name of the dynamics profile.
        @type name: string

        @raise ModelError: Raised when the specified dynamics profile is
        undefined in the current context.
        """

        if name not in self.dynamics_profiles:
            raise ModelError("Unknown dynamics profile '{0}'".format(name))

        self.selected_dynamics_profile = self.dynamics_profiles[name]

    def add_exposure(self, name):
        """
        Adds a state variable exposure to the current context.

        @param name: Name of the state variable being exposed.
        @type name: string

        @raise ModelError: Raised when the exposure name already exists
        in the current context.

        @raise ModelError: Raised when the exposure name is not
        being defined in the context of a component type.
        """
        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError("Exposure names can only be defined in "
                             "a component type - '{0}'".format(name))

        if name in self.exposures:
            raise ModelError("Duplicate exposure name '{0}'".format(name))

        self.exposures.add(name)

    def add_requirement(self, name, dimension):
        """
        Adds a parameter requirement to the current context.

        @param name: Name of the variable being required.
        @type name: string

        @param dimension: Dimension of the variable being required.
        @type dimension: string

        @raise ModelError: Raised when the exposure name already exists
        in the current context.

        @raise ModelError: Raised when the exposure name is not
        being defined in the context of a component type.
        """
        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError("Requirements can only be defined in "
                             "a component type - '{0}'".format(name))

        if name in self.requirements:
            raise ModelError("Duplicate requirement name '{0}'".format(name))

        self.requirements[name] = dimension

    def add_text_var(self, name, value = None):
        """
        Adds a text variable to the current context.

        @param name: Name of the text variable.
        @type name: string

        @param value: Value of the text variable.
        @type value: string

        @raise ModelError: Raised when the text variable already exists
        in the current context.
        """

        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError("Text variables can only be defined in "
                             "a component type - '{0}'".format(name))

        if name in self.texts:
            raise ModelError("Duplicate text variable '{0}'".format(name))

        self.texts[name] = value

    def add_path_var(self, name, value = None):
        """
        Adds a path variable to the current context.

        @param name: Name of the path variable.
        @type name: string

        @param value: Value of the path variable.
        @type value: string

        @raise ModelError: Raised when the path variable already exists
        in the current context.
        """

        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError("Path variables can only be defined in "
                             "a component type - '{0}'".format(name))

        if name in self.paths:
            raise ModelError("Duplicate path variable '{0}'".format(name))

        self.paths[name] = value

    def add_link_var(self, name, type = None):
        """
        Adds a link variable to the current context.

        @param name: Name of the link variable.
        @type name: string

        @param type: Type of the link variable.
        @type type: string

        @raise ModelError: Raised when the link variable already exists
        in the current context.
        """

        if self.context_type != Context.COMPONENT_TYPE:
            raise ModelError("Link variables can only be defined in "
                             "a component type - '{0}'".format(name))

        if name in self.links:
            raise ModelError("Duplicate link variable '{0}'".format(name))

        self.links[name] = type

    def add_event_port(self, name, direction):
        """
        Adds an event port to the list of event ports handled by this
        component or component type.

        @param name: Name of the event port.
        @type name: string

        @param direction: Event direction ('in' or 'out').
        @type direction: string

        @raise ModelError: Raised when the definition is already in the
        current context.
        """

        if name in self.event_in_ports or name in self.event_out_ports:
            raise ModelError("Duplicate event '{0}'".format(name))

        if direction == 'in':
            self.event_in_ports.add(name)
        else:
            self.event_out_ports.add(name)

    def add_attachment(self, name, type_):
        """
        Adds an attachment to this component-type.

        @param name: Name of the attachment.
        @type name: string

        @param type_: Type of the attachment.
        @type type_: string

        @raise ModelError: Raised when the attachment is already in the
        current context.
        """

        if name in self.attachments:
            raise ModelError("Duplicate attachment '{0}'".format(name))

        self.attachments[type_] = name


    def lookup_component_type(self, name):
        """
        Searches the current context and parent contexts for a component type
        with the given name.

        @param name: Name of the component type.
        @type name: string

        @return: Resolved component type object, or None on failure.
        @rtype: lems.model.component.ComponentType
        """

        if name in self.component_types:
            return self.component_types[name]
        elif self.parent:
            return self.parent.lookup_component_type(name)
        else:
            return None

    def lookup_component(self, name):
        """
        Searches the current context and parent contexts for a component
        with the given name.

        @param name: Name of the component.
        @type name: string

        @return: Resolved component object, or None on failure.
        @rtype: lems.model.component.Component
        """

        if name in self.components:
            return self.components[name]
        elif self.parent:
            return self.parent.lookup_component(name)
        else:
            return None

    def lookup_component_ref(self, name):
        """
        Searches the current context and parent contexts for a component
        with the given name.

        @param name: Name of the component.
        @type name: string

        @return: Resolved component object, or None on failure.
        @rtype: lems.model.component.Component
        """

        if name in self.component_refs:
            cname = self.component_refs[name]
            return self.lookup_component(cname)
        elif self.parent:
            return self.parent.lookup_component_ref(name)
        else:
            return None

    def lookup_child(self, name):
        """
        Searches the current context and parent contexts for a child
        with the given name.

        @param name: Name of the component.
        @type name: string

        @return: Component type for the child, or None on failure.
        @rtype: string
        """

        if name in self.child_defs:
            return self.child_defs[name]
        elif self.parent:
            return self.parent.lookup_child(name)
        else:
            return None


    def lookup_parameter(self, parameter_name):
        """
        Looks up a parameter by name within this context.

        @param parameter_name: Name of the parameter.
        @type parameter_name: string

        @return: Corresponding Parameter object or None if not found.
        @rtype: lems.model.parameter.Parameter
        """

        if parameter_name in self.parameters:
            return self.parameters[parameter_name]
        else:
            return None

    def lookup_path_parameter(self, path_name):
        """
        Looks up a path parameter.

        @param path_name: Name of the path parameter.
        @type path_name: string

        @return: Value of the path parameter
        @rtype: string
        """

        path_param = self.lookup_parameter(path_name)
        if path_param == None or path_param.dimension != '__path__':
            return None
        else:
            return path_param.value

    def lookup_text_parameter(self, text_name):
        """
        Looks up a text parameter.

        @param text_name: Name of the text parameter.
        @type text_name: string

        @return: Value of the text parameter
        @rtype: string
        """

        text_param = self.lookup_parameter(text_name)
        if text_param == None or text_param.dimension != '__text__':
            return None
        else:
            return text_param.value

    def merge(self, other, model):
        """
        Merge another context (base or type context) into this one.

        @param other: Base or type context to be merged in
        @type other: lems.model.context.Context
        """

        merge_dict(self.component_types, other.component_types)
        merge_ordered_dict(self.components, self.components_ordering,
                           other.components, other.components_ordering)
        merge_dict(self.component_refs, other.component_refs)
        merge_dict(self.child_defs, other.child_defs)
        merge_dict(self.children_defs, other.children_defs)

        for child in other.children:
            self.children.append(child)

        if (self.context_type == other.context_type and
            self.context_type in [Context.COMPONENT_TYPE, Context.COMPONENT]):
            self.merge_extended_parameters(other)
        elif (self.context_type == Context.COMPONENT and
              other.context_type == Context.COMPONENT_TYPE):
            self.merge_component_parameters_from_component_type(other, model)

        merge_dict(self.dynamics_profiles, other.dynamics_profiles)
        if not self.selected_dynamics_profile:
            self.selected_dynamics_profile = other.selected_dynamics_profile

        self.exposures |= other.exposures

        merge_dict(self.requirements, other.requirements)
        merge_dict(self.texts, other.texts)
        merge_dict(self.paths, other.paths)
        merge_dict(self.links, other.links)

        self.event_in_ports |= other.event_in_ports
        self.event_out_ports |= other.event_out_ports

        if (self.context_type == Context.COMPONENT and
            other.context_type == Context.COMPONENT_TYPE):
            self.structure.merge_from_type(other.structure, self)
        else:
            self.structure.merge(other.structure)

        self.simulation.merge(other.simulation)

        merge_dict(self.attachments, other.attachments)

    def merge_extended_parameters(self, other):
        """
        Merge parameters from a base component or component type
        into this one

        @param other: Base or type context to be merged in
        @type other: lems.model.context.Context
        """

        for pn in other.parameters:
            if pn in self.parameters:
                pt = self.parameters[pn]

                if pt.dimension == '__dimension_inherited__':
                    pb = other.parameters[pn]
                    self.parameters[pn] = Parameter(pt.name,
                                                    pb.dimension,
                                                    pt.fixed,
                                                    pt.value)
                else:
                    raise ModelError(('Parameter {0} in {1} is redefined ' +
                                      'in {2}').format(pn, other.name,
                                                       self.name))
            else:
                self.parameters[pn] = other.parameters[pn].copy()

    def merge_component_parameters_from_component_type(self, type_context, model):
        """
        Merge component parameters from a component type
        definition.

        @param type_context: Type context to be merged in
        @type type_context: lems.model.context.Context
        """


        for pn in type_context.parameters:
            pt = type_context.parameters[pn]
            if pn in self.parameters:
                pc = self.parameters[pn]

                if pc.value:
                    value = pc.value
                else:
                    value = pt.value

                if pc.dimension == '__dimension_inherited__':
                    if pt.fixed:
                        np = Parameter(pn, pt.dimension, pt.fixed, value)
                    else:
                        np = Parameter(pn, pt.dimension, pc.fixed, value)
                    self.parameters[pn] = np
            else:
                self.parameters[pn] = pt.copy()

            model.resolve_parameter_value(self.parameters[pn],
                                          self)

        for pn in self.parameters:
            pc = self.parameters[pn]
            if pc.dimension == '__dimension_inherited__':
                if pn in type_context.texts:
                    pc.dimension = '__text__'
                    self.texts[pn] = type_context.texts[pn]
                elif pn in type_context.paths:
                    pc.dimension = '__path__'
                    self.paths[pn] = type_context.paths[pn]
                elif pn in type_context.links:
                    pc.dimension = '__link__'
                    self.links[pn] = type_context.links[pn]
                elif pn in type_context.component_refs:
                    pc.dimension = '__component_ref__'
                    cf = type_context.component_refs[pn]
                    self.component_refs[pn] = pc.value


class Contextual(LEMSBase):
    """
    Base class for objects that need to store their own context.
    """

    def __init__(self, name, parent = None, context_type = Context.GLOBAL):
        """
        Constructor.
        """

        self.context = Context(name, parent, context_type)
        """ Context object.
        @type: lems.model.context.Context """

    def add_component_type(self, component_type):
        """
        Adds a component type to the list of defined component types in the
        current context.

        @param component_type: Component type to be added
        @type component_type: lems.model.component.ComponentType
        """

        self.context.add_component_type(component_type)

    def add_component(self, component):
        """
        Adds a component to the list of defined components in the current
        context.

        @param component: Component to be added
        @type component: lems.model.component.Component
        """

        self.context.add_component(component)

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of defined parameters in the current
        context.

        @param parameter: Parameter to be added
        @type parameter: lems.model.parameter.Parameter
        """

        self.context.add_parameter(parameter)

    def lookup_parameter(self, parameter_name):
        """
        Lookup a parameter in this context by name.

        @param parameter_name: Name of the parameter.
        @type parameter_name: string

        @return: Corresponding Parameter object or None if not found.
        @rtype: lems.model.parameter.Parameter
        """

        return self.context.lookup_parameter(parameter_name)

"""
Component structure storage.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.errors import ModelError

from lems.base.util import merge_dict

class Structure(LEMSBase):
    """
    Stores the structural characteristics for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.event_connections = []
        """ List of event connections b/w components. The from and to
        attributes are described as component:port
        @type: list(lems.base.structure.EventConnection) """

        self.single_child_defs = []
        """ List of single-child instantiation definitions.
        @type: list(string) """

        self.multi_child_defs = {}
        """ List of multi-child instantiation definitions.
        @type: dict(string -> string) """

        self.foreach = []
        """ List of foreach declarations.
        @type: lems.model.structure.ForEach """

        self.foreach_mappings = {}
        """ Accumulated name->target mappings for nested ForEach constructs.
        @type: dict(string -> string) """

        self.with_mappings = {}
        """ With mappings for With specifications.
        @type: dict(string -> string) """

    def add_event_connection(self, source_path, target_path,
                 source_port = '', target_port = '',
                 receiver = '', receiver_container = ''):
        """
        Adds an event connection to the structure.

        @param source_path: Name (or mapped name) of the path variable
        pointing to the source component.
        @type source_path: string

        @param target_path: Name (or mapped name) of the path variable
        pointing to the target component.
        @type target_path: string

        @param source_port: Port name for the source component. Can be left empty if
        there is only one output port defined in the component.
        @type source_port: string

        @param target_port: Port name for the target component. Can be left empty if
        there is only one input port defined in the component.
        @type target_port: string

        @param receiver: Name of a component reference pointing to a component
        acting as a receiver for the event.
        @type receiver: string

        @param receiver_container: TODO
        @type receiver_container: string
        """

        self.event_connections.append(EventConnection(source_path, target_path,
                                                      source_port, target_port,
                                                      receiver, receiver_container))

    def add_single_child_def(self, component):
        """
        Adds a single-child instantiation definition to this component type.

        @param component: Name of component reference used as template for
        instantiating the child.
        @type component: string
        """

        if component in self.single_child_defs:
            raise ModelError("Duplicate child instantiation = '{0}'".format(\
                component))
        self.single_child_defs.append(component)

    def add_multi_child_def(self, component, number):
        """
        Adds a single-child instantiation definition to this component type.

        @param component: Name of component reference used as template for
        instantiating the child.
        @type component: string

        @param number: Number of objects to be instantiated.
        @type number: string
        """

        if component in self.single_child_defs:
            raise ModelError("Duplicate child multiinstantiation = "
                             "'{0}'".format(component))

        if self.multi_child_defs != {}:
            raise ModelError("Only one multi-instantiation is permitted "
                             "per component type - '{0}'".format(component))

        self.multi_child_defs[component] = number

    def add_foreach(self, name, target):
        """
        Adds a foreach structure nesting.

        @param name: Name used to refer to the enumerated target references.
        @type name: string

        @param target: Path to thetarget references.
        @type target: string
        """

        foreach = ForEach(name, target)

        for n in self.foreach_mappings:
            t = self.foreach_mappings[n]
            foreach.foreach_mappings[n] = t

        foreach.foreach_mappings[name] = target

        self.foreach.append(foreach)
        return foreach

    def add_with(self, name, target):
        """
        Adds a with structure nesting.

        @param name: Name used to refer to the enumerated target references.
        @type name: string

        @param target: Path to thetarget references.
        @type target: string
        """

        if name in self.with_mappings:
            raise ModelError("Duplicate <With> specification for "
                             "'{0}'".format(component))

        self.with_mappings[name] = target

    def merge(self, other):
        """
        Merge another set of structural characteristics
        into this one.

        @param other: structural characteristics
        @type other: lems.model.structure.Structure
        """

        self.event_connections += other.event_connections
        self.single_child_defs += other.single_child_defs

        merge_dict(self.multi_child_defs, other.multi_child_defs)

        self.foreach += other.foreach
        merge_dict(self.foreach_mappings, other.foreach_mappings)
        merge_dict(self.with_mappings, other.with_mappings)


    def merge_from_type(self, other, context):
        """
        Merge another set of structural characteristics
        into this one.

        @param other: Structural characteristics
        @type other: lems.model.structure.Structure

        @param context: Context of the component
        @type context: lems.model.context.Context
        """

        self.event_connections += other.event_connections

        for c in other.single_child_defs:
            if c in context.component_refs:
                self.add_single_child_def(c)
            else:
                raise ModelError("Trying to multi-instantiate from an "
                                 "invalid component reference '{0}'".format(\
                        c))

        for c in other.multi_child_defs:
            n = other.multi_child_defs[c]
            if c in context.component_refs:
                component = context.component_refs[c]
                if n in context.parameters:
                    number = int(context.parameters[n].numeric_value)
                    self.add_multi_child_def(component, number)
                else:
                    raise ModelError("Trying to multi-instantiate using an "
                                     "invalid number parameter '{0}'".\
                                     format(n))
            else:
                raise ModelError("Trying to multi-instantiate from an "
                                 "invalid component reference '{0}'".format(\
                                     c))

        self.foreach += other.foreach
        merge_dict(self.foreach_mappings, other.foreach_mappings)
        merge_dict(self.with_mappings, other.with_mappings)


class ForEach(Structure):
    """
    Stores a <ForEach> statement and containing structures.
    """

    def __init__(self, name, target):
        """
        Constructor.
        """

        Structure.__init__(self)

        self.name = name
        """ Name used to refer to the enumerated target instances.
        @type: string """

        self.target = target
        """ Path to the target instances.
        @type: string """

class EventConnection(LEMSBase):
    """
    Stores specification of an event connection.
    """

    def __init__(self, source_path, target_path,
                 source_port, target_port,
                 receiver, receiver_container):
        """
        Constructor.
        """

        self.source_path = source_path
        """ Name (or mapped name) of the path variable
        pointing to the source component.
        @type: string """

        self.target_path = target_path
        """ Name (or mapped name) of the path variable
        pointing to the target component.
        @type: string """

        self.source_port = source_port
        """ Port name for the source component. Can be left empty if
        there is only one output port defined in the component.
        @type: string """

        self. target_port = target_port
        """ Port name for the target component. Can be left empty if
        there is only one input port defined in the component.
        @type: string """

        self.receiver = receiver
        """ Name of a component reference pointing to a component
        acting as a receiver for the event.
        @type: string """

        self.receiver_container = receiver_container
        """ TODO
        @type: string """

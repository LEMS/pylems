"""
Parameter, ComponentType and Component class definitions.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError

from lems.model.dynamics import Dynamics
from lems.model.structure import Structure
from lems.model.simulation import Simulation

class Parameter(LEMSBase):
    """
    Stores a parameter declaration.
    """
    
    def __init__(self, name, dimension, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the parameter.
        @type: str """
         
        self.dimension = dimension
        """ Physical dimension of the parameter.
        @type: str """

        self.fixed = False
        """ Whether the parameter has been fixed or not.
        @type: bool """
        
        self.fixed_value = None
        """ Value if fixed.
        @type: str """

        self.description = description
        """ Description of this parameter.
        @type: str """

class Fixed(Parameter):
    """
    Stores a fixed parameter specification.
    """
    
    def __init__(self, parameter, value, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """

        Parameter.__init__(self, parameter, '__dimension_inherited__', description)
        
        self.fixed = True
        self.fixed_value = value

class Constant(LEMSBase):
    """
    Stores a constant specification.
    """
    
    def __init__(self, name, value, dimension = None, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the constant.
        @type: str """

        self.value = value
        """ Value of the constant.
        @type: str """

        self.dimension = dimension
        """ Physical dimensions of the constant.
        @type: str """

        self.description = description
        """ Description of the constant.
        @type: str """

        self.numeric_value = 0
        """ Numeric value of the constant.
        @type: float """

class Exposure(LEMSBase):
    """
    Stores a exposure specification.
    """

    def __init__(self, name, dimension, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the exposure.
        @type: str """
         
        self.dimension = dimension
        """ Physical dimension of the exposure.
        @type: str """

        self.description = description
        """ Description of this exposure.
        @type: str """

class Requirement(LEMSBase):
    """
    Stores a requirement specification.
    """

    def __init__(self, name, dimension):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the requirement.
        @type: str """
         
        self.dimension = dimension
        """ Physical dimension of the requirement.
        @type: str """

class Children:
    """
    Stores children specification.
    """
    
    def __init__(self, name, type_, multiple = False):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the children.
        @type: str """
         
        self.type = type_
        """ Component type of the children.
        @type: str """

        self.multiple = multiple
        """ Single child / multiple children.
        @type: bool """

class Text(LEMSBase):
    """
    Stores a text entry specification.
    """

    def __init__(self, name, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the text entry.
        @type: str """
         
        self.description = description
        """ Description of the text entry.
        @type: str """

class Link(LEMSBase):
    """
    Stores a link specification.
    """

    def __init__(self, name, type_, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the link entry.
        @type: str """

        self.type = type_
        """ Type of the link.
        @type: str """
         
        self.description = description
        """ Description of the link.
        @type: str """

class Path(LEMSBase):
    """
    Stores a path entry specification.
    """

    def __init__(self, name, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the path entry.
        @type: str """
         
        self.description = description
        """ Description of the path entry.
        @type: str """

class EventPort(LEMSBase):
    """
    Stores an event port specification.
    """

    def __init__(self, name, direction, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the event port.
        @type: str """

        self.direction = direction
        """ Direction - IN/OUT .
        @type: str """
         
        self.description = description
        """ Description of the event port.
        @type: str """

class ComponentReference(LEMSBase):
    """
    Stores a component reference.
    """

    def __init__(self, name, type_):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """

        self.name = name
        """ Name of the component reference.
        @type: str """

        self.type = type_
        """ Type of the component reference.
        @type: str """

class Attachments(LEMSBase):
    """
    Stores an attachment type specification.
    """

    def __init__(self, name, type_, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """

        self.name = name
        """ Name of the attachment collection.
        @type: str """

        self.type = type_
        """ Type of attachment.
        @type: str """

        self.description = description
        """ Description about the attachment.
        @type: str """

    
        
class ComponentType(LEMSBase):
    """
    Stores a component type declaration.
    """

    def __init__(self, name, description = '', extends = None):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the component type.
        @type: str """
         
        self.extends = extends
        """ Base component type.
        @type: str """

        self.description = description
        """ Description of this component type.
        @type: str """
        
        self.parameters = Map()
        """ Map of parameters in this component type.
        @type: Map(str -> lems.model.component.Parameter) """

        self.constants = Map()
        """ Map of constants in this component type.
        @type: Map(str -> lems.model.component.Constant) """

        self.exposures = Map()
        """ Map of exposures in this component type.
        @type: Map(str -> lems.model.component.Exposure) """

        self.requirements = Map()
        """ Map of requirements.
        @type: Map(str -> lems.model.component.Requirement) """

        self.children = Map()
        """ Map of children.
        @type: Map(str -> lems.model.component.Children """

        self.texts = Map()
        """ Map of text entries.
        @type: Map(str -> lems.model.component.Text """

        self.links = Map()
        """ Map of links.
        @type: Map(str -> lems.model.component.Link """

        self.paths = Map()
        """ Map of path entries.
        @type: Map(str -> lems.model.component.Path """

        self.event_ports = Map()
        """ Map of event ports.
        @type: Map(str -> lems.model.component.EventPort """

        self.component_references = Map()
        """ Map of component references.
        @type: Map(str -> lems.model.component.ComponentReference) """

        self.attachments = Map()
        """ Map of attachment type specifications.
        @type: Map(str -> lems.model.component.Attachments) """

        self.dynamics = Dynamics()
        """ Behavioural dynamics object.
        @type: lems.model.dynamics.Dynamics """

        self.structure = Structure()
        """ Structural properties object.
        @type: lems.model.structure.Structure """

        self.simulation = Simulation()
        """ Simulation attributes.
        @type: lems.model.simulation.Simulation """

    def add_parameter(self, parameter):
        """
        Adds a paramter to this component type.

        @param parameter: Parameter to be added.
        @type parameter: lems.model.component.Parameter
        """

        self.parameters[parameter.name] = parameter

    def add_constant(self, constant):
        """
        Adds a paramter to this component type.

        @param constant: Constant to be added.
        @type constant: lems.model.component.Constant
        """

        self.constants[constant.name] = constant

    def add_exposure(self, exposure):
        """
        Adds a exposure to this component type.

        @param exposure: Exposure to be added.
        @type exposure: lems.model.component.Exposure
        """

        self.exposures[exposure.name] = exposure

    def add_requirement(self, requirement):
        """
        Adds a requirement to this component type.

        @param requirement: Requirement to be added.
        @type requirement: lems.model.component.Requirement
        """

        self.requirements[requirement.name] = requirement

    def add_children(self, children):
        """
        Adds children to this component type.

        @param children: Children to be added.
        @type children: lems.model.component.Children
        """

        self.children[children.name] = children

    def add_text(self, text):
        """
        Adds a text to this component type.

        @param text: Text to be added.
        @type text: lems.model.component.Text
        """

        self.texts[text.name] = text

    def add_link(self, link):
        """
        Adds a link to this component type.

        @param link: Link to be added.
        @type link: lems.model.component.Link
        """

        self.links[link.name] = link

    def add_path(self, path):
        """
        Adds a path to this component type.

        @param path: Path to be added.
        @type path: lems.model.component.Path
        """

        self.paths[path.name] = path

    def add_event_port(self, event_port):
        """
        Adds a event port to this component type.

        @param event_port: Event port to be added.
        @type event_port: lems.model.component.EventPort
        """

        self.event_ports[event_port.name] = event_port

    def add_component_reference(self, component_reference):
        """
        Adds a component reference to this component type.

        @param component_reference: Component reference to be added.
        @type component_reference: lems.model.component.ComponentReference
        """

        self.component_references[component_reference.name] = component_reference

    def add_attachments(self, attachments):
        """
        Adds an attachments type specification to this component type.

        @param attachments: Attachments specification to be added.
        @type attachments: lems.model.component.Attachments
        """

        self.attachments[attachments.name] = attachments

    def add(self, child):
        """
        Adds a typed child object to the component type.

        @param child: Child object to be added.
        """

        if isinstance(child, Parameter):
            self.add_dimension(parameter)
        elif isinstance(child, Constant):
            self.add_constant(child)
        elif isinstance(child, Exposure):
            self.add_exposure(child)
        elif isinstance(child, Requirement):
            self.add_requirement(child)
        elif isinstance(child, children):
            self.add_children(child)
        elif isinstance(child, Text):
            self.add_text(child)
        elif isinstance(child, Link):
            self.add_link(child)
        elif isinstance(child, Path):
            self.add_path(child)
        elif isinstance(child, EventPort):
            self.add_event_port(child)
        elif isinstance(child, ComponentReference):
            self.add_component_reference(child)
        elif isinstance(child, Attachments):
            self.add_attachments(child)
        else:
            raise ModelError('Unsupported child element')

class Component(LEMSBase):
    """
    Stores a component instantiation.
    """

    def __init__(self, id_, type_):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """

        self.id = id_
        """ ID of the component.
        @type: str """

        self.type = type_
        """ Type of the component.
        @type: str """

        self.parameters = dict()
        """ Dictionary of parameter values.
        @type: str """

        self.children = list()
        """ List of child components.
        @type: list(lems.model.component.Component) """

    def set_parameter(self, parameter, value):
        """
        Set a parameter.

        @param parameter: Parameter to be set.
        @type parameter: str

        @param value: Value to be set to.
        @type value: str
        """

        self.parameters[parameter] = value

    def add_child(self, child):
        """
        Adds a child component.

        @param child: Child component to be added.
        @type child: lems.model.component.Component
        """

        self.children.append(child)

    def add(self, child):
        """
        Adds a typed child object to the component.

        @param child: Child object to be added.
        """

        if isinstance(child, Component):
            self.add_child(child)
        else:
            raise ModelError('Unsupported child element')
        

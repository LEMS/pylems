"""
Parameter, ComponentType and Component class definitions.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase
from lems.util import Map
from lems.model.dynamics import Dynamics

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
        @type: dict(str -> lems.model.component.Parameter) """

        self.constants = Map()
        """ Map of constants in this component type.
        @type: dict(str -> lems.model.component.Constant) """

        self.exposures = Map()
        """ Map of exposures in this component type.
        @type: dict(str -> lems.model.component.Exposure) """

        self.requirements = Map()
        """ Map of requirements.
        @type: dict(str -> lems.model.component.Requirement) """

        self.children = Map()
        """ Map of children.
        @type: dict(str -> lems.model.component.Children """

        self.texts = Map()
        """ Map of text entries.
        @type: dict(str -> lems.model.component.Text """

        self.links = Map()
        """ Map of links.
        @type: dict(str -> lems.model.component.Link """

        self.event_ports = Map()
        """ Map of event ports.
        @type: dict(str -> lems.model.component.EventPort """

        self.dynamics = Dynamics()
        """ Behavioural dynamics object.
        @type: lems.model.dynamics.Dynamics """

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
        Adds text to this component type.

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

    def add_event_port(self, event_port):
        """
        Adds a event port to this component type.

        @param event_port: Event port to be added.
        @type event_port: lems.model.component.EventPort
        """

        self.event_ports[event_port.name] = event_port

class Component(LEMSBase):
    """
    Stores a component instantiation.
    """

    def __init(self, description = ''):
        """
        Constructor.
        """

        self.description = description
        """ Description of this component.
        @type: str """

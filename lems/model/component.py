"""
Parameter, ComponentType and Component class definitions.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase
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
        
        self.parameters = dict()
        """ Dictionary of parameters in this component type.
        @type: dict(str -> lems.model.component.Parameter) """

        self.exposures = dict()
        """ Dictionary of exposures in this component type.
        @type: dict(str -> lems.model.component.Exposure) """

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

    def add_exposure(self, exposure):
        """
        Adds a paramter to this component type.

        @param exposure: Exposure to be added.
        @type exposure: lems.model.component.Exposure
        """

        self.exposures[exposure.name] = exposure

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

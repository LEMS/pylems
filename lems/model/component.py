"""
Parameter, ComponentType and Component class definitions.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

class Parameter(LEMSBase):
    """
    Stores a parameter declaration.
    """
    
    def __init__(self, name, dimension):
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

class ComponentType(LEMSBase):
    """
    Stores a component type declaration.
    """
    pass

class Component(LEMSBase):
    """
    Stores a component instantiation.
    """
    pass

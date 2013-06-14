"""
Dimension and Unit definitions in terms of the fundamental SI units.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

class Dimension(LEMSBase):
    """
    Stores a dimension in terms of the seven fundamental SI units.
    """
    
    def __init__(self, name, description = '', **params):
        """
        Constructor.

        @param name: Name of the dimension.
        @type name: str

        @param params: Key arguments specifying powers for each of the 
        seven fundamental SI dimensions.
        @type params: dict()
        """
        
        self.name = name
        """ Name of the dimension.
        @type: str """

        self.m = params['m'] if 'm' in params else 0
        """ Power for the mass dimension.
        @type: int """
        
        self.l = params['l'] if 'l' in params else 0
        """ Power for the length dimension.
        @type: int """
        
        self.t = params['t'] if 't' in params else 0
        """ Power for the time dimension.
        @type: int """
        
        self.i = params['i'] if 'i' in params else 0
        """ Power for the electic current dimension.
        @type: int """
        
        self.k = params['k'] if 'k' in params else 0
        """ Power for the temperature dimension.
        @type: int """
        
        self.n = params['n'] if 'n' in params else 0
        """ Power for the quantity dimension.
        @type: int """
        
        self.j = params['j'] if 'j' in params else 0
        """ Power for the luminous intensity dimension.
        @type: int """

        self.description = description
        """ Description of this dimension.
        @type: str """
        

class Unit(LEMSBase):
    """
    Stores a unit definition.
    """
    
    def __init__(self, name, symbol, dimension, power = 0, scale = 0, offset = 0, description = ''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        
        self.name = name
        """ Name of the unit.
        @type: str """
        
        self.symbol = symbol
        """ Symbol for the unit.
        @type: str """
        
        self.dimension = dimension
        """ Dimension for the unit.
        @type: str """
        
        self.power = power
        """ Scaling by power of 10.
        @type: int """
        
        self.scale = scale
        """ Scaling.
        @type: float """
        
        self.offset = offset
        """ Offset for non-zero units.
        @type: float """

        self.description = description
        """ Description of this unit.
        @type: str """
        

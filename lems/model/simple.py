"""
Types for basic LEMS objects (Dimensions, units, ...)

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import LEMSBase

class Dimension(LEMSBase):
    """
    Stores dimensionality of user-defined quantities in terms of the
    seven fundamental SI units
    """

    def __init__(self, name, *dims):
        """
        Constructor

        @param name: Name of the new dimension.
        @type name: string

        @param dims: Dimensionality for the seven fundamental SI units in
        the order - length, mass, time, electric current, temperature,
        luninous intensity and quantity.
        @type dims: list (variable number of arguments)
        """
        
        self.name = name
        """ Name of the user-defined dimension
        @type: string """

        self.l = 0
        """ Length (default unit - metre)
        @type: int """
        
        self.m = 0
        """ Mass (default unit - kilogram)
        @type: int """
        
        self.t = 0
        """ Time (default unit - second)
        @type: int """
        
        self.i = 0
        """ Electric current (default unit - ampere)
        @type: int """
        
        self.k = 0
        """ Temperature (default unit - kelvin)
        @type: int """
        
        self.c = 0
        """ Luminous intensity (default unit - candela)
        @type: int """
    
        self.n = 0
        """ Quantity (default unit - mole)
        @type: int """

        if len(dims) != 7:
            raise Error

        self.l = dims[0]
        self.m = dims[1]
        self.t = dims[2]
        self.i = dims[3]
        self.k = dims[4]
        self.c = dims[5]
        self.n = dims[6]
            

class Unit(LEMSBase):
    """
    Stores definition of unit symbols (eg, mV, ug) in terms of
    dimensions
    """
    
    def __init__(self, symbol, dimension, power):
        """
        Constructor
        
        @param symbol: Symbol name
        @type symbol: string
        
        @param dimension: User-defined dimension for this symbol
        @type dimension: lems.base.units.Dimension
        
        @param power: Scaling factor in terms of powers of 10 relative
        to the default dimensions for this unit
        @type power: int
        """

        self.symbol = symbol
        """ Symbol used to define this unit.
        @type: string """

        self.dimension = dimension
        """ Dimension of this unit.
        @type: string """

        self.power = power
        """ Scaling factor in terms of powers of 10 relative to
        the default dimensions for this unit.
        @type: int """

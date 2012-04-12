"""
Types for basic LEMS objects (Dimensions, units, ...)

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

class Dimension:
    """
    Store dimensionality of a user-defined quantities in terms of the
    seven fundamental SI units
    """

    name = ''
    """ Name of the user-defined dimension
    @type: string """

    l = 0
    """ Length (default unit - metre)
    @type: int """

    m = 0
    """ Mass (default unit - kilogram)
    @type: int
    """

    t = 0
    """ Time (default unit - second)
    @type: int """
    
    i = 0
    """ Electric current (default unit - ampere)
    @type: int """
    
    k = 0
    """ Temperature (default unit - kelvin)
    @type: int """
    
    c = 0
    """ Luminous intensity (default unit - candela)
    @type: int """
    
    n = 0
    """ Quantity (default unit - mole)
    @type: int """

class Unit:
    """
    Store definition of unit symbols (eg, mV, ug) in terms of
    dimensions
    """
    
    symbol = ''
    """ Symbol used to define this unit
    @type: string """

    dimension = None
    """ Dimension of this unit
    @type: pylems.base.units.Dimension """

    pow10 = 0
    """ Scaling factor in terms of powers of 10 relative to
    the default dimensions for this unit
    @type: int """

    def __init__(self, symbol, dimension, pow10):
        """
        Constructor
        
        @param symbol: Symbol name
        @type symbol: string
        
        @param dimension: User-defined dimension for this symbol
        @type dimension: pylems.base.units.Dimension
        
        @param pow10: Scaling factor in terms of powers of 10 relative
        to the default dimensions for this unit
        @type pow10: int
        """

        self.symbol = symbol
        self.dimension = dimension
        self.pow10 = pow10

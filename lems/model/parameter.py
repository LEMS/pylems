"""
Parameter storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import re
from lems.base.errors import ModelError
from lems.base.base import LEMSBase

class Parameter(LEMSBase):
    """
    Stores a parameter.
    """

    def __init__(self, name, dimension, fixed = False, value = None,
                 numeric_value = None):
        """
        Constructor

        @param name: Name of this parameter.
        @type name: string

        @param dimension: Dimension of this parameter.
        @type dimension: string

        @param fixed: Is this parameter fixed?
        @type fixed: Boolean

        @param value: Value of this parameter.
        @type value: string

        """

        self.name = name
        """ Parameter name.
        @type: string """
        
        self.dimension = dimension
        """ Dimension for this parameter.
        @type: string """
        
        self.fixed = fixed
        """ Set to True if this parameter has a fixed value.
        @type: Boolean """

        if fixed and value == None:
            raise ModelError('A numeric value must be provided to fix' +
                             'this parameter')
            
        self.value = value
        """ Value for this parameter.
        @type: string """

        self.numeric_value = numeric_value
        """ Numeric value of this parameter in terms of standard units.
        @type: Number """


    def fix_value(self, value):
        """
        Fixes the value of this parameter.

        @param value: Fixed value for this parameter.
        For example, "30mV" or "45 kg"
        @type value: string

        @raise ModelError: Raised ModelError if the parameter is already
        fixed.
        """

        if self.fixed:
            raise ModelError('Parameter already fixed.')

        self.set_value(value)
        self.fixed = True

    def set_value(self, value):
        """
        Sets the value of this parameter.

        @param value: Value for this parameter. For example, "30mV" or "45 kg"
        @type value: string

        @raise ModelError: Raised ModelError if the parameter is already fixed.
        """

        if self.fixed:
            raise ModelError('Parameter already fixed.')

        self.value = value


    ## def set_value_text(self, value_string, model):
    ##     """
    ##     Sets the value of this parameter.

    ##     @param value_string: Value for this parameter. For example, "30mV" or
    ##     "45 kg"
    ##     @type value_string: string

    ##     @raise: Raised ModelError if the parameter is already fixed.
    ##     """

    ##     if self.fixed:
    ##         raise ModelError('Parameter already fixed.')
        
    ##     split_loc = min(map(lambda x: 100
    ##                         if value_string.find(x) == -1
    ##                         else value_string.find(x), 
    ##     'abcdesghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        
    ##     self.value = int(value_string[0:split_loc])
    ##     sym = value_string[split_loc:].strip()

    ##     if sym not in model.units:
    ##         raise ModelError('Invalid symbol ' + sym)

    ##     dim1 = model.dimensions[model.units[sym].dimension]
    ##     dim2 = model.dimensions[self.dimension]
    ##     if dim1 != dim2:
    ##         raise ModelError('Dimension mismatch')

    ##     self.value *= 10 ** model.units[sym].pow10

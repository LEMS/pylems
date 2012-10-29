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

    def __str__(self):
        return '[Parameter - {0},{1},{2},{3}]'.format(
            self.name,
            self.dimension,
            self.value,
            self.fixed)


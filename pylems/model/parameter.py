"""
Parameter storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import re
from pylems.base.errors import ModelError
from pylems.base.base import PyLEMSBase

class ParameterType(PyLEMSBase):
    """
    Stores a parameter type.
    """

    def __init__(self, name, dimension):
        """
        Constructor

        @param name: Name of this parameter type
        @type name: string

        @param dimension: Dimension of this parameter type
        @type dimension: pylems.model.simple.Dimension
        """

        self.name = name
        """ Parameter name.
        @type: string """
        
        self.dimension = dimension
        """ Dimension for this parameter.
        @type: pylems.model.simple.Dimension """
        
        self.fixed = False
        """ Set to True if this parameter has a fixed value.
        @type: Boolean """
        
        self.fixed_value = None
        """ Fixed value for this parameter.
        @type: Number """


    def copy(self):
        """
        Makes a copy of this parameter type.

        @return: A copy of this parameter type.
        @rtype: pylems.model.parameter.ParameterType
        """

        return ParameterType(self.name, self.dimension)

    def fix_value(self, value_string, model):
        """
        Fixes the value of this parameter type.

        @param value_string: Fixed value for this parameter type.
        For example, "30mV" or "45 kg"
        @type value_string: string

        @param model: Model object storing the current model. (Needed to find
        the dimension for the specified symbol)
        @type model: pylems.model.model.Model

        @attention: Having to pass the model in as a parameter is a temporary
        hack. This should fixed at some point of time, once PyLems is able to
        run a few example files.
        """

        split_loc = min(map(lambda x: 100
                            if value_string.find(x) == -1
                            else value_string.find(x),
        'abcdesghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        
        self.fixed_value = int(value_string[0:split_loc])
        sym = value_string[split_loc:].strip()

        if sym not in model.units:
            raise ModelError('Invalid symbol ' + sym)

        if model.units[sym].dimension.name != self.dimension.name:
            raise ModelError('Dimension mismatch')

        self.fixed_value *= 10 ** model.units[sym].pow10

        self.fixed = True

class Parameter(PyLEMSBase):
    """
    Stores a parameter.
    """

    def __init__(self, parameter_type, value = None):
        """
        Constructor

        @param parameter_type: Type for this parameter.
        @type parameter_type: pylems.model.parameter.ParameterType

        @param value: Value for this parameter
        @type value: Number
        """

        self.parameter_type = parameter_type
        """ Parameter type.
        @type: pylems.model.paramater.ParameterType """

        self.value = value
        """ Value of this parameter.
        @type: Number """

    def set_value(self, value):
        """
        Sets the value of this parameter.

        @param value: Value for this parameter.
        @type value: Number
        """

        if self.parameter_type.fixed:
            self.value = self.parameter_type.fixed_value
        else:
            self.value = value

    def set_value_text(self, value_string, model):
        """
        Sets the value of this parameter.

        @param value_string: Value for this parameter. For example, "30mV" or
        "45 kg"
        @type value_string: string

        @param model: Model object storing the current model. (Needed to find
        the dimension for the specified symbol)
        @type model: pylems.model.model.Model

        @attention: Having to pass the model in as a parameter is a temporary
        hack. This should fixed at some point of time, once PyLems is able to
        run a few example files.
        """

        split_loc = min(map(lambda x: 100
                            if value_string.find(x) == -1
                            else value_string.find(x), 
        'abcdesghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        
        self.value = int(value_string[0:split_loc])
        sym = value_string[split_loc:].strip()

        if sym not in model.units:
            raise ModelError('Invalid symbol ' + sym)

        if model.units[sym].dimension.name != self.parameter_type.dimension.name:
            raise ModelError('Dimension mismatch')

        self.value *= 10 ** model.units[sym].pow10

    def copy(self):
        """
        Makes a copy of this parameter.

        @return: A copy of this parameter type.
        @rtype: pylems.model.parameter.ParameterType
        """

        return Parameter(self.parameter_type, self.value)


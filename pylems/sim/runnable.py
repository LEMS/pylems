"""
Base class for runnable components.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

class Reflective(object):
    @classmethod
    def add_method(cls, method_name, parameter_list, statements):
        code_string = 'def __generated_function__'
        if parameter_list == []:
            code_string += '():\n'
        else:
            code_string += '(' + parameter_list[0]
            for parameter in parameter_list[1:]:
                code_string += ', ' + parameter
            code_string += '):\n'

        for statement in statements:
            code_string += '    ' + statement + '\n'
        print code_string

        exec compile(ast.parse(code_string), '<unknown>', 'exec')
        setattr(cls, method_name, __generated_function__)
        del __generated_function__

class Runnable(Reflective):
    def __init__(self):
        self.variables = dict()
        self.time_derivatives = dict()

    def add_parameter(self, parameter_name, initial_value, time_derivative):
        self.variables[parameter_name] = initial_value
        self.time_derivatives[parameter_name] = time_derivative

    def build(self, component, model):
        pass

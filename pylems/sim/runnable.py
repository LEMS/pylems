"""
Base class for runnable components.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

import ast

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

    def add_instance_variable(self, variable, initial_value):
        code_string = 'self.{0} = {1}'.format(variable, initial_value)
        exec compile(ast.parse(code_string), '<unknown>', 'exec')
        
    
class Incremental(Reflective):
    def build(self, component, model):
        context = component.context
        
        for pn in context.parameters:
            p = context.parameters[pn]
            self.add_instance_variable(p.name, p.numeric_value)

        print help(self)
        print self.__dict__
            
    
class Runnable(Incremental):
    def __init__(self):
        Incremental.__init__(self)


"""
Base class for runnable components.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

import ast

class Reflective(object):
    def __init__(self):
        self.instance_variables = []
        
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

        if statements == []:
            code_string += '    pass'
        else:
            for statement in statements:
                code_string += '    ' + statement + '\n'

        exec compile(ast.parse(code_string), '<unknown>', 'exec')
        setattr(cls, method_name, __generated_function__)
        del __generated_function__

    def add_instance_variable(self, variable, initial_value):
        self.instance_variables += [variable]
    
        code_string = 'self.{0} = {1}'.format(variable, initial_value)
        exec compile(ast.parse(code_string), '<unknown>', 'exec')
        
class Runnable(Reflective):
    def __init__(self):
        Reflective.__init__(self)

        self.time_step = 0
        self.time_completed = 0
        self.time_total = 0

    def configure_time(self, time_step, time_total):
        self.time_step = time_step
        self.time_total = time_total
        
    def reset_time(self):
        self.time_completed = 0
        
    def time_step(self, dt):
        self.update_state_variables()
        self.update_shadow_variables()

        self.run_postprocessing_event_handlers()
        self.update_shadow_variables()

        self.time_completed += self.time_step
        if self.time_completed >= self.time_total:
            return 0
        else:
            return self.time_step

    def update_shadow_variables(self):
        for var in self.instance_variables:
            self.__dict__[var + '_shadow'] = self.__dict__[var]

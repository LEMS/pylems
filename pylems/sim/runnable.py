"""
Base class for runnable components.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.util import Stack
import ast

class Reflective(object):
    def __init__(self):
        self.instance_variables = []
        
    #@classmethod
    def add_method(self, method_name, parameter_list, statements):
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
        
        #setattr(cls, method_name, __generated_function__)
        self.__dict__[method_name] = __generated_function__
        del __generated_function__

    def add_instance_variable(self, variable, initial_value):
        self.instance_variables += [variable]
    
        code_string = 'self.{0} = {1}\nself.{0}_shadow = {1}'.format(\
            variable, initial_value)
        exec compile(ast.parse(code_string), '<unknown>', 'exec')
        
        
class Runnable(Reflective):
    def __init__(self):
        Reflective.__init__(self)

        self.time_step = 0
        self.time_completed = 0
        self.time_total = 0

        self.plastic = True

        self.state_stack = Stack()

        self.children = {}

        self.recorded_variables = {}

    def add_child(self, id, runnable):
        self.children[id] = runnable

    def add_variable_recorder(self, variable):
        self.recorded_variables[variable] = []

    def configure_time(self, time_step, time_total):
        self.time_step = time_step
        self.time_total = time_total
        
    def reset_time(self):
        self.time_completed = 0
        
        for cid in self.children:
            self.children[cid].reset_time()

    def single_step(self, dt):
        self.update_state_variables(self, dt)
        self.update_shadow_variables()

        self.run_postprocessing_event_handlers(self)
        self.update_shadow_variables()

        self.record_variables()

        for cid in self.children:
            self.children[cid].single_step(dt)

        self.time_completed += self.time_step
        if self.time_completed >= self.time_total:
            return 0
        else:
            return self.time_step

    def record_variables(self):
        for variable in self.recorded_variables:
            self.recorded_variables[variable] += [self.__dict__[variable]]
            
    def push_state(self):
        vars = []
        for varname in self.instance_variables:
            vars += [self.__dict__[varname],
                     self.__dict__[varname + '_shadow']]
        self.state_stack.push(vars)

        for cid in self.children:
            self.children[cid].push_state()

    def pop_state(self):
        vars = self.state_stack.pop()
        for varname in self.instance_variables:
            self.__dict_[varname] = vars[0]
            self.__dict_[varname + '_shadow'] = vars[1]
            vars = vars[2:]

        for cid in self.children:
            self.children[cid].pop_state()

    def update_shadow_variables(self):
        if self.plastic:
            for var in self.instance_variables:
                self.__dict__[var + '_shadow'] = self.__dict__[var]

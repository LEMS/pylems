"""
Recording class(es).

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase

class Recording(LEMSBase):
    """
    Stores details of a variable recording across a single simulation run.
    """

    def __init__(self, variable, full_path, data_output, recorder):
        self.variable = variable
        
        self.full_path = full_path
        
        self.data_output = data_output

        self.recorder = recorder

        self.values = []

    def __str__(self):
        return 'Recording: {0} ({1}), {2}, size: {3}'.format(self.variable, self.full_path, self.recorder, len(self.values))

    def __repr__(self):
        return self.__str__()

    def add_value(self, time, value):
        self.values.append((time, value))

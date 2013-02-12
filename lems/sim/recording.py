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

    def __init__(self, variable, data_output, recorder):
        self.variable = variable
        
        self.data_output = data_output

        self.recorder = recorder

        self.values = []

    def add_value(self, time, value):
        self.values.append((time, value))

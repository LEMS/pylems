"""
Parameter class definition.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

class Parameter(LEMSBase):
    def __init__(self, name, dimension):
        self.name = name
        self.dimension = dimension

        self.initialized = False
        self.value = None

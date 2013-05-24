"""
Model storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

class Model(LEMSBase):
    def __init__(self):
        self.dimensions = {}
        self.units = {}
        self.component_types = {}
        self.components = {}
        self.include_directories = ['.']

    def add_dimension(self, dimensions):
        pass  

    def add_unit(self, unit):
        pass

    def add_component_type(self, component_type):
        pass

    def add_component(self, component):
        pass

    def add_simulation(self, simulation):
        pass

    def add_include_directory(self, path):
        self.include_directories.append(path)

    def include_file(self, path):
        pass

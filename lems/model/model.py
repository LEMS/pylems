"""
Model storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase
from lems.parser import LEMSFileParser

class Model(LEMSBase):
    """
    Stores a model.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        
        self.dimensions = dict()
        """ Dictionary of dimensions defined in the model.
        @type: dict(str -> lems.model.fundamental.Dimension """
        
        self.units = dict()
        """ Dictionary of units defined in the model.
        @type: dict(str -> lems.model.fundamental.Unit """
        
        self.component_types = dict()
        """ Dictionary of component types defined in the model.
        @type: dict(str -> lems.model.component.ComponentType) """
        
        self.components = dict()
        """ Dictionary of root components defined in the model.
        @type: dict(str -> lems.model.component.Component) """
        
        self.include_directories = ['.']
        """ List of include directories to search for included LEMS files.
        @type: list(str) """

    def add_dimension(self, dimension):
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

    def import_from_file(self, filepath):
        parser = LEMSFileParser(self)
        with open(filepath) as f:
            parser.parse(f.read())
        
    def export_to_file(self, filepath):
        pass

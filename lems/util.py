"""
PyLEMS utility classes / functions

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

class Map(dict, LEMSBase):
    """
    Map class.

    Same as dict, but iterates over values.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        
        dict.__init__(self)

    def __iter__(self):
        """
        Returns an iterator.
        """
        
        return iter(self.values())

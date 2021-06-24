"""
Map class.

:author: Gautham Ganapathy
:organization: LEMS (https://github.com/organizations/LEMS)
"""

from lems.base.base import LEMSBase

class Map(dict, LEMSBase):
    """
    Map class.

    Same as dict, but iterates over values.
    """
    
    def __init__(self, *params, **key_params):
        """
        Constructor.
        """
        
        dict.__init__(self, *params, **key_params)

    def __iter__(self):
        """
        Returns an iterator.
        """
        
        return iter(self.values())

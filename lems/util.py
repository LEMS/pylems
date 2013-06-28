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

id_counter = 0

def make_id():
    global id_counter
    id_counter = id_counter + 1
    return '__id_{0}__'.format(id_counter)

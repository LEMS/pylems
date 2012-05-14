"""
PyLEMS base class.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import copy

class PyLEMSBase(object):
    def copy(self):
        return copy.deepcopy(self)

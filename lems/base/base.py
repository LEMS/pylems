"""
LEMS base class.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import copy

class LEMSBase(object):
    def copy(self):
        return copy.deepcopy(self)

"""
PyLEMS base class.

:author: Gautham Ganapathy
:organization: LEMS (https://github.com/organizations/LEMS)
"""

import copy

class LEMSBase(object):
    """
    Base object for PyLEMS.
    """

    def copy(self):
        return copy.deepcopy(self)

    def toxml(self):
        return ''

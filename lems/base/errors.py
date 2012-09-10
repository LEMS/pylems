"""
LEMS exceptions.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

class Error(Exception):
    """
    Exception to signal errors in PyLEMS.
    """
    
    def __init__(self, message):
        """
        Constructor

        @param message: Error message.
        @type message: string
        """
        
        self.message = message
        """ Error message
        @type: string """

    def __str__(self):
        """
        Returns the error message string.

        @return: The error message
        @rtype: string
        """
        
        return self.message

class StackError(Error):
    """
    Exception to signal errors in the PyLEMS Stack class.
    """

    pass

class ParseError(Error):
    """
    Exception to signal errors found during parsing.
    """

    pass

class ModelError(Error):
    """
    Exception to signal errors found during model generation.
    """

    pass

class SimBuildError(Error):
    """
    Exception to signal errors found while building simulation.
    """

    pass

class SimError(Error):
    """
    Exception to signal errors found while running simulation.
    """

    pass

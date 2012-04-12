"""
LEMS exceptions

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

class ParseError(Exception):
    """
    Exception to signal errors found during parsing
    """

    message = ''
    """ Error message
    @type: string """
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ModelError(Exception):
    """
    Exception to signal errors found during model generation
    """

    message = ''
    """ Error message
    @type: string """
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


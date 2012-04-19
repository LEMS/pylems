"""
Parser interface definition

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

class Parser(PyLEMSBase):
    """
    Parser interface class
    """

    def parse_file(self, filename):
        """
        Parse a file and generate a LEMS model

        @param filename: Path to the file to be parsed
        @type filename: string

        @return: LEMS model parsed from the input file
        """
        return None
    
    def parse_string(self, str):
        return None

"""
LEMS XML file format parser.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import xml.etree.ElementTree as xe

from lems.base import LEMSBase

class LEMSFileParser(LEMSBase):
    def __init__(self, model):
        pass

    def parse(self, xmltext):
        xml = xe.XML(xmltext)
        print(xml.tag)
        pass

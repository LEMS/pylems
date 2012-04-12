"""
LEMS parser

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from xml.etree import ElementTree as xml

from pylems.base.parser import Parser
from pylems.model.model import Model
from pylems.base.errors import ParseError

def xmltag(node):
    return node.tag.lower()
    
class LEMSParser(Parser):
    """
    Parser for LEMS files
    """

    model = None
    """ Model built during parsing
    @type: pylems.model.model.model """

    tag_parse_table = None
    """ Dictionary of xml tags to parse methods
    @type: dict(string -> function) """

    valid_children = None
    """ Dictionary mapping each tag to it's list of valid child tags """

    def init_parser(self):
        self.model = Model()
        self.token_list = None
        self.prev_token_lists = None

        self.valid_children = dict()
        self.valid_children['lems'] = ['componenttype', 'defaultrun',
                                       'dimension', 'unit']
        
        self.tag_parse_table = dict()
        self.tag_parse_table['componenttype'] = self.parse_component_type
        self.tag_parse_table['defaultrun'] = self.parse_default_run
        self.tag_parse_table['dimension'] = self.parse_dimension
        self.tag_parse_table['unit'] = self.parse_unit

    def get_model(self):
        return self.model

    def parse_component_type(self, node):
        print 'component type'

    def parse_default_run(self, node):
        self.model.set_default_run(node.attrib['component'])
    
    def parse_dimension(self, node):
        print 'dimension'

    def parse_unit(self, node):
        print 'unit'
    
    def parse_root(self, node):
        """
        Parse the <lems> (root) element of a LEMS file
        """
        
        tag = xmltag(node)
    
        if tag != 'lems':
            raise ParseError('Not a LEMS file')

        for child in node:
            tag = xmltag(child)

            if tag in self.valid_children['lems']:
                self.tag_parse_table[tag](child)
            else:
                # TODO: Check symbol table
                raise ParseError('Unexpected tag - <' + tag + '>')
            

    def parse_file(self, filename):
        """
        Parse a LEMS file and generate a LEMS model

        @param filename: Path to the LEMS file to be parsed
        @type filename: string
        """

        self.parse_root(xml.parse(filename).getroot())

    def parse_string(self, str):
        pass

"""
LEMS XML file format parser.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import xml.etree.ElementTree as xe

from lems.base import LEMSBase
from lems.exceptions import ParseException

def get_xml_attr_value(node, attr):
    attrib_iter = node.attrib.items()
    lattr = attr.lower()
    for (k, v) in attrib_iter:
        if k.lower() == lattr:
            return v
    return None

class LEMSFileParser(LEMSBase):
    """
    LEMS XML file format parser class.
    """
    
    def __init__(self, model):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """

        self.model = model
        """
        Model instance to be populated from the parsed file.
        @type: lems.model.model.Model
        """

        self.tag_parse_table = None
        """ Dictionary of xml tags to parse methods
        @type: dict(string -> function) """

        self.valid_children = None
        """ Dictionary mapping each tag to it's list of valid child tags.
        @type: dict(string -> string) """

        self.id_counter = None
        """ Counter generator for generating unique ids.
        @type: generator(int) """
        
        self.init_parser()

    def init_parser(self):
        """
        Initializes the parser
        """

        #self.token_list = None
        #self.prev_token_lists = None

        self.valid_children = dict()
        self.valid_children['lems'] = ['component', 'componenttype',
                                       'target', 'include',
                                       'dimension', 'unit', 'assertion']
        self.valid_children['componenttype'] = ['dynamics',
                                                'child', 'children',
                                                'componentreference',
                                                'exposure', 'eventport',
                                                'fixed', 'link', 'parameter',
                                                'path', 'requirement',
                                                'simulation', 'structure',
                                                'text', 'attachments',
                                                'constant', 'derivedparameter']
        self.valid_children['dynamics'] = ['derivedvariable',
                                           'oncondition', 'onentry',
                                           'onevent', 'onstart',
                                           'statevariable', 'timederivative',
                                           'kineticscheme', 'regime']
        self.valid_children['regime'] = ['derivedvariable',
                                         'oncondition', 'onentry',
                                         'onevent', 'onstart',
                                         'statevariable', 'timederivative',
                                         'kineticscheme', 'transition']
        self.valid_children['oncondition'] = ['eventout', 'stateassignment']
        self.valid_children['onentry'] = ['eventout', 'stateassignment']
        self.valid_children['onevent'] = ['eventout', 'stateassignment']
        self.valid_children['onstart'] = ['eventout', 'stateassignment']
        self.valid_children['structure'] = ['childinstance',
                                            'eventconnection',
                                            'foreach',
                                            'multiinstantiate']
        self.valid_children['simulation'] = ['record', 'run',
                                             'datadisplay', 'datawriter']

        self.tag_parse_table = dict()
        #self.tag_parse_table['assertion'] = self.parse_assertion
        #self.tag_parse_table['attachments'] = self.parse_attachments
        #self.tag_parse_table['child'] = self.parse_child
        #self.tag_parse_table['childinstance'] = self.parse_child_instance
        #self.tag_parse_table['children'] = self.parse_children
        #self.tag_parse_table['component'] = self.parse_component
        #self.tag_parse_table['componentreference'] = self.parse_component_reference
        #self.tag_parse_table['componenttype'] = self.parse_component_type
        #self.tag_parse_table['constant'] = self.parse_constant
        #self.tag_parse_table['datadisplay'] = self.parse_data_display
        #self.tag_parse_table['datawriter'] = self.parse_data_writer
        #self.tag_parse_table['derivedparameter'] = self.parse_derived_parameter
        #self.tag_parse_table['derivedvariable'] = self.parse_derived_variable
        #self.tag_parse_table['dimension'] = self.parse_dimension
        #self.tag_parse_table['dynamics'] = self.parse_dynamics
        #self.tag_parse_table['eventconnection'] = self.parse_event_connection
        #self.tag_parse_table['eventout'] = self.parse_event_out
        #self.tag_parse_table['eventport'] = self.parse_event_port
        #self.tag_parse_table['exposure'] = self.parse_exposure
        #self.tag_parse_table['fixed'] = self.parse_fixed
        #self.tag_parse_table['foreach'] = self.parse_foreach
        #self.tag_parse_table['include'] = self.parse_include
        #self.tag_parse_table['kineticscheme'] = self.parse_kinetic_scheme
        #self.tag_parse_table['link'] = self.parse_link
        #self.tag_parse_table['multiinstantiate'] = self.parse_multi_instantiate
        #self.tag_parse_table['oncondition'] = self.parse_on_condition
        #self.tag_parse_table['onentry'] = self.parse_on_entry
        #self.tag_parse_table['onevent'] = self.parse_on_event
        #self.tag_parse_table['onstart'] = self.parse_on_start
        #self.tag_parse_table['parameter'] = self.parse_parameter
        #self.tag_parse_table['path'] = self.parse_path
        #self.tag_parse_table['record'] = self.parse_record
        #self.tag_parse_table['regime'] = self.parse_regime
        #self.tag_parse_table['requirement'] = self.parse_requirement
        #self.tag_parse_table['run'] = self.parse_run
        #self.tag_parse_table['show'] = self.parse_show
        #self.tag_parse_table['simulation'] = self.parse_simulation
        #self.tag_parse_table['stateassignment'] = self.parse_state_assignment
        #self.tag_parse_table['statevariable'] = self.parse_state_variable
        #self.tag_parse_table['structure'] = self.parse_structure
        #self.tag_parse_table['target'] = self.parse_target
        #self.tag_parse_table['text'] = self.parse_text
        #self.tag_parse_table['timederivative'] = self.parse_time_derivative
        #self.tag_parse_table['transition'] = self.parse_transition
        #self.tag_parse_table['unit'] = self.parse_unit
        #self.tag_parse_table['with'] = self.parse_with

        self.xml_node_stack = []
        
        def counter():
            count = 1
            while True:
                yield count
                count = count + 1

        self.id_counter = counter()
        
    def process_nested_tags(self, node):
        """
        Process child tags.

        @param node: Current node being parsed.
        @type node: xml.etree.Element

        @raise ParseError: Raised when an unexpected nested tag is found.
        """

        for child in node:
            self.xml_node_stack = [child] + self.xml_node_stack

            ctagl = child.tag.lower()

            if ctagl in self.tag_parse_table:
                self.tag_parse_table[ctagl](child)
            else:
                raise ParseException("Unrecognized tag '{0}'", ctagl)
                #self.parse_component_by_typename(child, child.tag)

            self.xml_node_stack = self.xml_node_stack[1:]

    def parse(self, xmltext):
        """
        Parse a string containing LEMS XML text.

        @param xmltext: String containing LEMS XML formatted text.
        @type xmltext: str
        """
        
        xml = xe.XML(xmltext)

        if xml.tag.lower() != 'lems':
            raise ParseException('<lems> expected as root element')

        self.process_nested_tags(xml)

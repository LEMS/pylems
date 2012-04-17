"""
LEMS parser

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from xml.etree import ElementTree as xml

from pylems.model.simple import Dimension,Unit
from pylems.base.parser import Parser
from pylems.model.model import Model
from pylems.base.errors import ParseError
from pylems.model.context import Context,Contextual
from pylems.model.component import Component,ComponentType
from pylems.model.parameter import Parameter

def xmltolower(node):
    """ Converts the tag and attribute names in the given XML node and
    child nodes to lower case. To convert the entire tree, pass in the
    root.

    @param node: Node in an XML tree.
    @type node: xml.etree.Element """
    node.tag = node.tag.lower()
    lattrib = dict()
    for key in node.attrib:
        lattrib[key.lower()] = node.attrib[key]
    node.attrib = lattrib
    for child in node:
        xmltolower(child)
    
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
    """ Dictionary mapping each tag to it's list of valid child tags.
    @type: dict(string -> string) """

    context_stack = []
    """ Stack of contexts used for handling nested contexts.
    @type: list(pylems.model.context.Context) """

    current_context = None
    """ Currently active (being parsed) context.
    @type: pylems.model.context.Context """

    parametric_stack = []
    """ Stack of parametric objects used for handling nested component types.
    @type: list(pylems.model.parameter.Parametric) """

    current_parametric = None
    """ Parametric object being parsed.
    @type: pylems.model.parameter.Parametric """

    def push_context(self, context):
        self.context_stack = [context] + self.context_stack
        self.current_context = context

    def pop_context(self):
        if len(self.context_stack) == 0:
            raise ParseError('Context stack underflow')
        self.context_stack = self.context_stack[1:]
        if len(self.context_stack) == 0:
            self.current_context = None
        else:
            self.current_context = self.context_stack[0]
 
    def push_parametric(self, parametric):
        self.parametric_stack = [parametric] + self.parametric_stack
        self.current_parametric = parametric

    def pop_parametric(self):
        if len(self.parametric_stack) == 0:
            raise ParseError('Parametric stack underflow')
        self.parametric_stack = self.parametric_stack[1:]
        if len(self.parametric_stack) == 0:
            self.current_parametric = None
        else:
            self.current_parametric = self.parametric_stack[0]

    def init_parser(self):
        """
        Initializes the parser
        """
        
        self.model = Model()
        self.token_list = None
        self.prev_token_lists = None

        self.valid_children = dict()
        self.valid_children['lems'] = ['component', 'componenttype', 'defaultrun',
                                       'dimension', 'unit']
        self.valid_children['componenttype'] = ['parameter']
        
        self.tag_parse_table = dict()
        self.tag_parse_table['component'] = self.parse_component
        self.tag_parse_table['componenttype'] = self.parse_component_type
        self.tag_parse_table['defaultrun'] = self.parse_default_run
        self.tag_parse_table['dimension'] = self.parse_dimension
        self.tag_parse_table['unit'] = self.parse_unit
        self.tag_parse_table['parameter'] = self.parse_parameter

    def get_model(self):
        """
        Returns the generated model.

        @return: The generated model.
        @rtype: pylems.model.model.Model
        """
        
        return self.model

    def parse_component_type(self, node):
        """
        Parse <ComponentType>

        @param node: Node containing the <ComponentType> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the component type does not have a name.
        @raise ParseError: Raised when the component type extends an udefined
        component type.
        @raise ParseError: Raised when an unexpected nested component is found.
        """
        
        try:
            name = node.attrib['name']
        except:
            raise ParseError('Component type must have a name')

        if 'extends' in node.attrib:
            if node.attrib['extends'] in current_context.component_types:
                extends = current_context.component_types[node.attrib['extends']]
            else:
                raise ParseError('Component type \'' + name + 
                                 '\' extends an undefined base type \'' + 
                                 node.attrib['extends'])
        else:
            extends = None

        component_type = ComponentType(name, extends)
        self.current_context.add_component_type(component_type)

        self.push_parametric(component_type)

        for child in node:
            if child.tag in self.valid_children['componenttype']:
                self.tag_parse_table[child.tag](child)
            else:
                raise ParseError('Unexpected tag - <' + child.tag + '>')

        self.pop_parametric()

    def parse_default_run(self, node):
        """
        Parse <DefaultRun>

        @param node: Node containing the <DefaultRun> element
        @type node: xml.etree.Element
        """
        
        self.model.set_default_run(node.attrib['component'])
    
    def parse_dimension(self, node):
        """
        Parse <Dimension>

        @param node: Node containing the <Dimension> element
        @type node: xml.etree.Element

        @raise ParseError: When the name is not a string or if the dimension is
        not a signed integer.
        """
        
        dim = list()
        try:
            name = node.attrib['name']
            for d in ['l', 'm', 't', 'i', 'k', 'c', 'n']:
                dim.append(int(node.attrib.get(d, 0)))
        except:
            raise ParseError('Invalid dimensionality format')

        self.model.add_dimension(Dimension(name, dim[0], dim[1], dim[2],
                                           dim[3], dim[4], dim[4], dim[6]))
            
    def parse_parameter(self, node):
        """
        Parse <Parameter>

        @param node: Node containing the <Parameter> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the parameter does not have a name.
        @raise ParseError: Raised when the parameter does not have a dimension.
        """
        
        try:
            name = node.attrib['name']
        except:
            raise ParseError('Parameter must have a name')

        try:
            dimension = node.attrib['dimension']
        except:
            raise ParseError('Parameter must have a dimension')

        parameter = Parameter(name, dimension)
        
        try:
            self.current_parametric.add_parameter(parameter)
        except:
            raise ParseError('Parameter definition is not permitted in this location')

    def parse_unit(self, node):
        """
        Parse <Unit>

        @param node: Node containing the <Unit> element
        @type node: xml.etree.Element

        @raise ParseError: When the name is not a string or the unit
        specfications are incorrect.

        @raise ModelError: When the unit refers to an undefined dimension.
        """

        try:
            symbol = node.attrib['symbol']
            dim = node.attrib['dimension']
            pow10 = int(node.attrib['powten'])
        except:
            raise ParseError('Invalid unit format')

        if dim not in self.model.dimensions:
            raise ModelError('Reference to undefined dimension')
        
        self.model.add_unit(Unit(symbol, self.model.dimensions[dim], pow10))
    
    def parse_root(self, node):
        """
        Parse the <lems> (root) element of a LEMS file
        
        @param node: Node containing the <LEMS> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when an unexpected XML child tag is found.
        """
        
        if node.tag != 'lems':
            raise ParseError('Not a LEMS file')

        for child in node:
            if child.tag in self.valid_children['lems']:
                self.tag_parse_table[child.tag](child)
            else:
                # TODO: Check symbol table
                raise ParseError('Unexpected tag - <' + child.tag + '>')
            
    def parse_file(self, filename):
        """
        Parse a LEMS file and generate a LEMS model

        @param filename: Path to the LEMS file to be parsed
        @type filename: string
        """

        root = xml.parse(filename).getroot()
        xmltolower(root)

        context = Context(self.current_context)
        if self.model.context == None:
            self.model.context = context

        self.push_context(context)

        self.parse_root(root)

        self.pop_context()


    def parse_string(self, str):
        pass

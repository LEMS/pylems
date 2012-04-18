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
from pylems.base.errors import ParseError,ModelError
from pylems.model.context import Context,Contextual
from pylems.model.component import Component,ComponentType
from pylems.model.parameter import Parameter,ParameterType

def xmltolower(node):
    """ Converts the tag and attribute names in the given XML node and
    child nodes to lower case. To convert the entire tree, pass in the
    root.

    @param node: Node in an XML tree.
    @type node: xml.etree.Element """
    node.tag = node.tag.lower()
    lattrib = dict()
    for key in node.attrib:
        lattrib[key] = node.attrib[key]
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

    component_type_stack = []
    """ Stack of component type objects used for handling nested component types.
    @type: list(pylems.model.parameter.ComponentType) """

    current_component_type = None
    """ Component type object being parsed.
    @type: pylems.model.parameter.ComponentType """

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
 
    def push_component_type(self, component_type):
        self.component_type_stack = [component_type] + self.component_type_stack
        self.current_component_type = component_type

    def pop_component_type(self):
        if len(self.component_type_stack) == 0:
            raise ParseError('Component_Type stack underflow')
        self.component_type_stack = self.component_type_stack[1:]
        if len(self.component_type_stack) == 0:
            self.current_component_type = None
        else:
            self.current_component_type = self.component_type_stack[0]

    def init_parser(self):
        """
        Initializes the parser
        """
        
        self.model = Model()
        self.token_list = None
        self.prev_token_lists = None

        self.valid_children = dict()
        self.valid_children['lems'] = ['component', 'componenttype', 
                                       'defaultrun', 'dimension', 'unit']
        self.valid_children['componenttype'] = ['behavior', 'behaviour', 'child', 
                                                'exposure', 'eventport', 
                                                'fixed', 'parameter',
                                                'requirement']
        self.valid_children['behaviour'] = ['onevent', 'statevariable', 
                                            'timederivative']
        self.valid_children['onevent'] = ['stateassignment']

        self.tag_parse_table = dict()
        self.tag_parse_table['behavior'] = self.parse_behaviour
        self.tag_parse_table['behaviour'] = self.parse_behaviour
        self.tag_parse_table['child'] = self.parse_child
        self.tag_parse_table['children'] = self.parse_children
        self.tag_parse_table['component'] = self.parse_component
        self.tag_parse_table['componenttype'] = self.parse_component_type
        self.tag_parse_table['defaultrun'] = self.parse_default_run
        self.tag_parse_table['dimension'] = self.parse_dimension
        self.tag_parse_table['exposure'] = self.parse_exposure
        self.tag_parse_table['eventport'] = self.parse_event_port
        self.tag_parse_table['fixed'] = self.parse_fixed
        self.tag_parse_table['onevent'] = self.parse_on_event
        self.tag_parse_table['parameter'] = self.parse_parameter
        self.tag_parse_table['requirement'] = self.parse_requirement
        self.tag_parse_table['stateassignment'] = self.parse_state_assignment
        self.tag_parse_table['statevariable'] = self.parse_state_variable
        self.tag_parse_table['timederivative'] = self.parse_time_derivative
        self.tag_parse_table['unit'] = self.parse_unit




    def process_nested_tags(self, node):
        """
        Process child tags.

        @param node: Current node being parsed.
        @type node: xml.etree.Element

        @raise ParseError: Raised when an unexpected nested tag is found.
        """
        for child in node:
            if child.tag in self.valid_children[node.tag]:
                self.tag_parse_table[child.tag](child)
            elif child.tag in self.current_context.component_types:
                self.parse_component_by_typename(child, child.tag)
            else:
                raise ParseError('Unexpected tag - <' + child.tag + '>')

    def resolve_typename(self, typename):
        """ 
        Resolve type name from the contex stack.

        @param typename: Name of the type to be resolved.
        @type typename: string

        @return: Component type corresponding to the type name or None if undefined.
        @rtype: pylems.model.component.ComponentType
        """

        stack = self.context_stack
        found = False
        while stack != [] and (not found):
            if typename in stack[0].component_types:
                found = True
                
        if found:
            return stack[0].component_types[typename]
        else:
            return None

    def get_model(self):
        """
        Returns the generated model.

        @return: The generated model.
        @rtype: pylems.model.model.Model
        """
        
        return self.model

    def parse_behaviour(self, node):
        """
        Parse <Behaviour>

        @param node: Node containing the <Behaviour> element
        @type node: xml.etree.Element
        """

        pass

    def parse_child(self, node):
        """
        Parse <Child>

        @param node: Node containing the <Child> element
        @type node: xml.etree.Element
        """

        pass

    def parse_children(self, node):
        """
        Parse <Children>

        @param node: Node containing the <Children> element
        @type node: xml.etree.Element
        """

        pass

    def parse_component_by_typename(self, node, typename):
        """
        Parses components defined directly by component name.

        @param node: Node containing the <Component> element
        @type node: xml.etree.Element

        @param typename: Name of the component type.
        @type typename: string

        @raise ParseError: Raised when the component does not have an id.
        @raise ModelError: Raised when the component has an undefined type.
        """

        try:
            id = node.attrib['id']
        except:
            raise ParseError('Component must have an id')

        component_type = self.resolve_typename(typename)
        if component_type == None:
            raise ModelError('Undefined component type')

        component = Component(id, component_type)
        
        for param in node.attrib:
            if param != 'id' and param != 'type':
                if param in component.parameters:
                    component.parameters[param].set_value_text(node.attrib[param], self.model)

        self.current_context.add_component(component)

        for param in component.parameters:
            if component.parameters[param].value == None:
                raise ModelError('Parameter ' + param + ' not initialized in component ' + id)

    def parse_component(self, node):
        """
        Parses <Component>

        @param node: Node containing the <ComponentType> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the component does not have a type.
        """
        
        try:
            type = node.attrib['type']
        except:
            raise ParseError('Component must have a type')

        self.parse_component_by_typename(node, type)

    def parse_component_type(self, node):
        """
        Parses <ComponentType>

        @param node: Node containing the <ComponentType> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the component type does not have a name.
        @raise ParseError: Raised when the component type extends an udefined
        component type.
        """
        
        try:
            name = node.attrib['name']
        except:
            raise ParseError('Component type must have a name')

        if 'extends' in node.attrib:
            if node.attrib['extends'] in self.current_context.component_types:
                extends = self.current_context.component_types[node.attrib['extends']]
            else:
                raise ParseError('Component type \'' + name + 
                                 '\' extends an undefined base type \'' + 
                                 node.attrib['extends'])
        else:
            extends = None

        component_type = ComponentType(name, extends)
        self.current_context.add_component_type(component_type)

        self.push_component_type(component_type)
        self.process_nested_tags(node)
        self.pop_component_type()

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
            
    def parse_event_port(self, node):
        """
        Parse <EventPort>

        @param node: Node containing the <EventPort> element
        @type node: xml.etree.Element
        """

        pass

    def parse_exposure(self, node):
        """
        Parse <Exposure>

        @param node: Node containing the <Exposure> element
        @type node: xml.etree.Element
        """

        pass

    def parse_fixed(self, node):
        """
        Parse <Fixed>

        @param node: Node containing the <Fixed> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when
        """
        
        try:
            parameter_name = node.attrib['parameter']
        except:
            raise ParseError('Parameter to be fixed must be specified')

        try:
            value = node.attrib['value']
        except:
            raise ParseError('Value to be fixed must be specified')

        if not self.current_component_type:
            raise ParseError('Fixed parameter specification is not permitted in this location')

        self.current_component_type.fix_parameter_type(parameter_name, value, self.model)

    def parse_on_event(self, node):
        """
        Parse <OnEvent>

        @param node: Node containing the <OnEvent> element
        @type node: xml.etree.Element
        """

        pass

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

        if dimension not in self.model.dimensions:
            raise ModelError('Undefined dimension ' + dimension)

        parameter_type = ParameterType(name, self.model.dimensions[dimension])

        if not self.current_component_type:
            raise ParseError('Parameter definition is not permitted in this location')

        self.current_component_type.add_parameter_type(parameter_type)

    def parse_requirement(self, node):
        """
        Parse <Requirement>

        @param node: Node containing the <Requirement> element
        @type node: xml.etree.Element
        """

        pass

    def parse_state_assignment(self, node):
        """
        Parse <StateAssignment>

        @param node: Node containing the <StateAssignment> element
        @type node: xml.etree.Element
        """

        pass

    def parse_state_variable(self, node):
        """
        Parse <StateVariable>

        @param node: Node containing the <StateVariable> element
        @type node: xml.etree.Element
        """

        pass

    def parse_time_derivative(self, node):
        """
        Parse <TimeDerivative>

        @param node: Node containing the <TimeDerivative> element
        @type node: xml.etree.Element
        """

        pass

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
        """
        
        if node.tag != 'lems':
            raise ParseError('Not a LEMS file')

        self.process_nested_tags(node)
            
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

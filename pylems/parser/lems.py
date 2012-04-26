"""
LEMS parser

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from xml.etree import ElementTree as xml
import os.path

from pylems.model.simple import Dimension,Unit
from pylems.base.parser import Parser
from pylems.model.model import Model
from pylems.base.errors import ParseError,ModelError
from pylems.model.context import Context,Contextual
from pylems.model.component import Component,ComponentType
from pylems.model.parameter import Parameter
from pylems.model.behavior import Behavior,Regime,OnCondition,StateAssignment

def xmltolower(node):
    """ Converts the tag and attribute names in the given XML node and
    child nodes to lower case. To convert the entire tree, pass in the
    root.

    @param node: Node in an XML tree.
    @type node: xml.etree.Element """

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

    base_path = '.'
    """ Base path for the file being parsed
    @type: string """

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

    current_regime = None
    """ Current behavior regime being parsed.
    @type: pylems.model.behavior.Regime """

    current_event_handler = None
    """ Current event_handler being parsed.
    @type: pylems.model.behavior.EventHandler """

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
                                       'defaultrun', 'dimension', 'include',
                                       'unit']
        self.valid_children['componenttype'] = ['behavior', 'behaviour',
                                                'child', 'children',
                                                'componentref',
                                                'exposure', 'eventport', 
                                                'fixed', 'link', 'parameter',
                                                'path', 'requirement', 'text']
        self.valid_children['behavior'] = ['build', 'derivedvariable',
                                           'oncondition', 'onevent',
                                           'onstart', 'record', 'run', 'show',
                                           'statevariable', 'timederivative']
        self.valid_children['oncondition'] = ['eventout', 'stateassignment']
        self.valid_children['onevent'] = ['stateassignment']
        self.valid_children['onstart'] = ['stateassignment']

        self.tag_parse_table = dict()
        self.tag_parse_table['behavior'] = self.parse_behavior
        self.tag_parse_table['build'] = self.parse_build
        self.tag_parse_table['child'] = self.parse_child
        self.tag_parse_table['children'] = self.parse_children
        self.tag_parse_table['component'] = self.parse_component
        self.tag_parse_table['componentref'] = self.parse_component_ref
        self.tag_parse_table['componenttype'] = self.parse_component_type
        self.tag_parse_table['defaultrun'] = self.parse_default_run
        self.tag_parse_table['derivedvariable'] = self.parse_derived_variable
        self.tag_parse_table['dimension'] = self.parse_dimension
        self.tag_parse_table['eventout'] = self.parse_event_out
        self.tag_parse_table['eventport'] = self.parse_event_port
        self.tag_parse_table['exposure'] = self.parse_exposure
        self.tag_parse_table['fixed'] = self.parse_fixed
        self.tag_parse_table['include'] = self.parse_include
        self.tag_parse_table['link'] = self.parse_link
        self.tag_parse_table['oncondition'] = self.parse_on_condition
        self.tag_parse_table['onevent'] = self.parse_on_event
        self.tag_parse_table['onstart'] = self.parse_on_start
        self.tag_parse_table['parameter'] = self.parse_parameter
        self.tag_parse_table['path'] = self.parse_path
        self.tag_parse_table['record'] = self.parse_record
        self.tag_parse_table['requirement'] = self.parse_requirement
        self.tag_parse_table['run'] = self.parse_run
        self.tag_parse_table['show'] = self.parse_show
        self.tag_parse_table['stateassignment'] = self.parse_state_assignment
        self.tag_parse_table['statevariable'] = self.parse_state_variable
        self.tag_parse_table['text'] = self.parse_text
        self.tag_parse_table['timederivative'] = self.parse_time_derivative
        self.tag_parse_table['unit'] = self.parse_unit

        def counter():
            count = 1
            while True:
                yield count
                count = count + 1
                
        self.id_counter = counter()
        """ Counter genertor for generating unique ids.
        @type: int """
        

    prefix = ''

    def process_nested_tags(self, node):
        """
        Process child tags.

        @param node: Current node being parsed.
        @type node: xml.etree.Element

        @raise ParseError: Raised when an unexpected nested tag is found.
        """

        #self.prefix += '  '

        for child in node:
            #print self.prefix, child.tag,
            #print child.attrib['name'] if 'name' in child.attrib else '',
            #print child.attrib['id'] if 'id' in child.attrib else ''

            ctagl = child.tag.lower()

            if ctagl in self.tag_parse_table:
                self.tag_parse_table[ctagl](child)
            else:
                self.parse_component_by_typename(child, child.tag)

        #self.prefix = self.prefix[2:]

    def resolve_typename(self, typename):
        """ 
        Resolves type name from the contex stack.

        @param typename: Name of the type to be resolved.
        @type typename: string

        @return: Component type corresponding to the type name or None if
        undefined.
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

    def resolve_component_name(self, component_name):
        """ 
        Resolves component name from the contex stack.

        @param component_name: Name of the component to be resolved.
        @type component_name: string

        @return: Component corresponding to the name or None if undefined.
        @rtype: pylems.model.component.Component
        """

        stack = self.context_stack
        found = False
        while stack != [] and (not found):
            if component_name in stack[0].components:
                found = True
                
        if found:
            return stack[0].components[component_name]
        else:
            return None

    def get_model(self):
        """
        Returns the generated model.

        @return: The generated model.
        @rtype: pylems.model.model.Model
        """
        
        return self.model

    def parse_behavior(self, node):
        """
        Parses <Behavior>

        @param node: Node containing the <Behaviour> element
        @type node: xml.etree.Element
        """

        if self.current_context.context_type != Context.COMPONENT_TYPE:
            raise ParseError('Behavior must be defined inside a component type')

        if 'name' in node.attrib:
            name = node.attrib['name']
        else:
            name = ''

        self.current_context.add_behavior_profile(name)
        
        old_regime = self.current_regime
        self.current_regime = self.current_context.selected_behavior_profile.\
                              default_regime
        
        self.process_nested_tags(node)
        
        self.current_regime = old_regime

    def parse_build(self, node):
        """
        Parses <Build>

        @param node: Node containing the <Build> element
        @type node: xml.etree.Element
        """

        pass

    def parse_child(self, node):
        """
        Parses <Child>

        @param node: Node containing the <Child> element
        @type node: xml.etree.Element
        """
        
        if self.current_context.context_type != Context.COMPONENT_TYPE:
            raise ParseError('Child definitions can only be made in ' +
                             'a component type')
        
        if 'name' in node.attrib:
            name = node.attrib['name']
        else:
            raise ParseError('<Child> must specify a name for the ' +
                             'reference.')

        if 'type' in node.attrib:
            type = node.attrib['type']
        else:
            raise ParseError('<Child> must specify a type for the ' +
                             'reference.')
            
        self.current_context.add_child(name, type)

    def parse_children(self, node):
        """
        Parses <Children>

        @param node: Node containing the <Children> element
        @type node: xml.etree.Element
        """
        
        if self.current_context.context_type != Context.COMPONENT_TYPE:
            raise ParseError('Children definitions can only be made in ' +
                             'a component type')
        
        if 'name' in node.attrib:
            name = node.attrib['name']
        else:
            raise ParseError('<Children> must specify a name for the ' +
                             'reference.')

        if 'type' in node.attrib:
            type = node.attrib['type']
        else:
            raise ParseError('<Children> must specify a type for the ' +
                             'reference.')
            
        self.current_context.add_children(name, type)

    def parse_component_by_typename(self, node, type):
        """
        Parses components defined directly by component name.

        @param node: Node containing the <Component> element
        @type node: xml.etree.Element

        @param type: Type of this component.
        @type type: string

        @raise ParseError: Raised when the component does not have an id.
        """

        if self.current_context.context_type == Context.GLOBAL:
            # Global component instatiation
            if 'id' in node.attrib:
                id = node.attrib['id']
            else:
                raise ParseError('Component must have an id')
            
            type = node.tag

            component = Component(id, self.current_context, type, None)
            self.current_context.add_component(component)
        else:
            # Child instantiation
            if 'id' in node.attrib:
                id = node.attrib['id']
            else:
                id = '__id_inherited__' + str(self.id_counter.next())

            type = node.tag
            ## if 'type' in node.attrib:
            ##     type = node.attrib['type']
            ## else:
            ##     type = '__type_inherited__'

            component = Component(id, self.current_context, type)
            
            for key in node.attrib:
                if key != 'id' and key != 'type':
                    param = Parameter(key, '__dimension_inherited__')
                    param.set_value(node.attrib[key])
                    component.add_parameter(param)
            self.current_context.add_component(component)

        self.push_context(component.context)
        self.process_nested_tags(node)
        self.pop_context()

    def parse_component(self, node):
        """
        Parses <Component>

        @param node: Node containing the <ComponentType> element
        @type node: xml.etree.Element
        """

        if 'id' in node.attrib:
            id = node.attrib['id']
        else:            
            raise ParseError('Component must have an id')
        
        if 'type' in node.attrib:
            type = node.attrib['type']
        else:
            type = None

        if type == None:
            if 'extends' in node.attrib:
                extends = node.attrib['extends']
            else:
                raise ParseError('Component must have a type or must extend ' +
                                 'another component')
        else:
            extends = None

        component = Component(id, self.current_context, type, extends)
        self.current_context.add_component(component)

        self.push_context(component.context)
        self.process_nested_tags(node)
        self.pop_context()

    def parse_component_ref(self, node):
        """
        Parses <ComponentRef>

        @param node: Node containing the <ComponentTypeRef> element
        @type node: xml.etree.Element
        """
        
        if self.current_context.context_type != Context.COMPONENT_TYPE:
            raise ParseError('Component references can only be defined in ' +
                             'a component type')
        
        if 'name' in node.attrib:
            name = node.attrib['name']
        else:
            raise ParseError('<ComponentRef> must specify a name for the ' +
                             'reference.')

        if 'type' in node.attrib:
            type = node.attrib['type']
        else:
            raise ParseError('<ComponentRef> must specify a type for the ' +
                             'reference.')
            
        self.current_context.add_component_ref(name, type)
        
    def parse_component_type(self, node):
        """
        Parses <ComponentType>

        @param node: Node containing the <ComponentType> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the component type does not have a name.
        """
        
        try:
            name = node.attrib['name']
        except:
            raise ParseError('Component type must have a name')

        if 'extends' in node.attrib:
            extends = node.attrib['extends']
        else:
            extends = None

        component_type = ComponentType(name, self.current_context, extends)
        self.current_context.add_component_type(component_type)

        self.push_context(component_type.context)
        self.process_nested_tags(node)
        self.pop_context()

    def parse_default_run(self, node):
        """
        Parses <DefaultRun>

        @param node: Node containing the <DefaultRun> element
        @type node: xml.etree.Element
        """
        
        self.model.add_default_run(node.attrib['component'])
    
    def parse_derived_variable(self, node):
        """
        Parses <DerivedVariable>

        @param node: Node containing the <DerivedVariable> element
        @type node: xml.etree.Element
        """

        pass

    def parse_dimension(self, node):
        """
        Parses <Dimension>

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
            
    def parse_event_out(self, node):
        """
        Parses <EventOut>

        @param node: Node containing the <EventOut> element
        @type node: xml.etree.Element
        """

        pass

    def parse_event_port(self, node):
        """
        Parses <EventPort>

        @param node: Node containing the <EventPort> element
        @type node: xml.etree.Element
        """

        pass

    def parse_exposure(self, node):
        """
        Parses <Exposure>

        @param node: Node containing the <Exposure> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the exposure name is not
        being defined in the context of a component type.
        """

        if self.current_context.context_type != Context.COMPONENT_TYPE:
            raise ParseError('Exposure names can only be defined in ' +
                             'a component type')
        
        if 'name' in node.attrib:
            self.current_context.add_exposure(node.attrib['name'])

    def parse_fixed(self, node):
        """
        Parses <Fixed>

        @param node: Node containing the <Fixed> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when
        """

        try:
            parameter = node.attrib['parameter']
        except:
            raise ParseError('Parameter to be fixed must be specified')

        try:
            value = node.attrib['value']
        except:
            raise ParseError('Value to be fixed must be specified')

        if self.current_context.lookup_parameter(parameter) == None:
            self.current_context.add_parameter(Parameter(
                parameter, '__dimension_inherited__'))
        self.current_context.lookup_parameter(parameter).fix_value(value)

    def parse_include(self, node):
        """
        Parses <Include>

        @param node: Node containing the <Include> element
        @type node: xml.etree.Element
        """

        if 'file' not in node.attrib:
            raise ParseError('Include file must be specified.')

        path = self.base_path + '/' + node.attrib['file']

        root = xml.parse(path).getroot()
        xmltolower(root)

        self.parse_root(root)

    def parse_link(self, node):
        """
        Parses <Link>

        @param node: Node containing the <Link> element
        @type node: xml.etree.Element
        """

        pass

    def parse_on_condition(self, node):
        """
        Parses <OnCondition>

        @param node: Node containing the <OnCondition> element
        @type node: xml.etree.Element
        """

        if self.current_regime == None:
            raise ParseError('<OnCondition must be defined inside a ' +
                             'behavior profile or regime')

        if 'test' in node.attrib:
            test = node.attrib['test']
        else:
            raise ParseError('Test expression not provided for <OnCondition>')

        event_handler = OnCondition(test)
        
        self.current_event_handler = event_handler
        self.current_regime.add_event_handler(event_handler)
        
        self.process_nested_tags(node)
        
        self.current_event_handler = None
        
    def parse_on_event(self, node):
        """
        Parses <OnEvent>

        @param node: Node containing the <OnEvent> element
        @type node: xml.etree.Element
        """

        self.process_nested_tags(node)

    def parse_on_start(self, node):
        """
        Parses <OnStart>

        @param node: Node containing the <OnStart> element
        @type node: xml.etree.Element
        """

        self.process_nested_tags(node)

    def parse_parameter(self, node):
        """
        Parses <Parameter>

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

        self.current_context.add_parameter(parameter)

    def parse_path(self, node):
        """
        Parses <Path>

        @param node: Node containing the <Path> element
        @type node: xml.etree.Element
        """

        pass

    def parse_record(self, node):
        """
        Parses <Record>

        @param node: Node containing the <Record> element
        @type node: xml.etree.Element
        """

        pass

    def parse_requirement(self, node):
        """
        Parses <Requirement>

        @param node: Node containing the <Requirement> element
        @type node: xml.etree.Element
        """

        pass

    def parse_run(self, node):
        """
        Parses <Run>

        @param node: Node containing the <Run> element
        @type node: xml.etree.Element
        """

        if self.current_regime == None:
            raise ParseError('<StateVariable> must be defined inside a ' +
                             'behavior profile or regime')

        if 'component' in node.attrib:
            component = node.attrib['component']
        else:
            raise ParseError('<Run> must specify a target component')

        if 'variable' in node.attrib:
            variable = node.attrib['variable']
        else:
            raise ParseError('<Run> must specify a state variable')

        if 'increment' in node.attrib:
            increment = node.attrib['increment']
        else:
            raise ParseError('<Run> must specify an increment for the ' +
                             'state variable')

        if 'total' in node.attrib:
            total = node.attrib['total']
        else:
            raise ParseError('<Run> must specify a final value for the ' +
                             'state variable')

        self.current_regime.add_run(component, variable, increment, total)
            
    def parse_show(self, node):
        """
        Parses <Show>

        @param node: Node containing the <Show> element
        @type node: xml.etree.Element
        """

        pass
 
    def parse_state_assignment(self, node):
        """
        Parses <StateAssignment>

        @param node: Node containing the <StateAssignment> element
        @type node: xml.etree.Element
        """

        if self.current_event_handler == None:
            raise ParseError('<StateAssignment> must be defined inside an ' +
                             'event handler in a behavior profile or regime')

        if 'variable' in node.attrib:
            variable = node.attrib['variable']
        else:
            raise ParseError('\'variable\' attribute not provided for ' +
                             '<StateAssignment>')

        if 'value' in node.attrib:
            value = node.attrib['value']
        else:
            raise ParseError('\'value\' attribute not provided for ' +
                             '<StateAssignment>')

        action = StateAssignment(variable, value)

        self.current_event_handler.add_action(action)
        
        
    def parse_state_variable(self, node):
        """
        Parses <StateVariable>

        @param node: Node containing the <StateVariable> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the state variable is not
        being defined in the context of a component type.
        """

        if self.current_regime == None:
            raise ParseError('<StateVariable> must be defined inside a ' +
                             'behavior profile or regime')

        if 'name' in node.attrib:
            name = node.attrib['name']
        else:
            raise ParseError('A state variable must have a name')

        if 'exposure' in node.attrib:
            exposure = node.attrib['exposure']
        else:
            exposure = None

        if 'dimension' in node.attrib:
            dimension = node.attrib['dimension']
        else:
            raise ParseError('A state variable must have a dimension')

        self.current_regime.add_state_variable(name, exposure, dimension)
            
    def parse_time_derivative(self, node):
        """
        Parses <TimeDerivative>

        @param node: Node containing the <TimeDerivative> element
        @type node: xml.etree.Element

        @raise ParseError: Raised when the time derivative is not
        being defined in the context of a component type.
        """

        if self.current_regime == None:
            raise ParseError('<TimeDerivative> must be defined inside a ' +
                             'behavior profile or regime')

        if self.current_context.context_type != Context.COMPONENT_TYPE:
            raise ParseError('Time derivatives can only be defined in ' +
                             'a component type')

        if 'variable' in node.attrib:
            name = node.attrib['variable']
        else:
            raise ParseError('The state variable being differentiated wrt time' +
                             ' must be specified')

        if 'value' in node.attrib:
            value = node.attrib['value']
        else:
            raise ParseError('The time derivative expression must be provided')

        self.current_regime.add_time_derivative(name, value)

    def parse_text(self, node):
        """
        Parses <Text>

        @param node: Node containing the <Text> element
        @type node: xml.etree.Element
        """

        pass

    def parse_unit(self, node):
        """
        Parses <Unit>

        @param node: Node containing the <Unit> element
        @type node: xml.etree.Element

        @raise ParseError: When the name is not a string or the unit
        specfications are incorrect.

        @raise ModelError: When the unit refers to an undefined dimension.
        """

        try:
            symbol = node.attrib['symbol']
            dimension = node.attrib['dimension']
        except:
            raise ParseError('Unit must have a symbol and dimension.')

        if 'powten' in node.attrib:
            pow10 = int(node.attrib['powten'])
        else:
            pow10 = 0

        self.model.add_unit(Unit(symbol, dimension, pow10))
    
    def parse_root(self, node):
        """
        Parse the <lems> (root) element of a LEMS file
        
        @param node: Node containing the <LEMS> element
        @type node: xml.etree.Element
        """
        
        if node.tag.lower() != 'lems':
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
        
        self.base_path = os.path.dirname(filename)
        if self.base_path == '':
            self.base_path = '.'

        context = Context(self.current_context)
        if self.model.context == None:
            self.model.context = context

        self.push_context(context)

        self.parse_root(root)

        self.pop_context()


    def parse_string(self, str):
        pass

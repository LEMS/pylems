"""
Expression parser

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase
from pylems.base.errors import ParseError
from pylems.base.util import Stack

class ExprNode(PyLEMSBase):
    """
    Base class for a node in the expression parse tree.
    """
    
    OP = 1
    VALUE = 2

    def __init__(self, type):
        """
        Constructor.

        @param type: Node type
        @type type: enum(ExprNode.OP, ExprNode.VALUE)
        """
        
        self.type = type
        """ Node type.
        @type: enum(ExprNode.OP, ExprNode.VALUE) """
        
class ValueNode(ExprNode):
    """
    Value node in an expression parse tree. This will always be a leaf node.
    """
    
    def __init__(self, value):
        """
        Constructor.
        
        @param value: Value to be stored in this node.
        @type value: string
        """
        
        ExprNode.__init__(self, ExprNode.VALUE)
        self.value = value
        """ Value to be stored in this node.
        @type: string """
        
    def __str__(self):
        """
        Generates a string representation of this node.
        """
        
        return self.value
        
class OpNode(ExprNode):
    """
    Operation node in an expression parse tree. This will always be a non-leaf
    node.
    """
    
    def __init__(self, op, left, right):
        """
        Constructor.
        
        @param op: Operation to be stored in this node.
        @type op: string

        @param left: Left operand.
        @type left: pylems.parser.expr.ExprNode

        @param right: Right operand.
        @type right: pylems.parser.expr.ExprNode
        """
        
        ExprNode.__init__(self, ExprNode.OP)
        
        self.op = op
        """ Operation stored in this node.
        @type: string """

        self.left = left
        """ Left operand.
        @type: pylems.parser.expr.ExprNode """

        self.right = right
        """ Right operand.
        @type: pylems.parser.expr.ExprNode """

    def __str__(self):
        """
        Generates a string representation of this node.
        """
        
        return '(' + self.op + ' ' + str(self.left) + ' ' + str(self.right) +')'
    
class ExprParser(PyLEMSBase):
    """
    Parser class for parsing an expression and generating a parse tree.
    """
    
    op_priority = {
        '$':-5,
        
        '+':1,
        '-':1,
        '*':2,
        '/':2,
        '^':3,

        '.and.':1,
        '.or.':1,
        '.gt.':2,
        '.ge.':2,
        '.lt.':2,
        '.le.':2,
        '.eq.':2,
        '.ne.':2}
    
    """ Dictionary mapping operators to their priorities.
    @type: dict(string -> Integer) """
    
    def __init__(self, parse_string):
        """
        Constructor.

        @param parse_string: Expression to be parsed.
        @type parse_string: string
        """
        
        self.parse_string = parse_string
        """ Expression to be parsed.
        @type: string """
        
        self.token_list = None
        """ List of tokens from the expression to be parsed.
        @type: list(string) """

    def is_op(self, str):
        """
        Checks if a token string contains an operator.

        @param str: Token string to be checked.
        @type str: string

        @return: True if the token string contains an operator.
        @rtype: Boolean
        """
        
        return str in self.op_priority
    
    def is_sym(self, str):
        """
        Checks if a token string contains a symbol.

        @param str: Token string to be checked.
        @type str: string

        @return: True if the token string contains a symbol.
        @rtype: Boolean
        """
        
        return str in ['+', '-', '*', '/', '^', '(', ')']
    
    def tokenize(self):
        """
        Tokenizes the string stored in the parser object into a list
        of tokens.
        """
        
        self.token_list = []
        ps = self.parse_string.strip()

        i = 0
        while i < len(ps):
            s = ''

            while ps[i].isspace():
                i += 1

            if ps[i].isalpha():
                while i < len(ps) and ps[i].isalnum():
                    s += ps[i]
                    i += 1
            elif ps[i] == '.':
                if ps[i+1].isdigit():
                    while i < len(ps) and (ps[i].isdigit() or ps[i] == '.'):
                        s += ps[i]
                        i += 1
                else:
                    while i < len(ps) and (ps[i] == '.' or ps[i].isalnum()):
                        s += ps[i]
                        i += 1
            else:
                s += ps[i]
                i += 1

            self.token_list += [s]

    def parse_token_list_rec(self):
        """
        Parses a tokenized arithmetic expression into a parse tree. It calls
        itself recursively to handle bracketed subexpressions.

        @return: Returns a token string.
        @rtype: pylems.parser.expr.ExprNode

        @attention: Does not handle unary minuses at the moment. Needs to be
        fixed.
        """
        
        op_stack = Stack()
        val_stack = Stack()
        node_stack = Stack()
        
        op_stack.push('$')
        val_stack.push('$')

        exit_loop = False

        while self.token_list and not exit_loop:
            token = self.token_list[0]
            self.token_list = self.token_list[1:]
            
            if token == '(':
                node_stack.push(self.parse_token_list_rec())
                val_stack.push('$')
            elif self.is_op(token):
                if self.op_priority[op_stack.top()] >= self.op_priority[token]:
                    rval = val_stack.pop()
                    lval = val_stack.pop()
                    op = op_stack.pop()

                    if lval == '$':
                        left = node_stack.pop()
                    else:
                        left = ValueNode(lval)

                    if rval == '$':
                        right = node_stack.pop()
                    else:
                        right = ValueNode(rval)
                
                    node_stack.push(OpNode(op, left, right))
                    val_stack.push('$')
                    
                op_stack.push(token)
            elif token == ')':
                exit_loop = True
            else:
                val_stack.push(token)
                
        rval = val_stack.pop()
        if rval == '$':
            right = node_stack.pop()
        else:
            right = ValueNode(rval)
            
        while op_stack.top() != '$':
            lval = val_stack.pop()
            if lval == '$':
                left = node_stack.pop()
            else:
                left = ValueNode(lval)

            op = op_stack.pop()

            right = OpNode(op, left, right)
        return right

    def parse(self):
        """
        Tokenizes and parses an arithmetic expression into a parse tree.

        @return: Returns a token string.
        @rtype: pylems.parser.expr.ExprNode
        """
        
        self.tokenize()
        return self.parse_token_list_rec()

    def __str__(self):
        return str(self.token_list)

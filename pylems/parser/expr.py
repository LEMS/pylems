"""
Expression parser

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from pylems.base.base import PyLEMSBase

class stack():
    def __init__(self):
        self.st = []
        
    def push(self, val):
        self.st = [val] + self.st

    def pop(self):
        val = self.st[0]
        self.st = self.st[1:]
        return val

    def top(self):
        return self.st[0]

    def is_empty(self):
        return self.st == []

    def __str__(self):
        if len(self.st) == 0:
            s = '[]'
        else:
            s = '[' + str(self.st[0])
            for i in range(1, len(self.st)):
                s += ', ' + str(self.st[i])
            s += ']'
        return s

class ExprNode(PyLEMSBase):
    OP = 1
    VALUE = 2

    def __init__(self, type):
        self.type = type
        
class ValueNode(ExprNode):
    def __init__(self, value):
        ExprNode.__init__(self, ExprNode.VALUE)
        
        self.value = value

    def __str__(self):
        return self.value
        
class OpNode(ExprNode):
    def __init__(self, op, left, right):
        ExprNode.__init__(self, ExprNode.OP)
        
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return '(' + self.op + ' ' + str(self.left) + ' ' + str(self.right) +')'
    
class ExprParser(PyLEMSBase):
    parse_string = None

    token_list = None

    op_priority = {
        '$':-5,
        '+':1,
        '-':1,
        '*':2,
        '/':2,
        '^':3,
        '(':4}
    
    def __init__(self, parse_string):
        self.parse_string = parse_string

    def is_op(self, str):
        return str in ['+', '-', '*', '/', '^']
    
    def is_sym(self, str):
        return str in ['+', '-', '*', '/', '^', '(', ')']
    
    def tokenize(self):
        self.token_list = []
        ps = self.parse_string.strip()
        print ps
        i = 0
        while i < len(ps):
            s = ''

            if ps[i].isalpha():
                while i < len(ps) and ps[i].isalnum():
                    s += ps[i]
                    i += 1
            elif ps[i].isdigit() or ps[i] == '.':
                while i < len(ps) and (ps[i].isdigit() or ps[i] == '.'):
                    s += ps[i]
                    i += 1
            else:
                s += ps[i]
                i += 1

            self.token_list += [s]

    def parse_token_list_rec(self):
        op_stack = stack()
        val_stack = stack()
        node_stack = stack()
        
        op_stack.push('$')
        val_stack.push('$')

        exit_loop = False

        print self.token_list

        while self.token_list and not exit_loop:
            token = self.token_list[0]
            self.token_list = self.token_list[1:]
            
            print '%%%', token, op_stack, val_stack, str(node_stack)

            if token == '(':
                node_stack.push(self.parse_token_list_rec())
                val_stack.push('$')
            elif self.is_op(token):
                if self.op_priority[op_stack.top()] >= self.op_priority[token]:
                    rval = val_stack.pop()
                    lval = val_stack.pop()
                    op = op_stack.pop()

                    print '###', lval, op, rval

                    if lval == '$':
                        left = node_stack.pop()
                    else:
                        left = ValueNode(lval)

                    if rval == '$':
                        right = node_stack.pop()
                    else:
                        right = ValueNode(rval)
                
                    node_stack.push(OpNode(op, left, right))
                    print '###', node_stack
                    val_stack.push('$')
                    
                op_stack.push(token)
            elif token == ')':
                #right = ValueNode(val_stack.top())
                exit_loop = True
            else:
                val_stack.push(token)

            
        while op_stack.top() != '$':
            rval = val_stack.pop()
            if rval == '$':
                right = node_stack.pop()
            else:
                right = ValueNode(rval)
                
            lval = val_stack.pop()
            if lval == '$':
                left = node_stack.pop()
            else:
                left = ValueNode(lval)

            op = op_stack.pop()
            
            node_stack.push(OpNode(op, left, right))
            val_stack.push('$')

        return node_stack.top()

    def parse(self):
        self.tokenize()
        return self.parse_token_list_rec()

    def __str__(self):
        return str(self.token_list)

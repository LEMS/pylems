'''
Unit tests for Parser

'''


from lems.parser.expr import ExprParser

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    

class TestParser(unittest.TestCase):


    def test_parser(self):
        
        x = 0.5
        
        exprs = {}
        #exprs['x'] = '{x}'
        #exprs['exp(v*2)'] = '(exp (* {v} {2}))'
        #exprs['exp(-x)'] = '(exp (- {0} {x}))'
        #exprs['sin(y)'] = '(sin {y})'
        exprs['a / b'] = '(/ {a} {b})'
        exprs['a / (b)'] = '(/ {a} {b})'
        #exprs['a / b * c'] = '(* (/ {a} {b}) {c})'
        #exprs['a / b * (c)'] = '(* (/ {a} {b}) {c})'
        #exprs['a / (b) * c'] = '(* (/ {a} {b}) {c})'
        
        #exprs['(2.64 - 2.52/(1.0 + (exp ((V+120)/(-25)))))'] = '(- {2.64} (/ {2.52} (+ {1.0} (exp (/ (+ {V} {120}) (- {0} {25}))))))'
        #3 / (1.0 + (exp (x)))*(+ 1.0/(1.0 + (exp ((V+34.9)/3.6))))
        #(1.34 / (1.0 + (exp ((V + 62.9)/(-10)))) * (1.5 + 1.0/(1.0 + (exp ((V+34.9)/3.6)))))
        #exprs['1.34 / (4) * (4)'] = 'xx'
        
        for expr in exprs.keys():
            self.parse_expr(expr, exprs[expr])
        
    def parse_expr(self, expr, val):
        
        print('\n------  Parsing %s, checking against %s'%(expr, val))
        ep = ExprParser(expr)
        pt = ep.parse()
        print("%s == %s ??"%(pt, val))
        assert str(pt) == val
        



if __name__ == '__main__':
    tp = TestParser()
    tp.test_parser()
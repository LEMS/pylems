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
        exprs['x'] = '{x}'
        exprs['a + (b + c) * d'] = '(+ {a} (* (+ {b} {c}) {d}))'
        exprs['(43.4 - 42.6/(1.0 + (exp ((V + 68.1)/(-20.5)))))'] = '(- {43.4} (/ {42.6} (+ {1.0} (exp (/ (+ {V} {68.1}) (- {0} {20.5}))))))'
        #          (((0.04 * ((v ^ 2) / MVOLT)) + (((5 * v) + ((140.0 - U) + ISyn)) * MVOLT)) / MSEC)
        
        all = False
        all = True
        
        if all:
            
            exprs['1 + (exp(x))'] = '(+ {1} (exp {x}))'
            exprs['exp(x)'] = '(exp {x})'
            exprs['x / y * z']   = '(* (/ {x} {y}) {z})'
            exprs['x / (y) * z'] = '(* (/ {x} {y}) {z})'
            exprs['(y - z) + t'] = '(+ (- {y} {z}) {t})'
            exprs['x + (y) - z'] = '(- (+ {x} {y}) {z})'
            exprs['exp(v*2)'] = '(exp (* {v} {2}))'
            exprs['exp(-x)'] = '(exp (- {0} {x}))'
            exprs['sin(y)'] = '(sin {y})'
            exprs['a / b'] = '(/ {a} {b})'
            exprs['a / (b)'] = '(/ {a} {b})'

            exprs['(2.64 - 2.52/(1.0 + (exp ((V+120)/(-25)))))'] = '(- {2.64} (/ {2.52} (+ {1.0} (exp (/ (+ {V} {120}) (- {0} {25}))))))'
      
            exprs['(1.34 / (1.0 + (exp ((V + 62.9)/(-10)))) * (1.5 + 1.0/(1.0 + (exp ((V+34.9)/3.6)))))'] = '(* (/ {1.34} (+ {1.0} (exp (/ (+ {V} {62.9}) (- {0} {10}))))) (+ {1.5} (/ {1.0} (+ {1.0} (exp (/ (+ {V} {34.9}) {3.6}))))))'
   
        
        for expr in exprs.keys():
            self.parse_expr(expr, exprs[expr])
        
    def parse_expr(self, expr, val):
        
        print('\n---  Parsing %s, checking against %s'%(expr, val))
        ep = ExprParser(expr)
        pt = ep.parse()
        print("Expr:       %s "%expr)
        print("Parsed as:  %s "%(str(pt)))
        print("Expected :  %s "%(val))
        print("Math :      %s "%(pt.to_python_expr()))
        assert str(pt) == val
        print("Success")
        



if __name__ == '__main__':
    tp = TestParser()
    tp.test_parser()
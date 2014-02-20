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
        exprs['exp(x)'] = '(exp {x})'
        
        all = False
        all = True
        
        if all:
            
            exprs['(R * temperature / (zCa * F)) * log(caConcExt / caConc)'] = '(* (/ (* {R} {temperature}) (* {zCa} {F})) (log (/ {caConcExt} {caConc})))'
            exprs['( (V - ((V^3) / 3)) - W + I) / SEC'] = '(/ (+ (- (- {V} (/ (^ {V} {3.0}) {3.0})) {W}) {I}) {SEC})'
            exprs['(V - (V^3) / 3 - W + I) / SEC']      = '(/ (- {V} (+ (- (/ (^ {V} {3.0}) {3.0}) {W}) {I})) {SEC})'
            exprs['120+300'] = '(+ {120.0} {300.0})'
            exprs['12e-22'] = '{1.2e-21}'
            exprs['1e+22'] = '{1e+22}'
            exprs['1-1E+2+2'] = '(+ (- {1.0} {100.0}) {2.0})'
            exprs['5.0E-11'] = '{5e-11}'
            exprs['a + (b + c) * d'] = '(+ {a} (* (+ {b} {c}) {d}))'
            exprs['1 + (exp(x))'] = '(+ {1.0} (exp {x}))'
            exprs['exp(x)'] = '(exp {x})'
            exprs['x / y * z']   = '(* (/ {x} {y}) {z})'
            exprs['x / (y) * z'] = '(* (/ {x} {y}) {z})'
            exprs['(y - z) + t'] = '(+ (- {y} {z}) {t})'
            exprs['x + (y) - z'] = '(- (+ {x} {y}) {z})'
            exprs['exp(v*2)'] = '(exp (* {v} {2.0}))'
            exprs['exp(-x)'] = '(exp (- {0.0} {x}))'
            exprs['sin(y)'] = '(sin {y})'
            exprs['a / b'] = '(/ {a} {b})'
            exprs['a / (b)'] = '(/ {a} {b})'
            
            exprs['(120 + 300/( (exp ((V + 55)/9)) + (exp ((V + 65)/(-16)))))'] = '(+ {120.0} (/ {300.0} (+ (exp (/ (+ {V} {55.0}) {9.0})) (exp (/ (+ {V} {65.0}) (- {0.0} {16.0}))))))'
        
            exprs['(43.4 - 42.6/(1.0 + (exp ((V + 68.1)/(-20.5)))))'] = '(- {43.4} (/ {42.6} (+ {1.0} (exp (/ (+ {V} {68.1}) (- {0.0} {20.5}))))))'

            exprs['(2.64 - 2.52/(1.0 + (exp ((V+120)/(-25)))))'] = '(- {2.64} (/ {2.52} (+ {1.0} (exp (/ (+ {V} {120.0}) (- {0.0} {25.0}))))))'
      
            exprs['(1.34 / (1.0 + (exp ((V + 62.9)/(-10)))) * (1.5 + 1.0/(1.0 + (exp ((V+34.9)/3.6)))))'] = '(* (/ {1.34} (+ {1.0} (exp (/ (+ {V} {62.9}) (- {0.0} {10.0}))))) (+ {1.5} (/ {1.0} (+ {1.0} (exp (/ (+ {V} {34.9}) {3.6}))))))'
   
        for expr in exprs.keys():
            self.parse_expr(expr, exprs[expr])
            
            
        bad_exprs = {}
        bad_exprs['exxp(x)'] = '(exxp {x})'
        bad_exprs['ln(x)'] = '(ln {x})'  # Use log instead!!
        
        for expr in bad_exprs.keys():
            self.parse_expr(expr, bad_exprs[expr], True)
        
    def parse_expr(self, expr, val, should_fail=False):
        
        print('\n---  Parsing %s, checking against %s'%(expr, val))
        ep = ExprParser(expr)
        try:
            pt = ep.parse()
            print("Expr:       %s "%expr)
            print("Parsed as:  %s "%(str(pt)))
            print("Expected :  %s "%(val))
            print("Math :      %s "%(pt.to_python_expr()))

            assert str(pt) == val
            print("Success")
        except Exception as e:
            if not should_fail:
                print("Exception thrown %s"%e)
                assert 1==2 
            else:
                print("Successfully failed")
        



if __name__ == '__main__':
    
    TestParser.test_parser(None)

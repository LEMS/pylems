#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from pylems.parser.lems import LEMSParser
from pylems.base.errors import ParseError,ModelError

from pylems.parser.expr import ExprParser

#p = ExprParser('1-(95+.3)*v/(60+40)')
p = ExprParser('1+2*(3-5)-4')
print p.parse()

sys.exit(0)

model_file = sys.argv[1]

parser = LEMSParser()
parser.init_parser()

try:
    #parser.parse_file(model_file)
    pass
except ParseError as e:
    print e
except ModelError as e:
    print e
except Exception as e:
    print type(e)
    print e

parser.parse_file(model_file)
print '\n\nModel settings'
print parser.get_model()

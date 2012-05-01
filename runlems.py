#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from pylems.base.errors import ParseError,ModelError
from pylems.parser.lems import LEMSParser
from pylems.sim.build import SimulationBuilder

from pylems.parser.expr import ExprParser

#print ExprParser('1').parse()
#print ExprParser('1 + 2').parse()
#print ExprParser('v .gt. threshold').parse()
#sys.exit(0)

model_file = sys.argv[1]

parser = LEMSParser()
parser.init_parser()
parser.parse_file(model_file)

model = parser.get_model()
print 'Resolving model'
model.resolve_model()
print model

print 'Building simulation'
sim = SimulationBuilder(model).build()


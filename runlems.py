#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from pylems.base.errors import ParseError,ModelError,SimBuildError,SimError
from pylems.parser.lems import LEMSParser
from pylems.sim.build import SimulationBuilder

#from pylems.parser.expr import ExprParser

#print ExprParser('1').parse()
#print ExprParser('1 + 2').parse()
#print ExprParser('v .gt. threshold').parse()
#print ExprParser('1-95*v/100').parse()
#sys.exit(0)

if len(sys.argv) == 1:
    print 'Usage: runlems <model-file>'
    
model_file = sys.argv[1]

try:
    print 'Parsing model file'
    parser = LEMSParser()
    parser.init_parser()
    parser.parse_file(model_file)
    model = parser.get_model()
    
    print 'Resolving model'
    model.resolve_model()
    print model

    print 'Building simulation'
    sim = SimulationBuilder(model).build()

    print 'Running simulation'
    sim.run()
except ParseError as e:
    print 'Caught ParseError - ' + str(e)
except ModelError as e:
    print 'Caught ModelError - ' + str(e)
except SimBuildError as e:
    print 'Caught SimBuildError - ' + str(e)
except SimError as e:
    print 'Caught SimError - ' + str(e)

#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from lems.base.errors import ParseError,ModelError,SimBuildError,SimError
from lems.parser.LEMS import LEMSParser
from lems.sim.build import SimulationBuilder

#from pylems.parser.expr import ExprParser
#print ExprParser('1').parse()
#print ExprParser('1 + 2').parse()
#print ExprParser('v .gt. threshold').parse()
#print ExprParser('1-95*v_t/100').parse()
#print ExprParser('rate / (1 + exp(-(v - midpoint)/scale))').parse()
#print ExprParser('-1+-exp(a-b)-(c-d)').parse()
#print ExprParser('-1--2').parse()
#print '### {0}'.format(ExprParser('-10').parse())
#sys.exit(0)

if len(sys.argv) not in [2,3]:
    print 'Usage: runlems [-nogui] <model-file>'
    sys.exit(-1)

nogui = False
if len(sys.argv) == 2:
    model_file = sys.argv[1]
else:
    if sys.argv[1] == '-nogui':
        nogui = True
    model_file = sys.argv[2]

try:
    print 'Parsing model file'
    parser = LEMSParser()
    parser.init_parser()
    parser.parse_file(model_file)
    model = parser.get_model()
    #print model
    
    print 'Resolving model'
    model.resolve_model()
    #print model

    print 'Building simulation'
    sim = SimulationBuilder(model).build()

    def print_run(run, offset):
        print offset,run.id
        for rn in run.children:
            r = run.children[rn]
            print_run(r, '  ' + offset)
        if run.array:
            for r in run.array:
                print_run(r, '  ' + offset)

    print 'Runnables:'
    for r in sim.runnables:
        print_run(sim.runnables[r], '')
        
    print 'Running simulation'
    sim.run()
    #sys.exit(0)
    
    if not nogui:
        import matplotlib.pyplot as plt
        import numpy

        print 'Plotting graphs'
        rq = []
        for rn in sim.runnables:
            rq.append(sim.runnables[rn])

        while rq != []:
            runnable = rq[0]
            rq = rq[1:]
            for c in runnable.children:
                rq.append(runnable.children[c])
            if runnable.recorded_variables:
                for variable in runnable.recorded_variables:
                    values = runnable.recorded_variables[variable]
                    x = numpy.empty(len(values))
                    y = numpy.empty(len(values))
                    i = 0
                    for (xv, yv) in values:
                        x[i] = xv
                        y[i] = yv
                        i = i + 1

                    p = plt.subplot(111)
                    p.plot(x, y)
        plt.show()


except ParseError as e:
    print 'Caught ParseError - ' + str(e)
except ModelError as e:
    print 'Caught ModelError - ' + str(e)
except SimBuildError as e:
    print 'Caught SimBuildError - ' + str(e)
except SimError as e:
    print 'Caught SimError - ' + str(e)

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

from xml.etree import ElementTree as xml
from lxml import etree as xml2

xsl = xml2.parse('xsl/canonical.xsl')
xslt = xml2.XSLT(xsl)

def xslt_preprocessor_callback(xmltext):
    return str(xslt(xml2.XML(xmltext)))

def print_run(run, offset):
    print('{0}{1} ({2})'.format(offset, run.id, run.component.component_type))
    for rn in run.children:
        r = run.children[rn]
        print_run(r, '  ' + offset)
    if run.array:
        for r in run.array:
            print_run(r, '  ' + offset)

def dump_runnables(sim):
    print('Runnables:')
    for r in sim.runnables:
        print_run(sim.runnables[r], '')


if __name__ == '__main__':

    if len(sys.argv) not in [2,3]:
        print('Usage: runlems [-nogui] <model-file>')
        sys.exit(-1)

    nogui = False
    if len(sys.argv) == 2:
        model_file = sys.argv[1]
    else:
        if sys.argv[1] == '-nogui':
            nogui = True
        model_file = sys.argv[2]

    try:
        print('Parsing model file')
        parser = LEMSParser(xslt_preprocessor_callback)
        parser.parse_file(model_file)
        model = parser.get_model()
        #print model

        print('Resolving model')
        model.resolve_model()
        #print model
        #sys.exit(0)

        print('Building simulation')
        sim = SimulationBuilder(model).build()
        #dump_runnables(sim)
        #sys.exit(0)

        print('Running simulation')
        sim.run()
        #sys.exit(0)

        if not nogui:
            import matplotlib.pyplot as plt
            import numpy

            print('Plotting graphs')
            rq = []
            for rn in sim.runnables:
                rq.append(sim.runnables[rn])

            while rq != []:
                runnable = rq[0]
                rq = rq[1:]
                for c in runnable.children:
                    rq.append(runnable.children[c])
                for child in runnable.array:
                    rq.append(child)
                if runnable.recorded_variables:
                    for variable in runnable.recorded_variables:
                        recording = runnable.recorded_variables[variable]
                        x = numpy.empty(len(recording.values))
                        y = numpy.empty(len(recording.values))
                        i = 0
                        for (xv, yv) in recording.values:
                            x[i] = xv
                            y[i] = yv / recording.numeric_scale
                            i = i + 1

                        p = plt.subplot(111)
                        p.plot(x, y, color=recording.color,label=recording.quantity)
            plt.show()


    except ParseError as e:
        print('Caught ParseError - ' + str(e))
    except ModelError as e:
        print('Caught ModelError - ' + str(e))
        #except SimBuildError as e:
        #print('Caught SimBuildError - ' + str(e))
    except SimError as e:
        print('Caught SimError - ' + str(e))

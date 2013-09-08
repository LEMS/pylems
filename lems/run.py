"""
Command line simulation driver.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import argparse
from pprint import pprint

from lems.model.model import Model
from lems.parser.LEMS import LEMSFileParser
from lems.sim.build import SimulationBuilder
from lems.model.simulation import DataDisplay,DataWriter

#import pylab
import matplotlib.pyplot as pylab
import numpy

from lems.parser.expr import ExprParser as EP

def printsexp(sexp, prefix = '', indent = '||'):
    s = sexp
    i = 0
    l = len(s)

    print('')
    print(prefix, end = '')
    
    while i < l:
        if s[i] == '(':
            s = printsexp(s[(i + 1):], prefix + indent, indent)
            i = 0
            l = len(s)
        elif s[i] == ')':
            #print('')
            return s[(i + 1):]
        elif s[i] == ' ':
            print('')
            print(prefix, end = '')
            i = i + 1
        else:
            print(s[i], end = '')
            i = i + 1

    return ''
    
def main2():
    #expr = 'x'
    #expr = '( (V - ((V^3) / 3)) - W + I) / SEC'
    expr = '(V - (V^3) / 3 - W + I) / SEC'
    sexp = str(EP(expr).parse())
    print(sexp)
    printsexp(sexp)
    
def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-I', type=str,
                        metavar='<Include directory>',
                        action='append',
                        help='Directory to be searched for included files')
    parser.add_argument('-nogui',
                        action='store_true',
                        help="If this is specified, just parse & simulate the model, but don't show any plots")
    parser.add_argument('lems_file', type=str, metavar='<LEMS file>', 
                        help='LEMS file to be simulated')
    
    return parser.parse_args()
    
def main():
    """
    Program entry point.
    """
    
    args = process_args()

    model = Model()
    if args.I is not None:
        for dir in args.I:
            model.add_include_directory(dir)
    model.import_from_file(args.lems_file)

    resolved_model = model.resolve()
    
    ###fn = '/tmp/model2.xml'
    ###model.export_to_file(fn)

    sim = SimulationBuilder(resolved_model).build()
    #sim.dump()
    sim.run()

    process_simulation_output(sim, args)
    
fig_count = 0

def process_simulation_output(sim, options):
    global fig_count
    if not options.nogui:
        print('Processing results')
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
                for recording in runnable.recorded_variables:
                    if isinstance(recording.data_output, DataDisplay):
                        plot_recording(recording)
                    elif isinstance(recording.data_output, DataWriter):
                        save_recording(recording)
                    else:
                        raise Exception("Invalid output type - " + str(type(recording.data_output)))

    if fig_count > 0:
        pylab.show()


displays = {}

def plot_recording(recording):
    global fig_count

    data_output = recording.data_output
    recorder = recording.recorder

    x = numpy.empty(len(recording.values))
    y = numpy.empty(len(recording.values))
    i = 0
    for (xv, yv) in recording.values:
        x[i] = xv / data_output.timeScale
        y[i] = yv / recorder.scale
        i = i + 1

    if data_output.title in displays:
        fig = displays[data_output.title]
    else:
        fig_count = fig_count + 1
        fig = fig_count
        displays[data_output.title] = fig

        f = pylab.figure(fig)
        pylab.title(data_output.title)


    pylab.figure(fig)
    p = pylab.subplot(111)
    p.patch.set_facecolor('#7f7f7f')
    pylab.plot(x, y,
               color=recorder.color,
               label=recorder.quantity)


def save_recording(recording):
    pass

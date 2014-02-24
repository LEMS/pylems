"""
Command line simulation driver.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import argparse

from lems.model.model import Model
from lems.sim.build import SimulationBuilder
from lems.model.simulation import DataDisplay,DataWriter


from lems.parser.expr import ExprParser as EP

dlems_info = "dLEMS (distilled LEMS in JSON format, see https://github.com/borismarin/som-codegen)"

def printsexp(sexp, prefix = '', indent = '||'):
    s = sexp
    i = 0
    l = len(s)

    print('')
    print(prefix,)
    
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
            print(prefix,)
            i = i + 1
        else:
            print(s[i],)
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
                        
                        
    parser.add_argument('lems_file', type=str, metavar='<LEMS file>', 
                        help='LEMS file to be simulated')
                        
    parser.add_argument('-nogui',
                        action='store_true',
                        help="If this is specified, just parse & simulate the model, but don't show any plots")
                        
    parser.add_argument('-dlems',
                        action='store_true',
                        help="If this is specified, export the LEMS file as "+dlems_info)
    
    return parser.parse_args()
    
def main():
    """
    Program entry point.
    """
    
    args = process_args()

    print('Parsing and resolving model: '+args.lems_file)
    model = Model()
    if args.I is not None:
        for dir in args.I:
            model.add_include_directory(dir)
    model.import_from_file(args.lems_file)
    
    resolved_model = model.resolve()
    
    print('Building simulation')
    sim = SimulationBuilder(resolved_model).build()
    #sim.dump("Afterbuild:")

    if args.dlems:
        print('Exporting as: '+dlems_info)
        
        from lems.dlems.exportdlems import export_component
        
        target = model.targets[0]

        sim_comp = model.components[target]

        target_net = sim_comp.parameters['target']

        target_comp = model.components[target_net]
        
        dlems_file_name = args.lems_file.replace('.xml', '.json')
        if dlems_file_name == args.lems_file:
            dlems_file_name = args.lems_file + '.json'

        if target_comp.type == 'network':

            for child in target_comp.children:

                if child.type == 'population':

                    comp =  model.components[child.parameters['component']]

                    export_component(model, comp, sim_comp, child.id, file_name=dlems_file_name)
        else:
            export_component(model, sim_comp, target_comp)
    
    else:
        print('Running simulation')
        sim.run()

        process_simulation_output(sim, args)
    
    
fig_count = 0

def process_simulation_output(sim, options):
    global fig_count

    print('Processing results')
    rq = []
    for rn in sim.runnables:
        rq.append(sim.runnables[rn])

    file_times = {}
    file_outs = {}

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
                    if not options.nogui:
                        plot_recording(recording)
                elif isinstance(recording.data_output, DataWriter):
                    data_output = recording.data_output
                    times = []
                    vals = []
                    for (x,y) in recording.values:
                        times.append(x)
                        vals.append(y)
                    file_times[data_output.file_name] = times
                    if data_output.file_name not in file_outs:
                        file_outs[data_output.file_name] = []
                    file_outs[data_output.file_name].append(vals)
                else:
                    raise Exception("Invalid output type - " + str(type(recording.data_output)))

    for file_out_name in file_times.keys():
        times = file_times[file_out_name]
        vals = file_outs[file_out_name]
        print('Going to save {0}x{1} data points to file {2}'.format(len(times),len(vals),file_out_name))
        file_out = open(data_output.file_name, 'w')
        i=0
        
        for time in times:
           file_out.write('{0}   '.format(time))
           for val in vals:
                file_out.write('{0}   '.format(val[i]))
           file_out.write('\n')
           i += 1


    if fig_count > 0:
        import matplotlib.pyplot as pylab
        pylab.show()


class Display:
    def __init__(self, fig):
        self.fig = fig
        self.plots = list()
        self.legend = list()

displays = {}

def plot_recording(recording):
    
    import matplotlib.pyplot as pylab
    import numpy
    
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
        fig = displays[data_output.title].fig
    else:
        fig_count = fig_count + 1
        fig = fig_count
        displays[data_output.title] = Display(fig)

        f = pylab.figure(fig)
        pylab.title(data_output.title)


    pylab.figure(fig)
    p = pylab.subplot(111)
    p.patch.set_facecolor('#7f7f7f')
    plot, = pylab.plot(x, y,
                      color=recorder.color,
                      label=recorder.quantity)
    displays[data_output.title].plots.append(plot)
    displays[data_output.title].legend.append(recorder.id)
    pylab.legend(displays[data_output.title].plots, displays[data_output.title].legend)





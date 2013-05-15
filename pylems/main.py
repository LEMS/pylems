"""
@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import sys

from xml.etree import ElementTree as xml
from lxml import etree as xml2

from options import Options,parse_cmdline_options

from lems.base.errors import ParseError,ModelError,SimBuildError,SimError
from lems.parser.LEMS import LEMSParser
from lems.sim.build import SimulationBuilder

from lems.model.simulation import DataOutput

import pylab
import numpy

xsl_preprocessor_file = 'canonical.xsl'

def main(argv):
    try:
        options = parse_cmdline_options(argv)
    except Exception as e:
        print("Caught exception when processing command line options: '{0}'".format(
            str(e)))
        sys.exit(-1)

    xsl_pp_cb = make_xsl_preprocessor_callback(options)
    if xsl_pp_cb == None:
        print('Unable to find preprocessor file canonical.xsl. Try using -XI '
              'or -xsl-include to specifiy additional include directories')
        sys.exit(-1)

    for source_file in options.source_files:
        run(source_file, options, xsl_pp_cb)

def make_xsl_preprocessor_callback(options):
    for xsl_include_dir in options.xsl_include_dirs:
        xslpath = xsl_include_dir + '/' + xsl_preprocessor_file
        try:
            xsl = xml2.parse(xslpath)
            xslt = xml2.XSLT(xsl)

            def xsl_pp_cb(xmltext):
                return str(xslt(xml2.XML(xmltext)))

            return xsl_pp_cb

            print xslpath
            break
        except:
            pass

    return None

def run(source_file, options, xsl_pp_cb):
    try:
        print('Parsing model file')
        parser = LEMSParser(xsl_pp_cb, options.include_dirs,
                            ['neuroml'])
        parser.parse_file(source_file)
        model = parser.get_model()
        #print model

        print('Resolving model')
        model.resolve_model()
        #print model

        print('Building simulation')
        sim = SimulationBuilder(model).build()
        #sim.dump()

        print('Running simulation')
        sim.run()

        process_simulation_output(sim, options)

    except ParseError as e:
        print('Caught ParseError - ' + str(e))
    except ModelError as e:
        print('Caught ModelError - ' + str(e))
    except SimBuildError as e:
        print('Caught SimBuildError - ' + str(e))
    except SimError as e:
        print('Caught SimError - ' + str(e))

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
                    if recording.data_output.type == DataOutput.DISPLAY:
                        plot_recording(recording)
                    elif recording.data_output.type == DataOutput.FILE:
                        save_recording(recording)
                    else:
                        raise Exception("Invalid output type")

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
        x[i] = xv
        y[i] = yv / recorder.numeric_scale
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

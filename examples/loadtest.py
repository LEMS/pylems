#! /usr/bin/python


from lems.model.model import Model
from lems.parser.LEMS import LEMSFileParser
from lems.sim.build import SimulationBuilder

model = Model()

model.import_from_file('examples/hhcell.xml')


fn = '/tmp/hhmodel.xml'
model.export_to_file(fn)

print("Written generated LEMS to %s"%fn)

print("Done")

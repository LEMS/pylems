#! /usr/bin/python

from lems.model.model import Model
import sys

model = Model()

file_name = 'examples/hhcell.xml'
#file_name = '../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex0_IaF.xml'
#file_name = '../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex3_Net.xml'
#file_name = '../org.neuroml.import/src/test/resources/BIOMD0000000185_LEMS.xml'

if len(sys.argv) == 2:
    file_name = sys.argv[1] 

model.import_from_file(file_name)

fn = '/tmp/hhmodel.xml'
model.export_to_file(fn)

print("----------------------------------------------")
print(open(fn,'r').read())
print("----------------------------------------------")

print("Written generated LEMS to %s"%fn)

from lems.base.util import validate_lems

validate_lems(fn)

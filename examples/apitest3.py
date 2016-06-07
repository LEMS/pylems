#! /usr/bin/python

import lems.api as lems

model = lems.Model()

model.add(lems.Include("test.xml"))

model.add(lems.Dimension('voltage', m=1, l=3, t=-3, i=-1))
model.add(lems.Dimension('time', t=1))
model.add(lems.Dimension('capacitance', m=-1, l=-2, t=4, i=2))

model.add(lems.Unit('milliVolt', 'mV', 'voltage', -3))
model.add(lems.Unit('milliSecond', 'ms', 'time', -3))
model.add(lems.Unit('microFarad', 'uF', 'capacitance', -12))

iaf1 = lems.ComponentType('iaf1')
model.add(iaf1)

iaf1.add(lems.Parameter('threshold', 'voltage'))
iaf1.add(lems.Parameter('reset', 'voltage'))
iaf1.add(lems.Parameter('refractoryPeriod', 'time'))
iaf1.add(lems.Parameter('capacitance', 'capacitance'))
iaf1.add(lems.Exposure('vexp', 'voltage'))
dp = lems.DerivedParameter('range', 'threshold - reset', 'voltage')
iaf1.add(dp)

iaf1.dynamics.add(lems.StateVariable('v','voltage', 'vexp')) 
iaf1.dynamics.add(lems.DerivedVariable('v2',dimension='voltage', value='v*2'))
cdv = lems.ConditionalDerivedVariable('v_abs','voltage')
cdv.add(lems.Case('v .geq. 0','v'))
cdv.add(lems.Case('v .lt. 0','-1*v'))
iaf1.dynamics.add(cdv)


model.add(lems.Component('celltype_a', iaf1.name))
model.add(lems.Component('celltype_b', iaf1.name, threshold="20mV"))

fn = '/tmp/model.xml'
model.export_to_file(fn)

print("----------------------------------------------")
print(open(fn,'r').read())
print("----------------------------------------------")

print("Written generated LEMS to %s"%fn)

from lems.base.util import validate_lems

validate_lems(fn)

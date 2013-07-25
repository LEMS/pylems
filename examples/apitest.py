#! /usr/bin/python

import lems.api as lems

model = lems.Model()

model.add(lems.Dimension('voltage', m=1, l=3, t=-3, i=-1))
model.add(lems.Dimension('time', t=1))
model.add(lems.Dimension('capacitance', m=-1, l=-2, t=4, i=2))

model.add(lems.Unit('milliVolt', 'mV', 'voltage', -3))
model.add(lems.Unit('milliSecond', 'ms', 'time', -3))
model.add(lems.Unit('microFarad', 'uF', 'capacitance', -12))

iaf1 = lems.ComponentType('iaf1')
model.add(iaf1)

iaf1.add(lems.Parameter('threshold', 'voltage'))
iaf1.add(lems.Parameter('refractoryPeriod', 'time'))
iaf1.add(lems.Parameter('capacitance', 'capacitance'))

model.add(lems.Component('celltype_a', 'iaf1'))
          
model.export_to_file('/tmp/model.xml')


#! /usr/bin/python

import sys

from lems.model.model import Model
from lems.model.dynamics import OnStart
from lems.model.dynamics import OnCondition
from lems.model.dynamics import StateAssignment

from lems.parser.LEMS import LEMSFileParser
from lems.sim.build import SimulationBuilder


import json

def to_si(unit_str):
    return str(model.get_numeric_value(unit_str))

def comp2sign(cond):
    ret = '???'
    if cond in ('gt', 'geq'):
        ret = '+'
    elif cond in ('lt', 'leq'):
        ret = '-'
    elif cond == 'eq':
        ret = '0'
    return ret

def inequality_to_condition(ineq):
    import re
    r = re.compile("(.+)(?:\.([gleqt]+)\.)(.+)")
    s = r.search(ineq)
    expr =  ''.join([s.group(1).strip(), ' - (',  s.group(3).strip() + ')'])
    sign = comp2sign(s.group(2))
    return (expr, sign)

def export_component(comp):
        comp_type = model.component_types[comp.type]

        som = {}
        som['name'] = comp.id
                                
        params = {}

        for p in comp.parameters.keys():
           params[p] = to_si(comp.parameters[p])

        for c in comp_type.constants.keys():
           params[c] = to_si(comp_type.constants[c].value)
                              
        som['parameters']=params

        dyn = comp_type.dynamics

        dvs = {}

        for dv  in dyn.derived_variables:
            if dv.value is not None:
                dvs[dv.name] = dv.value
            else:
                dvs[dv.name] = "0"

        som['state_functions']=dvs

        tds = {}

        for td in dyn.time_derivatives:
            tds[td.variable] = td.value

        som['dynamics']=tds

        svs = {}
        for sv in dyn.state_variables:
            for eh in dyn.event_handlers:
                if isinstance(eh, OnStart):
                    for action in eh.actions:
                        if isinstance(action, StateAssignment):
                            if action.variable == sv.name:
                                svs[sv.name] = action.value
            if not svs.has_key(sv.name): 
                svs[sv.name] = '0'

        som['state']=svs

        evs = []
        count_cond = 0
        
        for eh in dyn.event_handlers:
            if isinstance(eh, OnCondition):
                ev = {}
                ev['name'] = 'condition_%i'%count_cond
                (cond, dir) = inequality_to_condition(eh.test)
                ev['condition'] = cond
                ev['direction'] = dir 
                effect = {}
                state_effects = {}
                for action in eh.actions:
                    if isinstance(action, StateAssignment):
                        state_effects[action.variable] = action.value
                effect['state'] = state_effects
                ev['effect'] = effect
                evs.append(ev)
                count_cond+=1   

        som['events']=evs

  
        som['t_start']='0'
        som['t_end']=to_si(sim_comp.parameters['length'])
        som['dt']=to_si(sim_comp.parameters['step'])

        
                                
        som_file_name = 'comp_%s.json'%comp.id
        som_file = file(som_file_name, 'w')

        som_file.write(json.dumps(som, sort_keys=True,
                  indent=4, separators=(',', ': ')))

        som_file.close()

        print(open(som_file_name,'r').read())

        print "Written to "+som_file_name
    

model = Model()


try:
    lems_file = sys.argv[1] 
except:
    lems_file = '../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex9_FN.xml'

print('Importing LEMS file from: %s'%lems_file)
model.import_from_file(lems_file)

target = model.targets[0]

sim_comp = model.components[target]

target_net = sim_comp.parameters['target']

target_comp = model.components[target_net]

if target_comp.type == 'network':

    for child in target_comp.children:

        if child.type == 'population':

            comp =  model.components[child.parameters['component']]

            export_component(comp)
else:
    export_component(target_comp)
    





#! /usr/bin/python
"""
Exporter for dLEMS (formerly SOM). See https://github.com/borismarin/som-codegen

@author: Boris Marin
"""

import sys
import re
import json
from collections import OrderedDict

from lems.model.model import Model
from lems.sim.build import order_derived_variables, order_derived_parameters
from lems.model.dynamics import OnStart
from lems.model.dynamics import OnCondition
from lems.model.dynamics import StateAssignment

SI_PREF = {'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'c': 1e-2}

def to_si(model, unit_str):
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
    
def has_display(disp, pop):
    pop = re.compile(pop)
    #iterate over plots/dumps pertaining to current element
    quants = [li.parameters['quantity'] for li in disp.children]
    return any([pop.search(q) for q in quants])

    
def any_svs_plotted(disp, svs):
    s = lambda x: x[x.rfind('/')+1:]
    return any([s(li.parameters['quantity']) in svs for li in disp.children])


def inequality_to_condition(ineq):

    r = re.compile("(.+)(?:\.([glneqt]+)\.)(.+)")
    s = r.search(ineq)
    expr =  ''.join([s.group(1).strip(), ' - (',  s.group(3).strip() + ')'])
    sign = comp2sign(s.group(2))
    return (expr, sign)

def export_component(model, comp, sim_comp, parent_pop='', file_name=None):
    
        comp_type = model.component_types[comp.type]

        dlems = OrderedDict()
        dlems['name'] = comp.id
        params = OrderedDict()

        for p in comp.parameters.keys():
            params[p] = to_si(model, comp.parameters[p])

        for p in order_derived_parameters(comp_type):
            params[p] = to_si(model, comp_type.derived_parameters[p])

        for c in comp_type.constants.keys():
            params[c] = to_si(model, comp_type.constants[c].value)
        dlems['parameters']=params

        dyn = comp_type.dynamics
        dvs = OrderedDict()
        for dv in order_derived_variables(dyn):
            val = dyn.derived_variables[dv].value
            if val is not None:
                dvs[dv] = val
            else:
                dvs[dv] = "0"

        dlems['state_functions']=dvs

        tds = OrderedDict()

        for td in dyn.time_derivatives:
            tds[td.variable] = td.value

        dlems['dynamics']=tds

        svs = OrderedDict()
        for sv in dyn.state_variables:
            for eh in dyn.event_handlers:
                if isinstance(eh, OnStart):
                    for action in eh.actions:
                        if isinstance(action, StateAssignment):
                            if action.variable == sv.name:
                                svs[sv.name] = action.value
            if not sv.name in svs: 
                svs[sv.name] = '0'

        dlems['state']=svs

        evs = []
        count_cond = 0
        
        for eh in dyn.event_handlers:
            if isinstance(eh, OnCondition):
                ev = OrderedDict()
                ev['name'] = 'condition_%i'%count_cond
                (cond, dir) = inequality_to_condition(eh.test)
                ev['condition'] = cond
                ev['direction'] = dir 
                effect = OrderedDict()
                state_effects = OrderedDict()
                for action in eh.actions:
                    if isinstance(action, StateAssignment):
                        state_effects[action.variable] = action.value
                effect['state'] = state_effects
                ev['effect'] = effect
                evs.append(ev)
                count_cond+=1   

        dlems['events']=evs

        dlems['t_start'] = '0'
        dlems['t_end'] = to_si(model, sim_comp.parameters['length'])
        dlems['dt'] = to_si(model, sim_comp.parameters['step'])

        disps = []

        for d in sim_comp.children: 

            if d.type == 'Display' and has_display(d, parent_pop) and any_svs_plotted(d, svs.keys()):
                
            
                di = OrderedDict()
                abax = OrderedDict()
                abax['min'] = d.parameters['xmin']
                abax['max'] = d.parameters['xmax']
                
                orax = OrderedDict()
                orax['min'] = d.parameters['ymin']
                orax['max'] = d.parameters['ymax']

                
                curves = []
                for li in d.children:
                    cur = OrderedDict() 
                    s = li.parameters['quantity']
                    x = s[s.rfind('/')+1:]
                    cur['abscissa'] = 't'
                    cur['ordinate'] = x
                    cur['colour'] = li.parameters['color'] 
                    px = re.search('([cmunp])s', li.parameters['timeScale'], re.IGNORECASE)
                    py = re.search('([cmunp])+\w', li.parameters['scale'], re.IGNORECASE)
                    try:
                        scale_x = SI_PREF[px.group()[0]]
                    except (KeyError, AttributeError) as e:
                        scale_x = 1
                    try:
                        scale_y = SI_PREF[py.group()[0]]
                    except (KeyError, AttributeError) as e:
                        scale_y = 1
                    #dlems is currently concerned with state var plots only
                    if cur['ordinate'] in svs:
                        curves.append(cur)
                
                abax = {k: str(scale_x*float(v)) for (k, v) in abax.items()} 
                orax = {k: str(scale_y*float(v)) for (k, v) in orax.items()} 
                di['abscissa_axis'] = abax
                di['ordinate_axis'] = orax

                di['curves'] = curves
                disps.append(di)
                
                
            elif d.type == 'OutputFile':
                dlems['dump_to_file'] = d.parameters['fileName']
                for dd in d.children:
                    s = dd.parameters['quantity']
                
        dlems['display'] = disps

        dlems_file_name = file_name
        if dlems_file_name is None:
            dlems_file_name = 'comp_%s.json'%comp.id
            
        dlems_file = open(dlems_file_name, 'w')

        dlems_file.write(json.dumps(dlems, indent=4, separators=(',', ': ')))

        dlems_file.close()

        print(open(dlems_file_name,'r').read())

        print("Written to %s"%dlems_file_name)
    


if __name__ == '__main__':
    model = Model()

    try:
        lems_file = sys.argv[1] 
    except:
        lems_file = '../NeuroML2/LEMSexamples/LEMS_NML2_Ex9_FN.xml'
        model.add_include_directory('../NeuroML2/NeuroML2CoreTypes')

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

                export_component(model, comp, sim_comp, child.id)
    else:
        export_component(model, target_comp, sim_comp)
    





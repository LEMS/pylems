"""
Base class for runnable components.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.stack import Stack
from lems.base.errors import SimBuildError
from lems.sim.recording import Recording

import ast
import sys

from math import *

#import math

#class Ex1(Exception):
#    pass

#def exp(x):
#    try:
#        return math.exp(x)
#    except Exception as e:
#        print('ERROR performing exp({0})'.format(x))
#        raise Ex1()

class Reflective(LEMSBase):
    
    debug = False
    
    def __init__(self):
        self.instance_variables = []
        self.derived_variables = []
        self.array = []
        self.methods = {}
        #self.total_code_string = '' 

    #@classmethod
    def add_method(self, method_name, parameter_list, statements):
        if statements == []:
            return;
        
        code_string = 'def __generated_function__'
        if parameter_list == []:
            code_string += '():\n'
        else:
            code_string += '(' + parameter_list[0]
            for parameter in parameter_list[1:]:
                code_string += ', ' + parameter
            code_string += '):\n'


        for statement in statements:
            if 'random.uniform' in statement:
                code_string += '    import random\n'
                
        if self.debug:
            code_string += '    if "xxx" in "%s": print("Calling method: %s(), dv: %s, iv: %s")\n'%(method_name,method_name, str(self.derived_variables), str(self.instance_variables))
        if statements == []:
            code_string += '    pass'
        else:
            for statement in statements:
                code_string += '    ' + statement + '\n'

        g = globals()
        l = locals()
        
        #print(code_string.replace('__generated_function__', 
        #                          '{0}.{1}'.format(self.component.type, method_name)))

        if self.debug and statements != []:
            print("------------- %s, %s, %s ----------------"%(method_name, self.id, str(self.derived_variables)))
            print(code_string)
        exec(compile(ast.parse(code_string), '<unknown>', 'exec'), g, l)

        #setattr(cls, method_name, __generated_function__)
        self.__dict__[method_name] = l['__generated_function__']
        del l['__generated_function__']

    def add_instance_variable(self, variable, initial_value):
        self.instance_variables.append(variable)

        code_string = 'self.{0} = {1}\nself.{0}_shadow = {1}'.format(\
            variable, initial_value)
        exec(compile(ast.parse(code_string), '<unknown>', 'exec'))

    def add_derived_variable(self, variable):
        self.derived_variables.append(variable)

        code_string = 'self.{0} = {1}\nself.{0}_shadow = {1}'.format(\
            variable, 0)
        exec(compile(ast.parse(code_string), '<unknown>', 'exec'))

    def add_text_variable(self, variable, value):
        self.__dict__[variable] = value

    def __getitem__(self, key):
        return self.array[key]

    def __setitem__(self, key, val):
        self.array[key] = val

class Regime:
    def __init__(self, name):
        self.name = name
        self.update_state_variables = None
        self.update_derived_variables = None
        self.run_startup_event_handlers = None
        self.run_preprocessing_event_handlers = None
        self.run_postprocessing_event_handlers = None
        self.update_kinetic_scheme = None

class Runnable(Reflective):
    uid_count = 0

    def __init__(self, id_, component, parent = None):
        Reflective.__init__(self)

        self.uid = Runnable.uid_count
        Runnable.uid_count += 1

        self.id = id_
        self.component = component
        self.parent = parent

        self.time_step = 0
        self.time_completed = 0
        self.time_total = 0

        self.plastic = True

        self.state_stack = Stack()

        self.children = {}
        self.uchildren = {}
        self.groups = []

        self.recorded_variables = []

        self.event_out_ports = []
        self.event_in_ports = []

        self.event_out_callbacks = {}
        self.event_in_counters = {}

        self.attachments = {}

        self.new_regime = ''
        self.current_regime = ''
        self.last_regime = ''
        self.regimes = {}
        
        
    def __str__(self):
        return 'Runnable, id: {0} ({1}, {2}), component: ({3})'.format(self.id, self.uid, id(self), self.component)
    
    def __repr__(self):
        return self.__str__()
            

    def add_child(self, id_, runnable):
        self.uchildren[runnable.uid] = runnable
        
        self.children[id_] = runnable
        self.children[runnable.id] = runnable

        self.__dict__[id_] = runnable
        self.__dict__[runnable.id] = runnable

        runnable.configure_time(self.time_step, self.time_total)

        runnable.parent = self

    def add_child_typeref(self, typename, runnable):
        self.__dict__[typename] = runnable

    def add_child_to_group(self, group_name, child):
        #print("add_child_to_group in %s; grp: %s; child: %s "%(self.id, group_name, child))
        if group_name not in self.__dict__:
            #print sorted(self.__dict__.keys())
            self.__dict__[group_name] = []
            self.groups.append(group_name)
        #print sorted(self.__dict__.keys())
        #print ".........."
        #print self.__dict__[group_name]
        # Force group_name attribute to be a list before we append to it.
        if type(self.__dict__[group_name]) is not list:
            self.__dict__[group_name] = [self.__dict__[group_name]]
        self.__dict__[group_name].append(child)
        child.parent = self

    def make_attachment(self, type_, name):
        self.attachments[type_] = name
        self.__dict__[name] = []

    def add_attachment(self, runnable, container = None):
        for ctype in runnable.component.types:
            if ctype in self.attachments:
                name = self.attachments[ctype]
                if container is not None and container != name:
                    continue
                
                if name not in self.__dict__:
                    raise SimBuildError('Cannot attach {0} to {1} in {2}'.format(
                        runnable.id, name, self.id))
                                                                                 
                runnable.id = runnable.id + str(len(self.__dict__[name]))

                self.__dict__[name].append(runnable)
                runnable.parent = self

                return

        raise SimBuildError('Unable to find appropriate attachment for {0} in {1}',
                            runnable.id, self.id)

    def add_event_in_port(self, port):
        self.event_in_ports.append(port)
        if port not in self.event_in_counters:
            self.event_in_counters[port] = 0

    def inc_event_in(self, port):
        self.event_in_counters[port] += 1
        if self.debug: 
            print("\n--- Event in to %s (%s, %s) on port: %s"%(self.id, id(self), self.__class__, port))
            print("EIC (%s): %s"%(id(self),self.event_in_counters))

    def add_event_out_port(self, port):
        self.event_out_ports.append(port)
        if port not in self.event_out_callbacks:
            self.event_out_callbacks[port] = []

    def register_event_out_link(self, port, runnable, remote_port):
        self.event_out_callbacks[port].append((runnable, remote_port))

    def register_event_out_callback(self, port, callback):
        if self.debug: print("register_event_out_callback on %s, port: %s, callback: %s"%(self.id, port, callback))
        if port in self.event_out_callbacks:
            self.event_out_callbacks[port].append(callback)
        else:
            raise SimBuildError('No event out port \'{0}\' in '
                                'component \'{1}\''.format(port, self.id))
        if self.debug: print("EOC: "+str(self.event_out_callbacks))

    def add_regime(self, regime):
        self.regimes[regime.name] = regime

    def resolve_path(self, path):
        if self.debug: print("Resolving path: %s in %s"%(path, self))
        if path == '':
            return self
        if path == 'this':
            return self
        if path[0] == '/':
            return self.parent.resolve_path(path)
        elif path.find('../') == 0:
            return self.parent.resolve_path(path[3:])
        elif path.find('..') == 0:
            return self.parent
        elif path == 'parent':
            return self.parent
        else:
            if path.find('/') >= 1:
                (child, new_path) = path.split('/', 1)
            else:
                child = path
                new_path = ''

            idxbegin = child.find('[')
            idxend = child.find(']')
            if idxbegin != 0 and idxend > idxbegin:
                idx = int(child[idxbegin+1:idxend])
                child = child[:idxbegin]
            else:
                idx = -1

            if child in self.children:
                childobj = self.children[child]
                if idx != -1:
                    childobj = childobj.array[idx]
            elif child in self.component.parameters:
                ctx = self.component
                p = ctx.parameters[child]
                return self.resolve_path('../' + p.value)
            elif child in self.__dict__.keys():
                child_resolved = self.__dict__[child]
                #print("Think it's a link from %s to %s"%(child, child_resolved))
                return self.resolve_path('../' + child_resolved)
            else:
                if self.debug:
                    keys = list(self.__dict__.keys())
                    keys.sort()
                    prefix = "--- "
                    print('{0}    Keys for {1}'.format(prefix, self.id))
                    for k in keys:
                        key_str = str(self.__dict__[k])
                        if len(key_str) > 0 and not key_str == "[]" and not key_str == "{}":
                            print('{0}       {1} -> {2}'.format(prefix, k, key_str))
                        
                raise SimBuildError('Unable to find child \'{0}\' in '
                                    '\'{1}\''.format(child, self.id))

            if new_path == '':
                return childobj
            else:
                return childobj.resolve_path(new_path)

    def add_variable_recorder(self, data_output, recorder):
        self.add_variable_recorder2(data_output, recorder, recorder.quantity, recorder.quantity)

    def add_variable_recorder2(self, data_output, recorder, path, full_path):
        
        if path[0] == '/':
            self.parent.add_variable_recorder2(data_output, recorder, path, full_path)
        elif path.find('../') == 0:
            self.parent.add_variable_recorder2(data_output, recorder, path[3:], full_path)
        elif path.find('/') >= 1:
            (child, new_path) = path.split('/', 1)
            
            if ':' in child:
                syn_parts = child.split(":")
                if syn_parts[0] == 'synapses' and syn_parts[2] == '0':
                    child = syn_parts[1]
                else:
                    raise SimBuildError('Cannot determine what to do with (synapse?) path: %s (full path: %s)'
                                        % (child, full_path))
                
            idxbegin = child.find('[')
            idxend = child.find(']')
            if idxbegin != 0 and idxend > idxbegin:
                idx = int(child[idxbegin+1:idxend])
                child = child[:idxbegin]
            else:
                idx = -1

            if child in self.children:
                childobj = self.children[child]
                if idx == -1:
                    childobj.add_variable_recorder2(data_output,
                                                    recorder,
                                                    new_path,
                                                    full_path)
                else:
                    childobj.array[idx].add_variable_recorder2(data_output,
                                                               recorder,
                                                               new_path,
                                                               full_path)
            elif child in self.component.children:
                cdef = self.component.children[child]
                childobj = None
                for cid in self.children:
                    c = self.children[cid]
                    if cdef.type in c.component.types:
                        childobj = c
                if childobj:
                    childobj.add_variable_recorder2(data_output,
                                                    recorder,
                                                    new_path)
                else:                    
                    raise SimBuildError('Unable to find the child \'{0}\' in '
                                        '\'{1}\''.format(child, self.id))
            else:
                raise SimBuildError('Unable to find a child \'{0}\' in '
                                    '\'{1}\''.format(child, self.id))
        else:
            self.recorded_variables.append(Recording(path, full_path, data_output, recorder))


    def configure_time(self, time_step, time_total):
        self.time_step = time_step
        self.time_total = time_total

        for cn in self.uchildren:
            self.uchildren[cn].configure_time(self.time_step, self.time_total)

        for c in self.array:
            c.configure_time(self.time_step, self.time_total)

        ## for type_ in self.attachments:
        ##     components = self.__dict__[self.attachments[type_]]
        ##     for component in components:
        ##         component.configure_time(self.time_step, self.time_total)


    def reset_time(self):
        self.time_completed = 0

        for cid in self.uchildren:
            self.uchildren[cid].reset_time()

        for c in self.array:
            c.reset_time()

        ## for type_ in self.attachments:
        ##     components = self.__dict__[self.attachments[type_]]
        ##     for component in components:
        ##         component.reset_time()

    def single_step(self, dt):
        #return self.single_step2(dt)

        # For debugging
        try:
            return self.single_step2(dt)
        #except Ex1 as e:
        #    print self.rate
        #    print self.midpoint
        #    print self.scale
        #    print self.parent.parent.parent.parent.v
        #    # rate * exp((v - midpoint)/scale)
        #    sys.exit(0)
        except KeyError as e:
            r = self
            name = r.id
            while r.parent:
                r = r.parent
                name = "{0}.{1}".format(r.id, name)

            print("Error in '{0} ({1})': {2}".format(name,
                                                         self.component.type, 
                                                         e))
            print(e)
            
            prefix = "- "
            if self.instance_variables:
                print('Instance variables'.format(prefix))
                for vn in self.instance_variables:
                    print('{0}      {1} = {2}'.format(prefix, vn, self.__dict__[vn]))
            if self.derived_variables:
                print('{0}    Derived variables'.format(prefix))
                for vn in self.derived_variables:
                    print('{0}      {1} = {2}'.format(prefix, vn, self.__dict__[vn]))
            
            keys = list(self.__dict__.keys())
            keys.sort()
            for k in keys:
                print('{0} -> {1}'.format(k, str(self.__dict__[k])))
            print('')
            print('')

            if isinstance(e, ArithmeticError):
                print(('This is an arithmetic error. Consider reducing the '
                       'integration time step.'))

            sys.exit(0)

    def single_step2(self, dt):
        for cid in self.uchildren:
            self.uchildren[cid].single_step(dt)

        for child in self.array:
            child.single_step(dt)
            
        '''
        Regime transition now happens below...
        if self.new_regime != '':
            self.current_regime = self.new_regime
            self.new_regime = '''''
        
        if getattr(self, "update_kinetic_scheme", None): self.update_kinetic_scheme(self, dt)

        #if self.time_completed == 0:
        #    self.run_startup_event_handlers(self)

        if getattr(self, "run_preprocessing_event_handlers", None): self.run_preprocessing_event_handlers(self)
        if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()

        if getattr(self, "update_derived_variables", None): self.update_derived_variables(self)
        if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()
                
        if getattr(self, "update_state_variables", None): self.update_state_variables(self, dt)
        if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()
        
        #if self.time_completed == 0:
        #    self.update_derived_parameters(self)

        if getattr(self, "run_postprocessing_event_handlers", None): self.run_postprocessing_event_handlers(self)
        if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()

        if False:#self.id == 'hhpop__hhcell__0':
            print('1', self.uid, self.v)
        if False:#self.id == 'reverseRate':
            print('2', self.parent.parent.parent.parent.uid, self.parent.parent.parent.parent.v)

        if self.current_regime != '':
            if self.debug: print("In reg: "+self.current_regime)
            regime = self.regimes[self.current_regime]

            #if getattr(self, "xxx", None): 
            if getattr(regime, "update_kinetic_scheme", None): regime.update_kinetic_scheme(self, dt)

            if getattr(regime, "run_preprocessing_event_handlers", None): regime.run_preprocessing_event_handlers(self)
            if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()

            if getattr(regime, "update_derived_variables", None): regime.update_derived_variables(self)
            if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()

            if getattr(regime, "update_state_variables", None): regime.update_state_variables(self, dt)
            if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()

            if getattr(regime, "run_postprocessing_event_handlers", None): regime.run_postprocessing_event_handlers(self)
            if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()
            
            if self.new_regime != '':
                self.current_regime = self.new_regime
                self.new_regime = ''
                regime = self.regimes[self.current_regime]
                if getattr(regime, "run_preprocessing_event_handlers", None): regime.run_preprocessing_event_handlers(self)
                if getattr(self, "update_shadow_variables", None): self.update_shadow_variables()
                
            if self.debug: print("In reg: "+self.current_regime)
                

        self.record_variables()

        self.time_completed += dt
        if self.time_completed >= self.time_total:
            return 0
        else:
            return dt

    def do_startup(self):
        
        if self.debug and False:
            print("  Doing startup: "+self.id)
            for iv in self.instance_variables: print("%s = %s"%(iv,self.__dict__[iv]))
            for dv in self.derived_variables: print("%s = %s"%(dv,self.__dict__[dv]))
        
        for cid in self.uchildren:
            self.uchildren[cid].do_startup()

        for child in self.array:
            child.do_startup()
        
        #if getattr(self, "xxx", None): 
        if getattr(self, "run_startup_event_handlers", None): self.run_startup_event_handlers(self)
        if getattr(self, "update_derived_parameters", None): self.update_derived_parameters(self)
        
        try:
            if getattr(self, "update_derived_variables", None): self.update_derived_variables(self)
        except Exception as e:
            print("Problem setting initial value of DerivedVariable in %s: %s"%(self.id,e))
            print("Continuing...")
      
        for cid in self.uchildren:
            self.uchildren[cid].do_startup()

        for child in self.array:
            child.do_startup()
             

    def record_variables(self):
        for recording in self.recorded_variables:
            recording.add_value(self.time_completed,
                               self.__dict__[recording.variable])

    def push_state(self):
        vars = []
        for varname in self.instance_variables:
            vars += [self.__dict__[varname],
                     self.__dict__[varname + '_shadow']]
        self.state_stack.push(vars)

        for cid in self.uchildren:
            self.uchildren[cid].push_state()

        for c in self.array:
            c.push_state()

    def pop_state(self):
        vars = self.state_stack.pop()
        for varname in self.instance_variables:
            self.__dict_[varname] = vars[0]
            self.__dict_[varname + '_shadow'] = vars[1]
            vars = vars[2:]

        for cid in self.uchildren:
            self.uchildren[cid].pop_state()

        for c in self.array:
            c.pop_state()

    def update_shadow_variables(self):
        if self.plastic:
            for var in self.instance_variables:
                self.__dict__[var + '_shadow'] = self.__dict__[var]
            for var in self.derived_variables:
                self.__dict__[var + '_shadow'] = self.__dict__[var]

    def __lt__(self, other):
        return self.id < other.id

    def copy(self):
        """
        Make a copy of this runnable.

        @return: Copy of this runnable.
        @rtype: lems.sim.runnable.Runnable
        """
        if self.debug: print("Coping....."+self.id)
        r = Runnable(self.id, self.component, self.parent)
        copies = dict()

        # Copy simulation time parameters
        r.time_step = self.time_step
        r.time_completed = self.time_completed
        r.time_total = self.time_total

        # Plasticity and state stack (?)
        r.plastic = self.plastic
        r.state_stack = Stack()
        
        # Copy variables (GG - Faster using the add_* methods?)
        for v in self.instance_variables:
            r.instance_variables.append(v)
            r.__dict__[v] = self.__dict__[v]
            r.__dict__[v + '_shadow'] = self.__dict__[v + '_shadow']
        
        for v in self.derived_variables:
            r.derived_variables.append(v)
            r.__dict__[v] = self.__dict__[v]
            r.__dict__[v + '_shadow'] = self.__dict__[v + '_shadow']
        
        # Copy array elements
        for child in self.array:
            child_copy = child.copy()
            child_copy.parent = r
            r.array.append(child_copy)
            copies[child.uid] = child_copy
            
        # Copy attachment def
        for att in self.attachments:
            atn = self.attachments[att]
            r.attachments[att] = atn
            r.__dict__[atn] = []

        # Copy children
        for uid in self.uchildren:
            child = self.uchildren[uid]
            child_copy = child.copy()
            child_copy.parent = r
            copies[child.uid] = child_copy
            
            r.add_child(child_copy.id, child_copy)

            # For typerefs
            try:
                idx = [k for k in self.__dict__ if self.__dict__[k] == child][0]
                r.__dict__[idx] = child_copy
            except:
                pass

            # For groups and attachments:
            try:
                idx = [k for k in self.__dict__ if child in self.__dict__[k]][0]
                if idx not in r.__dict__:
                    r.__dict__[idx] = []
                r.__dict__[idx].append(child_copy)

            except:
                pass
               
        # Copy event ports
        for port in self.event_in_ports:
            r.event_in_ports.append(port)
            r.event_in_counters[port] = 0

        for port in self.event_out_ports:
            r.event_out_ports.append(port)
            r.event_out_callbacks[port] = self.event_out_callbacks[port]
        
        for ec in r.component.structure.event_connections:
            if self.debug: print("--- Fixing event_connection: %s in %s"%(ec.toxml(), id(r)))
            
            source = r.parent.resolve_path(ec.from_)
            target = r.parent.resolve_path(ec.to)
            
            if ec.receiver:
                # Will throw error...
                receiver_template = self.build_runnable(ec.receiver, target)                                
                #receiver = copy.deepcopy(receiver_template)
                receiver = receiver_template.copy()
                receiver.id = "{0}__{1}__".format(component.id,
                                                  receiver_template.id)

                if ec.receiver_container:
                    target.add_attachment(receiver, ec.receiver_container)
                target.add_child(receiver_template.id, receiver)
                target = receiver
            else:
                source = r.resolve_path(ec.from_)
                target = r.resolve_path(ec.to)

            source_port = ec.source_port
            target_port = ec.target_port

            if not source_port:
                if len(source.event_out_ports) == 1:
                    source_port = source.event_out_ports[0]
                else:
                    raise SimBuildError(("No source event port "
                                         "uniquely identifiable"
                                         " in '{0}'").format(source.id))
            if not target_port:
                if len(target.event_in_ports) == 1:
                    target_port = target.event_in_ports[0]
                else:
                    raise SimBuildError(("No destination event port "
                                         "uniquely identifiable "
                                         "in '{0}'").format(target))
             
            if self.debug: print("register_event_out_callback\n   Source: %s, %s (port: %s) \n   -> %s, %s (port: %s)"%(source, id(source), source_port, target, id(target), target_port))
            source.register_event_out_callback(\
                source_port, lambda: target.inc_event_in(target_port))
            
        
            

        # Copy methods
        if getattr(self, "update_kinetic_scheme", None): r.update_kinetic_scheme = self.update_kinetic_scheme
        if getattr(self, "run_startup_event_handlers", None): r.run_startup_event_handlers = self.run_startup_event_handlers
        if getattr(self, "run_preprocessing_event_handlers", None): r.run_preprocessing_event_handlers = self.run_preprocessing_event_handlers
        if getattr(self, "run_postprocessing_event_handlers", None): r.run_postprocessing_event_handlers = self.run_postprocessing_event_handlers
        
        if getattr(self, "update_state_variables", None): r.update_state_variables = self.update_state_variables
        if getattr(self, "update_derived_variables", None): r.update_derived_variables = self.update_derived_variables
        #r.update_shadow_variables = self.update_shadow_variables
        if getattr(self, "update_derived_parameters", None): r.update_derived_parameters = self.update_derived_parameters

        for rn in self.regimes:
            r.add_regime(self.regimes[rn])
        r.current_regime = self.current_regime

        # Copy groups
        for gn in self.groups:
            g = self.__dict__[gn]
            for c in g:
                if c.uid in copies:
                    r.add_child_to_group(gn, copies[c.uid])
                else:
                    c2 = c.copy()
                    c2.parent = r
                    copies[c.uid] = c2
                    r.add_child_to_group(gn, c2)
                    

        # Copy remaining runnable references.
        for k in self.__dict__:
            if k == 'parent':
                continue
            c = self.__dict__[k]
            if isinstance(c, Runnable):
                if c.uid in copies:
                    r.__dict__[k] = copies[c.uid]
                else:
                    c2 = c.copy()
                    c2.parent = r
                    copies[c.uid] = c2
                    r.__dict__[k] = c2
           
        # Copy text fields
        for k in self.__dict__:          
            if not k in r.__dict__:
                c = self.__dict__[k]
                if self.debug: print("Adding remaining field: %s = %s"%(k,c))
                r.__dict__[k] = c
                
        if self.debug:
            print('########################################')
            keys = list(self.__dict__.keys())
            keys.sort()
            print(len(keys))
            for k in keys:
                print(k, self.__dict__[k])
            print('----------------------------------------')
            keys = list(r.__dict__.keys())
            keys.sort()
            print(len(keys))
            for k in keys:
                print(k, r.__dict__[k])
            print('########################################')
            print('')
            print('')
            print('')
            print('')
            
        if self.debug: print("Finished coping..."+self.id)
        
        return r

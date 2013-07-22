"""
PyLEMS utility classes / functions

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

id_counter = 0

def make_id():
    global id_counter
    id_counter = id_counter + 1
    return '__id_{0}__'.format(id_counter)

def merge_maps(m, base):
    """
    Merge in undefined map entries from given map.
    
    @param m: Map to be merged into.
    @type m: lems.util.Map
    
    @param base: Map to be merged into.
    @type base: lems.util.Map
    """
    
    for k in base.keys():
        if k not in m:
            m[k] = base[k]

def merge_lists(l, base):
    """
    Merge in undefined list entries from given list.
    
    @param l: List to be merged into.
    @type l: list
    
    @param base: List to be merged into.
    @type base: list
    """
    
    for i in base:
        if i not in l:
            l.append(i)


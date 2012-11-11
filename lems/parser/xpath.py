"""
XPath parser

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.errors import ParseError

import os.path

def split_path(path):
    nesting = 0
    for i in xrange(len(path)):
        if path[i] == '[':
            nesting += 1
        elif path[i] == ']':
            nesting -= 1
        elif path[i] == '/' and nesting == 0:
            return [path[0:i], path[(i + 1):]]

    return [path]

def seperate_predicate(selector):
    sc = selector.count('[')
    ec = selector.count('[')

    if sc == 0 and ec == 0:
        return [selector]
    elif sc == 1 and ec == 1:
        si = selector.index('[')
        ei = selector.index(']')

        return [selector[0:si], selector[(si + 1):ei]]
    else:
        return None

def get_root_ctx(context):
    ctx = context
    while ctx.parent is not None:
        ctx = ctx.parent

    return ctx

def resolve_xpath(xpath, context):
    path = xpath.strip()

    if path[0:2] == '//':
        global_search = True
        path = path[2:]
        ctx = get_root_ctx(context)
    elif path[0] == '/':
        global_search = False
        path= path[1:]
        ctx = get_root_ctx(context)
    else:
        global_search = False
        ctx = context

    bits = split_path(path)
    selector = bits[0]
    path = bits[1] if len(bits) > 1 else None

    bits = seperate_predicate(selector)
    if bits == None:
        raise ParseError("Error parsing XPath expression '{0}'".format(xpath))

    selector = bits[0]
    predicate = bits[1] if len(bits) > 1 else None

    print xpath
    print selector, predicate, path, global_search

    print search_across_model(ctx, selector)

def search_across_model(ctx, name):
    nodes = []

    print ctx.name, name

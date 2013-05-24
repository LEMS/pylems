"""
Dimension and Unit definitions in terms of the fundamental SI units.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

class Dimension(LEMSBase):
    def __init__(self, name, **params):
        self.name = name

        self.m = params['m'] if 'm' in params else 0
        self.l = params['l'] if 'l' in params else 0
        self.t = params['t'] if 't' in params else 0
        self.l = params['l'] if 'l' in params else 0
        self.i = params['i'] if 'i' in params else 0
        self.k = params['k'] if 'k' in params else 0
        self.n = params['n'] if 'n' in params else 0
        self.j = params['j'] if 'j' in params else 0

class Unit(LEMSBase):
    def __init__(self, name, symbol, dimension, power = 0, scale = 0, offset = 0):
        self.name = name
        self.symbol = symbol
        self.dimension = dimension
        self.power = power
        self.scale = scale
        self.offset = offset

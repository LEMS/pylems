#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from pylems.main import main



#main(sys.argv[1:])


#1e-5 * (targetVoltage - v) / seriesResistance | (- {e} (* {5} (/ (- {targetVoltage} {v}) {seriesResistance})))

from lems.parser.expr import ExprParser

#e = ExprParser('1e-5 * (targetVoltage - v) / seriesResistance')
e = ExprParser('1')
print e.parse()


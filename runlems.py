#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from pylems.parser.lems import LEMSParser
from pylems.base.errors import ParseError,ModelError

model_file = sys.argv[1]

parser = LEMSParser()
parser.init_parser()

try:
    parser.parse_file(model_file)
except ParseError as e:
    print e
except ModelError as e:
    print e
except Exception as e:
    print type(e)
    print e
    
print '\n\nModel settings'
#print parser.get_model()

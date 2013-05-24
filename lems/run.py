"""
Command line simulation driver.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import argparse

from lems.api import Model
from lems.parser import LEMSFileParser

def process_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-I', type=str,
                        metavar='<Include directory>',
                        action='append',
                        help='Directory to be searched for included files')
    parser.add_argument('lems_file', type=str, metavar='<LEMS file>', 
                        help='LEMS file to be simulated')
    
    return parser.parse_args()
    
def main():
    args = process_args()

    model = Model()
    parser = LEMSFileParser(model)

    with open(args.lems_file) as f:
        parser.parse(f.read())

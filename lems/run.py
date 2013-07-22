"""
Command line simulation driver.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

import argparse

from lems.model.model import Model
from lems.parser.LEMS import LEMSFileParser
from lems.sim.build import SimulationBuilder

def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-I', type=str,
                        metavar='<Include directory>',
                        action='append',
                        help='Directory to be searched for included files')
    parser.add_argument('lems_file', type=str, metavar='<LEMS file>', 
                        help='LEMS file to be simulated')
    
    return parser.parse_args()
    
def main():
    """
    Program entry point.
    """
    args = process_args()

    model = Model()
    model.import_from_file(args.lems_file)

    resolved_model = model.resolve()

    sim = SimulationBuilder(resolved_model).build()

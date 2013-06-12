#! /usr/bin/env python
"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

import sys
from lems.base.errors import ParseError,ModelError,SimError
from lems.parser.LEMS import LEMSParser

from lxml import etree as xml2

xsl = xml2.parse('xsl/canonical.xsl')
xslt = xml2.XSLT(xsl)

def xslt_preprocessor_callback(xmltext):
    return str(xslt(xml2.XML(xmltext)))



if __name__ == '__main__':

    model_file = "examples/example2.xml"
    if len(sys.argv) == 2:
        model_file = sys.argv[1]


    try:
        print('Parsing model file')
        parser = LEMSParser(xslt_preprocessor_callback)


        ############   Simple reading/printing contents   #######


        parser.parse_file(model_file)
        model = parser.get_model()
        for ct_name in model.context.component_types.keys():
            ct = model.context.component_types[ct_name]
            
            print "-  Found ComponentType: "+ct.name
            for param_name in ct.context.parameters:
                par = ct.context.parameters[param_name]
                print "     %s has dimension: %s"%(param_name, par.dimension)
            if len(ct.context.dynamics_profiles)==1:
                dyn = ct.context.dynamics_profiles['']
                regime = dyn.default_regime
                print "     Dynamics [SV: %s]"%(regime.state_variables)

        print
        for comp_name in model.context.components.keys():
            comp = model.context.components[comp_name]
            print "-  Found Component of type: %s, id: %s"%(comp.component_type,comp.id)
            for param_name in comp.context.parameters:
                par = comp.context.parameters[param_name]
                print "     %s has value: %s"%(param_name, par.value)

        '''  My ideal API...

        model = parser.get_model()
        for ct in model.component_types:

            print "-  Found ComponentType: "+ct.name
            for param in ct.parameters:
                print "     %s has dimension: %s"%(param.name, param.dimension)
            if len(ct.dynamics)==1:
                dyn = ct.dynamics['']
                # Note: default regime could be used for dyn.state_variables etc. (i.e. dyn.default_regime.state_variables)
                print "     Dynamics [SV: %s]"%(dyn.state_variables)

        print
        for comp in model.components:
            print "-  Found Component of type: %s, id: %s"%(comp.component_type,comp.id)
            for param in comp.parameters:
                print "     %s has value: %s"%(param.name, param.value)


        '''




    except ParseError as e:
        print('Caught ParseError - ' + str(e))
    except ModelError as e:
        print('Caught ModelError - ' + str(e))
    except SimError as e:
        print('Caught SimError - ' + str(e))

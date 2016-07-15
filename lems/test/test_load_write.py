"""
Unit tests for loading/writing

"""

from lems.model.model import Model

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    

class TestLoadWrite(unittest.TestCase):


    def test_load_write_xml(self):
        
        model = Model()

        file_name = 'lems/test/hhcell_resaved2.xml'

        model.import_from_file(file_name)

        file_name2 = 'lems/test/hhcell_resaved3.xml'
        model.export_to_file(file_name2)

        print("----------------------------------------------")
        print(open(file_name2,'r').read())
        print("----------------------------------------------")

        print("Written generated LEMS to %s"%file_name2)

        from lems.base.util import validate_lems

        validate_lems(file_name2)
        
    def test_load_get_dom(self):
        
        model = Model()

        file_name = 'lems/test/hhcell_resaved2.xml'

        model.import_from_file(file_name)

        dom0 = model.export_to_dom()
        

        
        
        




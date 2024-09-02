"""
Unit tests for loading/writing

"""

import os
import unittest

from lems.model.model import Model


class TestLoadWrite(unittest.TestCase):
    def test_load_write_xml(self):
        model = Model()
        file_name = "lems/test/hhcell_resaved2.xml"
        model.import_from_file(file_name)
        file_name2 = "lems/test/hhcell_resaved3.xml"
        model.export_to_file(file_name2)

        print("----------------------------------------------")
        print(open(file_name2, "r").read())
        print("----------------------------------------------")

        print("Written generated LEMS to %s" % file_name2)

        from lems.base.util import validate_lems

        validate_lems(file_name2)

    def test_load_get_dom(self):
        model = Model()
        file_name = "lems/test/hhcell_resaved2.xml"
        model.import_from_file(file_name)
        dom0 = model.export_to_dom()

    def test_include_includes_is_true(self):
        """Test that include_includes works as expected"""
        cwd = os.getcwd()
        os.chdir("lems/test/")
        model = Model(
            include_includes=True,
            fail_on_missing_includes=True,
        )
        model.debug = True
        model.add_include_directory("NeuroML2CoreTypes/")

        model.import_from_file("LEMS_NML2_Ex2_Izh.xml")

        model_string = model.export_to_dom().toprettyxml("    ", "\n")
        print(model_string)
        self.assertNotIn("<Include ", model_string)

        self.assertEqual(0, len(model.includes))

        os.chdir(cwd)

    def test_include_includes_is_false(self):
        """Test that include_includes works as expected"""
        cwd = os.getcwd()
        os.chdir("lems/test/")
        model = Model(
            include_includes=False,
            fail_on_missing_includes=True,
        )
        model.debug = True
        model.add_include_directory("NeuroML2CoreTypes/")

        model.import_from_file("LEMS_NML2_Ex2_Izh.xml")

        model_string = model.export_to_dom().toprettyxml("    ", "\n")
        print(model_string)
        self.assertIn("<Include ", model_string)

        for include in model.includes:
            inc_string = include.toxml()
            self.assertIn("<Include file=", inc_string)

        os.chdir(cwd)

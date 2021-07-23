"""
Misc tests.

File: test_misc.py

Copyright 2021 LEMS contributors
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import unittest
import os
from lems.model.model import Model


class TestExposure(unittest.TestCase):

    """Test getting exposures from LEMS models"""

    def test_exposure_getters(self):
        model = Model(include_includes=True, fail_on_missing_includes=True)
        file_name = os.path.dirname(os.path.abspath(__file__)) + '/test_exposure_listing.xml'
        model.import_from_file(file_name)
        exp_list = model.list_exposures()
        for c, es in exp_list.items():
            # iaf1 defines v as an exposure
            if c.id == "example_iaf1_cell":
                self.assertTrue('v' in es)
            # iaf2 extends iaf1 and so should inherit v
            if c.id == "example_iaf2_cell":
                self.assertTrue('v' in es)


if __name__ == '__main__':
    unittest.main()

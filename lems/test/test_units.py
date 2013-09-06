"""
Unit tests for Unit/Dimension handling


"""


from lems.model.fundamental import Dimension,Unit
from lems.model.model import Model

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    

class TestUnitParsing(unittest.TestCase):

    def get_model(self):

        model = Model()

        model.add(Dimension('voltage', m=1, l=3, t=-3, i=-1))
        model.add(Dimension('time', t=1))
        model.add(Dimension('capacitance', m=-1, l=-2, t=4, i=2))
        model.add(Dimension('conductanceDensity', m="-1", l="-4", t="3", i="2"))

        model.add(Unit('milliVolt', 'mV', 'voltage', -3))
        model.add(Unit('milliSecond', 'ms', 'time', -3))
        model.add(Unit('microFarad', 'uF', 'capacitance', -12))
        model.add(Unit('mS_per_cm2', 'mS_per_cm2', 'conductanceDensity', 1))

        return model


    def check_num_val(self, unit_str, val, dimension = None):

        print("Ensuring %s returns %f in dimension %s"%(unit_str, val, dimension))
        val = self.get_model().get_numeric_value(unit_str, dimension)

    def test_parse_units(self):

        self.check_num_val('-60mV', -60)
        self.check_num_val('-60mV', -0.06, 'voltage')
        self.check_num_val('-60', -60)
        self.check_num_val('1.1ms', 1.1)
        self.check_num_val('5E-24', 5E-24)
        self.check_num_val('10.5 mS_per_cm2', 10.5)
        self.check_num_val('10.5 mS_per_cm2', 1.05, 'conductanceDensity')
        self.check_num_val('1.1e-2 ms', 0.011)
        self.check_num_val('1.1e-2 ms', 0.000011, 'time')



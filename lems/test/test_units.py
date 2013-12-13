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
        model.add(Dimension('temperature', k=1))

        model.add(Unit('volt', 'V', 'voltage', 0))
        model.add(Unit('milliVolt', 'mV', 'voltage', -3))
        model.add(Unit('milliSecond', 'ms', 'time', -3))
        model.add(Unit('microFarad', 'uF', 'capacitance', -12))
        model.add(Unit('mS_per_cm2', 'mS_per_cm2', 'conductanceDensity', 1))

        model.add(Unit('Kelvin', 'K', 'temperature', 0))
        model.add(Unit('celsius', 'degC', 'temperature', 0, offset=273.15))
        
        model.add(Unit('hour', 'hour', 'time', scale=3600))
        model.add(Unit('min', 'min', 'time', scale=60))

        return model


    def check_num_val(self, unit_str, val, dimension = None):

        val2 = self.get_model().get_numeric_value(unit_str, dimension)
        print("Ensuring %s returns %f in SI units of %s; it returns %f"%(unit_str, val, dimension, val2))
        self.assertAlmostEqual(val, val2)

    def test_parse_units(self):
        
        self.check_num_val('-60mV', -0.06, 'voltage')
        self.check_num_val('1V', 1, 'voltage')
        self.check_num_val('10 K', 10)
        self.check_num_val('0 K', 0)
        self.check_num_val('0 degC', 273.15)
        self.check_num_val('-40 degC', 233.15)
        
        self.check_num_val('1.1e-2 ms', 0.000011, 'time')
        self.check_num_val('5E-24', 5E-24)
        self.check_num_val('1.1ms', 0.0011)
        self.check_num_val('-60mV', -0.060)
        self.check_num_val('-60', -60)
        self.check_num_val('1.1e-2 ms', 0.000011)
        
        self.check_num_val('10.5 mS_per_cm2', 105, 'conductanceDensity')
        self.check_num_val('10.5 mS_per_cm2', 105)
        
        self.check_num_val('1 hour', 3600)
        self.check_num_val('30 min', 30*60)
        



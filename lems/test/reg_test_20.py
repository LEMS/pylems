#!/usr/bin/env python3
"""
Regression test for https://github.com/LEMS/pylems/issues/20

File: reg_test_20.py

Copyright 2021 LEMS contributors
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import unittest
import os
import textwrap
import tempfile
import typing

from lems.run import run as lems_run


class TestIssue20Regression(unittest.TestCase):

    """Regression test for issue #20

    PyLEMS does not initialise initMembPotential correctly.
    """

    def test_initMembPotential_init(self):
        """Test for https://github.com/LEMS/pylems/issues/20"""
        initmembpot = -20.000000000000000000000
        reg_20_nml = textwrap.dedent(
            """<neuroml xmlns="http://www.neuroml.org/schema/neuroml2"  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta3.xsd" id="TestDoc">

        <!-- regression test data for https://github.com/LEMS/pylems/issues/20 -->
        <ionChannel id="chnl_lk" type="ionChannelPassive" conductance="1nS" />

        <cell id="cell1">
          <morphology id="morpho">
            <segment id ="0" name="Soma">
              <proximal x="0" y="0" z="0" diameter="10"/>
              <distal x="10" y="0" z="0" diameter="10"/>
            </segment>

            <!-- Segment group probably not needed? -->
            <segmentGroup id="segs_soma">
              <member segment="0" />
            </segmentGroup>
          </morphology>

          <biophysicalProperties id="bio_cell">
            <membraneProperties>
              <channelPopulation id="chn_pop_lk" ionChannel="chnl_lk" number="1" erev="-50mV" />
              <spikeThresh value="20mV" />
              <specificCapacitance value="1.0 uF_per_cm2" segmentGroup="segs_soma" />
              <initMembPotential value="{}mV" />
            </membraneProperties>
            <intracellularProperties />
          </biophysicalProperties>
        </cell>
    </neuroml>
            """.format(
                initmembpot
            )
        )
        nml_file = tempfile.NamedTemporaryFile(mode="w+b")
        nml_file.write(str.encode(reg_20_nml))
        nml_file.flush()

        reg_20_xml = textwrap.dedent(
            """<Lems>
        <!-- regression test data for https://github.com/LEMS/pylems/issues/20 -->
        <Target component="sim1"/>

        <Include file="Simulation.xml"/>
        <Include file="Cells.xml"/>
        <Include file="{}"/>

        <Simulation id="sim1" length="100ms" step="0.1ms" target="cell1">
          <!-- (x|y)(min|max) don't appear to do anything with PyLEMS, but error if not included... -->
            <OutputFile path="." fileName="reg_20.dat">
                <OutputColumn quantity="v" />
            </OutputFile>
        </Simulation>
    </Lems>
            """.format(
                nml_file.name
            )
        )

        xml_file = tempfile.NamedTemporaryFile(mode="w+b")
        xml_file.write(str.encode(reg_20_xml))
        xml_file.flush()

        # TODO: replace this with pynml's extract LEMS files function when that has
        # been merged and released. We won't need to carry a copy of the coretypes
        # then.
        coretype_files_dir = (
            os.path.dirname(os.path.abspath(__file__)) + "/NeuroML2CoreTypes"
        )
        lems_run(xml_file.name, include_dirs=[coretype_files_dir])

        # Deletes the files also
        nml_file.close()
        xml_file.close()

        with open("reg_20.dat", "r") as res:
            for line in res:
                ln = line.split()
                time = float(ln[0])
                value = float(ln[1])
                assert time == 0
                self.assertAlmostEqual(value, initmembpot / 1000.0, delta=0.01)
                # We only want to check the first line
                break
        os.remove("reg_20.dat")

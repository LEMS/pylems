PyLEMS 
======

A LEMS (http://lems.github.io/LEMS) simulator written in Python which can be used to run NeuroML2 (http://neuroml.org/neuroml2.php) models

Usage as a LEMS model simulator
-------------------------------

    pylems [options] LEMS_file

**Options**

- -I/-include path - Adds a directory to the model file include search path

Examples
--------


**NeuroML examples (from https://github.com/NeuroML/NeuroML2/tree/development/NeuroML2CoreTypes)**

- Example 0 --  Working
- Example 1 --  Working
- Example 2 --  Working
- Example 3 --  Working
- Example 4 --  Not working (Unsupported in PyLEMS: KSChannel)
- Example 5 --  Working
- Example 6 --  Working
- Example 7 --  Working
- Example 8 --  Working
- Example 9 --  Working
- Example 10 -- Working
- Example 11 -- Working
- Example 12 -- Not working (Unsupported in PyLEMS: Property)
- Example 13 -- Working
- Example 14 -- Not working (Unsupported in PyLEMS: Property)
- Example 15 -- Working
- Example 16 -- Working (apart from spikeArray)
- Example 17 -- Working
- Example 18 -- Working


**LEMS examples (in directory examples)**

- example1.xml --  Working
- example2.xml --  Working
- example3.xml --  Working
- example4.xml --  Not working (Unsupported in PyLEMS: KSChannel)
- example5.xml --  Not working (Unsupported in PyLEMS: KSChannel)
- example6.xml --  Working
-- TODO: Rest of examples require an update to the <Simulation> element,
   i.e. use <Simulation...> not <SimulationSet...>, to work in PyLEMS 

      
**LEMS elements that do not work**

- XPath based parameters - PathParameter
- Assertions

**Tasks TODO**

- Implement flattening
- Decouple events from runnables
- Perform dimension-checking on expressions.
- Implement LEMS API over lems.model.* (NeuroML API?)
  - Interface with libNeuroML and Pyramidal to export Neuron MOD files
  - Export C files (Interface? Steve Marsh’s project?)
- Assertions.
- XPath implementation.
- Implement Runnables from Component types instead of expanded typeless Components (Required for efficient C/C++ code generation, but conflicts with flattening)



Travis integration
------------------

pylems is integrated with the the [Travis Continuous Integration service](http://travis-ci.org/).

[![Build Status](https://travis-ci.org/LEMS/pylems.png?branch=master)](https://travis-ci.org/LEMS/pylems)



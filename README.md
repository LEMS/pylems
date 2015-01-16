PyLEMS 
======

A LEMS (http://lems.github.io/LEMS) simulator written in Python which can be used 
to run NeuroML2 (http://neuroml.org/neuroml2.php) models.

For more about PyLEMS see:

Michael Vella, Robert C. Cannon, Sharon Crook, Andrew P. Davison, Gautham Ganapathy, Hugh P. C. Robinson, R. Angus Silver and Padraig Gleeson,
**libNeuroML and PyLEMS: using Python to combine procedural and declarative modeling approaches in computational neuroscience**
[Frontiers in Neuroinformatics 2014](http://journal.frontiersin.org/Journal/10.3389/fninf.2014.00038/abstract), doi: 10.3389/fninf.2014.00038

_**PLEASE CITE THE PAPER ABOVE IF YOU USE PYLEMS!**_

For more details on LEMS see: 

Robert C. Cannon, Padraig Gleeson, Sharon Crook, Gautham Ganapathy, Boris Marin, Eugenio Piasini and R. Angus Silver, 
**LEMS: A language for expressing complex biological models in concise and hierarchical form and its use in underpinning NeuroML 2**, 
[Frontiers in Neuroinformatics 2014](http://journal.frontiersin.org/Journal/10.3389/fninf.2014.00079/abstract), doi: 10.3389/fninf.2014.00079


Installation
------------

A stable version of PyLEMS is [available on PyPI](https://pypi.python.org/pypi/PyLEMS) using [pip](https://pip.pypa.io/en/latest/installing.html):

    pip install pylems

To install as root:

    sudo pip install pylems

Alternatively, you can obtain the latest version with

    git clone https://github.com/LEMS/pylems.git
    cd pylems 
    git checkout development   # optional
    sudo python setup.py install

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
-- TODO: Rest of examples require an update to the `<Simulation>` element,
   i.e. use `<Simulation...>` not `<SimulationSet...>`, to work in PyLEMS 

      
**LEMS elements that do not work**

- KSChannel
- Property
- XPath based parameters - PathParameter
- Assertions

**Tasks TODO**

- Implement flattening
- Decouple events from runnables
- Improve dimension-checking on expressions.


Travis integration
------------------

pylems is integrated with the the [Travis Continuous Integration service](http://travis-ci.org/).

[![Build Status](https://travis-ci.org/LEMS/pylems.png?branch=master)](https://travis-ci.org/LEMS/pylems)

This code is distributed under the terms of the GNU Lesser General Public License.



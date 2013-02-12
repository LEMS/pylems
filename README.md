# PyLEMS - A LEMS/NeuroML simulator written in Python

## Usage
runlems.py [-I/-include \<Model file include path\>] [-XI/-xsl-include \<XSL preprocessor include path\>] \<LEMS/NeuroML file\>

## Examples
### LEMS examples
+ example1 -- Running
+ example2 -- Running
+ example3 -- Running
+ example4 -- Running
+ example5 -- Not running (XPath)
+ example6 -- Running
+ example7 -- Running
+ example8 -- Running
+ example9 -- Not running

[an example](http://example.com/ "Title")

### NeuroML examples ([LEMS_NML2_Ex*.xml](https://github.com/NeuroML/NeuroML2/tree/master/NeuroML2CoreTypes/))
+ Example 0 -- Running
+ Example 1 -- Running
+ Example 2 -- Running
+ Example 3 -- Almost works (initial conditions) after disabling some model resolution checks.
+ Example 4 -- Not working
+ Example 5 -- Not running (XPath)
+ Example 6 -- Not running ([Issue 5](https://github.com/lisphacker/pylems/issues/5))
+ Example 7 -- Not running ([Issue 5](https://github.com/lisphacker/pylems/issues/5))
+ Example 8 -- Not running ([Issue 5](https://github.com/lisphacker/pylems/issues/5))
+ Example 9 -- Not working
+ Example 10 -- Not working. Too many spikes.
+ Example 11 -- Not running (Symbol parsing error?)
+ Example 12 -- XML preprecessing error in lxml
+ Example 13 -- Not running (XPath)
+ Example 14 -- No model!
+ Example 15 -- Not running (Perhaps related to [Issue 5](https://github.com/lisphacker/pylems/issues/5))

## TODO
+ XPath (DerivedParameter)
+ Flattening
+ Initial model stabilization
+ High-level LEMS API for creating, reading and writing LEMS files.

set -e
sudo python2.7 setup.py clean
sudo python2.7 setup.py install
python2.7 examples/apitest.py
python2.7 examples/apitest2.py
python2.7 examples/loadtest.py
python2.7 lems/dlems/exportdlems.py
python2.7 pylems ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex2_Izh.xml

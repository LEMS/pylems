set -e
python setup.py clean
python setup.py install
python examples/apitest.py
python examples/apitest2.py
python examples/loadtest.py
python lems/dlems/exportdlems.py
python pylems -I ../NeuroML2/NeuroML2CoreTypes ../NeuroML2/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml

set -e
sudo python3 setup.py clean
sudo python3 setup.py install
python3 examples/apitest.py
python3 examples/apitest2.py
python3 examples/loadtest.py
python3 examples/exportsom.py
#python pylems ~/NeuroML2/NeuroML2CoreTypes/Test_pylems.xml

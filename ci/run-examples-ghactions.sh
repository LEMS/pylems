#!/bin/bash

# Copyright 2021 LEMS contributors
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
# File : run-examples-ghactions.sh
#
# Run tests on GitHub actions

mkdir results

###      Try running "standard" LEMS examples
echo "Running standard LEMS examples"
./pylems examples/example1.xml -nogui
./pylems examples/example2.xml -nogui
./pylems examples/example3.xml -nogui
#./pylems examples/example4.xml -nogui     # Not working (Unsupported in PyLEMS: KSChannel)
#./pylems examples/example5.xml -nogui     # Not working (Unsupported in PyLEMS: KSChannel)
./pylems examples/example6.xml -nogui
# Rest of examples require an update to the <Simulation> element, i.e. use <Simulation...> not <SimulationSet...>, to work in PyLEMS

###      Try running NeuroML 2 examples
echo "Running NeuroML2 examples"
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex0_IaF.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex1_HH.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex2_Izh.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex3_Net.xml -nogui
#./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex4_KS.xml -nogui  # Not working (Unsupported in PyLEMS: KSChannel)
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex6_NMDA.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex7_STP.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex8_AdEx.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex9_FN.xml -nogui
#./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex10_Q10.xml -nogui
./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex11_STDP.xml -nogui

./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex13_Instances.xml -nogui

#./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex15_CaDynamics.xml -nogui

#./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex17_Tissue.xml -nogui
#./pylems -I NeuroML2/NeuroML2CoreTypes/ NeuroML2/LEMSexamples/LEMS_NML2_Ex18_GHK.xml -nogui  # Mismatch...

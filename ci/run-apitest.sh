#!/bin/bash

# Copyright 2021 LEMS contributors
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
# File : run-apitest.sh
#
# Run api tests on GitHub actions

python examples/apitest.py
python examples/apitest2.py
python examples/loadtest.py

# Update NeuroML2 path for CI
if [ "$CI" = "true" ]; then
    sed -i 's|../NeuroML2|./NeuroML2|g' lems/dlems/exportdlems.py
fi
python lems/dlems/exportdlems.py

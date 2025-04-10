#!/bin/bash

# Copyright 2023 LEMS contributors
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
# File : run-apitest.sh
#
# Run api tests on GitHub actions

cd examples
python apitest.py
python apitest2.py
python apitest3.py
python loadtest.py
python apitest_maxmin.py
cd ..


# Update NeuroML2 path for CI
if [ "$CI" = "true" ]; then
    if [ "$RUNNER_OS" = "macOS" ]; then
        sed -i '' 's|../NeuroML2|./NeuroML2|g' lems/dlems/exportdlems.py;
    else
        sed -i 's|../NeuroML2|./NeuroML2|g' lems/dlems/exportdlems.py;
    fi
fi
python lems/dlems/exportdlems.py

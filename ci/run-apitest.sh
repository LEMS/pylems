#!/bin/bash

# Copyright 2023 LEMS contributors
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
# File : run-apitest.sh
#
# Run api tests on GitHub actions

python examples/apitest.py
python examples/apitest2.py
python examples/loadtest.py

# Update NeuroML2 path for CI
if [ "$CI" = "true" ]; then
    if [ "$RUNNER_OS" = "macOS" ]; then
        sed -i '' 's|../NeuroML2|./NeuroML2|g' lems/dlems/exportdlems.py;
    else
        sed -i 's|../NeuroML2|./NeuroML2|g' lems/dlems/exportdlems.py;
    fi
fi
python lems/dlems/exportdlems.py

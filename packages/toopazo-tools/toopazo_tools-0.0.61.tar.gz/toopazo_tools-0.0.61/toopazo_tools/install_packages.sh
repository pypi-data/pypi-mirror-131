#!/usr/bin/env bash

FILE=venv/bin/activate
if [ -f "$FILE" ]; then
    echo "$FILE exists, sourcing it"
    source ${FILE}

#    sudo apt-get install python3-dev python3-venv
    python3 -m pip install -U matplotlib
    python3 -m pip install -U numpy
    python3 -m pip install -U scipy
    python3 -m pip install -U toopazo_tools
    python3 -m pip install -U toopazo_tools

else
    echo "$FILE does not exist."
fi
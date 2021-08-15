#!/bin/bash

# Nonsense to get conda install location
A=$(which conda)
B=$(dirname $A)/
export CONDA_DIR=$B..
source $CONDA_DIR/etc/profile.d/conda.sh

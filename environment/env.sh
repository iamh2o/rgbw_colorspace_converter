#!/bin/bash

# Nonsense to get conda install location
A=$(which conda)
B=$(dirname $A)/
export CONDA_DIR=$B..
source $CONDA_DIR/etc/profile.d/conda.sh
conda activate
conda activate HBP

## Dir of this script
THIS_DIR=$(dirname `realpath $0`)
export RGBW_CC_ROOT=$THIS_DIR/../
export PYTHONPATH=$RGBW_CC_ROOT/src/:$PYTHONPATH

export PATH=RGBW_CC_ROOT/bin/:$PATH

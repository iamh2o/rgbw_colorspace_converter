#!/bin/bash

################################################################################
# Sets up miniconda and HBP conda environment for running the color test UI
################################################################################

export repo=HBP

if [[ $1 != "$repo" ]]; then

  echo """

    Hello! This is the  __$repo___installer. This script will have almost certainly have died the time you read this.

    """
  echo "
    If you ran this script to see what it would do, you're in luck, it says hello and has not installed a conda env for you :-)  (yet!)."
  echo "
    	  If you simply wish to use the library, put  ./lib in your PYTHONPATH and import color.   See the comments in ./lib/color.py for more info.

          And if you wish it to create a conda env, with a SUPER minimal color test UI... continue reading please.

	  "
  echo "
	   To install $repo, you'll enter 2 arguments: '$repo' CONDA_DIR(/path/to/conda).

           If CONDA_DIR is an existing conda root directory, the conda install will be skipped and the supersonic annd mantasvenv2 envs will be created using the existing conda install--- though, mamaba will be installed into the base conda env(you can skip this part, but are now trailblazing and all waranties are void) ( https://github.com/mamba-org/mamba). "
  echo "
               mamba installs to base. Then the $repo yaml file is used to build the env. It should be fast if you're used to old skool conda.  You'll need the base environment to be called 'base' for this to (hopefully) run.  You are free to hack though."
  echo "
																	Right.
														   To recap: to install $repo, run this script again with the first argument being '$repo' and the second argument being the path to install conda to -OR- your existing conda install dir. If there is a file or dir in the place specified, conda base environment install will be skipped and the existing codna env will be attempted to be used.  The third argument is if you would like to run the post installation micro-test, type yes to run the tests and no to skip them (not implemented yet).


ie: ./setup.sh $repo $HOME/conda [no|yes]

"
  exit 15
fi

echo "$repo----------------------------PrepareForLaunch"
sleep 2

if [[ $2 == "" ]]; then
  echo "

    .......Please specify a path to find/install conda as argument #2

    "
  exit 33
fi

export CONDA_DIR=$2
echo "(INSTALLING/LOKING FOR) CONDA IN "$CONDA_DIR
sleep 3

export ENV_DIR=$(dirname $0)
export CPUS=$(fgrep processor /proc/cpuinfo | wc -l)

# Install miniconda if you don't have it
if [[ ! -d $CONDA_DIR ]]; then
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh -b -p $CONDA_DIR
  rm Miniconda3-latest-Linux-x86_64.sh
fi

source $CONDA_DIR/etc/profile.d/conda.sh
conda init
conda deactivate
source ~/.bashrc

source $CONDA_DIR/etc/profile.d/conda.sh
conda install -y -n base -c conda-forge mamba

# Create conda environment
echo "CREATING $e"
mamba env create -n $repo -f $repo.yaml

conda activate $repo
source ./env.sh

cd ..
pre-commit install
sleep 1
conda activate $repo
pip install -e .
sleep 1

echo "

       It would appear things installed!  Great Success. The evironments should be accessible via:
            - conda activate $repo
	    - run a test with pytest
	    - run the UI with ./bin/run_color_test.sh

                                               ╦ ╦╔╗ ╔═╗
                                               ╠═╣╠╩╗╠═╝
                                               ╩ ╩╚═╝╩
"

bin/run_spectrum_saturation_cycler.py 2
exit 0

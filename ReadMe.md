# CAMP Application Program Example

This repository provides a minimal working example of an application code using the CAMP library for collision free motion generation. 

## Quick Start

First, clone this repository.

`git clone https://github.com/cchaas-uwaterloo/iso-motion-planning-application-ex.git`

Create an empty conda environment.

`conda create --name <your_env_name>`

Activate the environment.

`conda activate <your_env_name>`

Next, in another folder, clone the CAMP package.

`git clone https://github.com/cchaas-uwaterloo/iso-motion-planning.git`

Follow the instructions in the CAMP ReadMe to set up the package.

Once the CAMP package is set up, in this folder:

Install the CAMP package using `pip`.

`pip install <path_to_camp_workspace_root>`

The quadratic program solver used for the differential inverse kinematics needs to be installed manually. 

`conda install -c conda-forge qpoases`

The installation of the CAMP package and its dependencies can be checked by running `conda list`. You 
should see: 

`camp                      0.0.1                    pypi_0    pypi`

The test script `camp_test.py` can now be run simply by calling: 

`python camp_test.py`

The script should generate an `images/` and a `videos/` folder into which the output of the camp functions will be written.
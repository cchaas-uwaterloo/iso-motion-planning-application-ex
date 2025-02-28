# CAMP Application Program Example

This repository provides a minimal working example of an application code using the CAMP library for collision free motion generation. 

## Quick Start

First, clone this repository








The CAMP package can be installed into other projects on the same machine. First, in the workspace of the project using
CAMP, create a conda environment. 

`conda create --name <your_env_name>`

Activate the environment. 

`conda activate <your_env_name>`

Install the CAMP package using `pip`.

`pip install <path_to_camp_workspace_root>`

The quadratic program solver used for the differential inverse kinematics needs to be installed manually. 

`conda install -c conda-forge qpoases`

The installation of the CAMP package and its dependencies can be checked by running `conda list`. You 
should see: 

`camp                      0.0.1                    pypi_0    pypi`

The camp and sort functions can now be imported and used in the application project.
# iwfm

Python functions to work with IWFM-based models

# README #

* Quick summary

The California Department of Water Resources is actively developing the Integrated Water Flow Model for creating integrated hydrologic models. 

This repository contains a python package for working with IWFM model input and output files. Many of these work across the Windows, Linux and MacOS operating systems.

* Version

Initial release: Alpha January 2021

### How do I get set up? ###

Install the latest release of Python 3.

Download this repository and navigate to the iwfm directory. Install using 'python -m pip install'. 

Alternatively, if you want to contribute to this project, see the installation instructions below.

### How do I use this package? ###

* In python programs

Once this package is installed, import 'iwfm' to use the package components.

For example, to use the hyd_diff function (create a new IWFM hydrograph file as the difference between two IWFM hydrograph files):
 
import iwfm as iwfm

iwfm.hyd_diff(scenario_file_name, base_file_name, diff_file_name)
 
Or:
 
import iwfm.hyd_diff as hyd_diff

hyd_diff(scenario_file_name, base_file_name, diff_file_name)
 
* From the command line

Many of the python functions can also be run from the command line, as they contain a section “if __name__ = ‘__main__’:" that handles command line input. For example, to run hyd_diff.py from the Results directory of a model, you can use:
 
python [path\to\iwfm\package\directory]\hyd_diff.py C2VSimFG_GW_Hydrograph_Scenario.out C2VSimFG_GW_Hydrograph_Base.out C2VSimFG_GW_Hydrograph_Diff.out
 
You may also be able to make [path\to\iwfm\package\directory] part of the PYTHONPATH environment variable to run commands without specifying this path.

### Contribution guidelines ###

Please consider contributing to this effort, whether through bug reporting, making improvements or contributing new components.

To become a contributor, download the source file repository using Github Desktop, Sourcetree, terminal-based git, or another source control program.

Install the package using 'python -m pip install -e'. The '-e' option will allow you to edit the source files while using the package; python will then re-compile any changed files to pseudocode at execution time.

Submit suggested code changes and additions to the repository using a 'pull request'.

### Who do I talk to? ###

* Repo owner/admin: cfbrush@ucdavis.edu

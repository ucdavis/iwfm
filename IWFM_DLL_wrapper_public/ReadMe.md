# IWFM-DLL Python Wrapper
This code repository is the beginnings of a python wrapper for the IWFM-DLL. This may be useful if you are looking to interface with an IWFM model using python. Using this python wrapper, one can run an IWFM model, fully couple an IWFM model with another model using python, or quickly analyze results from an IWFM simulation.

To get started with this codebase...
    1) You need a windows computer  
    2) You need an IWFM model and it's associated IWFM-DLL (ex. C2VSimFG v1.01 with IWFM-DLL v1129 which can be downloaded at https://data.cnra.ca.gov/dataset/c2vsimfg-version-1-01)  
    3) It is strongly recommended that you read through the first few chapters of the IWFM-DLL documentation, available here: https://data.cnra.ca.gov/dataset/iwfm-integrated-water-flow-model/resource/6be7a705-5577-4fa0-b02e-d28cabc75c9a?inner_span=True  

Note: this codebase was written with C2VSim Fine Grid version 1.01 in mind, which is an IWFM/IDC model developed by the CA Department of Water Resources. C2VSimFG v1.01 can be downloaded at https://data.cnra.ca.gov/dataset/c2vsimfg-version-1-01
This codebase specifies filepaths as if the C2VSimFG v1.01 is downloaded and ran in folder named "modelRuns" located in the same directory as DLL_shortcuts.py.   

This codebase is a work in progress and is not guarenteed to work for all use cases. Feedback is welcome.  

## Description of files included
DLL_shortcuts.py:  
    - This file is the meat of the repository. It offers a subset of functions listed in the IWFM-DLL documentation, each one is callable in python and returns a python object.  
    
customRead_functions.py:  
    - This script utilizes DLL_shortucts.py to grab data from all simulation output budget hdf files and convert them to a pandas dataframe object  

customPlot_functions.py:      
    - This script uses the pandas dataframe developed by the customRead_function to plot various budget items for various modelRuns (or scenarios), all on the same timeseries plot. This function is potentially useful for exploring budget data and comparing model results.  

plottingExample.ipynb:  
    - This is a jupyter notebook file that gives an example of how to use the customPlot_functions  
    - Jupyter notebook or jupyter lab can be accessed through anaconda  

runningModel_oneStep-at-a-time_example.ipynb:  
    - This is a jupyter notebook file that gives an example of how to use the model group functions from DLL_shortcuts.py to run an IWFM model one step at a time. This is potentially useful if you want to fully couple IWFM with another model. For more info, see "Running an IWFM Model Application from Client Code" in Section 5.1 of IWFM-DLL 1129 (Emin C. Dogrul and Tariq N. Kadir, Feb. 2021).  

IWFM-2015.0.1129:  
    - This a copy of the IWFM-DLL version 1129. This can downloaded along with C2VSim FG v1.01 at https://data.cnra.ca.gov/dataset/c2vsimfg-version-1-01  
    
modelRuns:  
    - Empty folder, included as potential folder structure (put complete models here to analyze with IWFM-DLL wrapper without modifying file paths in DLL_shortcuts.py)  

### WARNINGS ABOUT DLL_shortcuts.py  
First note that DLL_shortcuts.py is not complete. There are many functions available in the IWFM-DLL that are not included in this wrapper (though the budget module is nearly complete). Please refer to the IWFM-DLL documentation for a complete list of possible functions. Hopefully the functions included can serve as a template for futher development.  

Second, this code is designed with C2VSimFG v1.01 in mind, and may not be immediately applicable to all IWFM models. For example, DLL_shortcuts.py assumes the following:  
1) The user's IWFM internal model timestep and desired budget output timestep are both months
2) The user's IWFM internal simulation unit is in feet, square feet, and cubic feet for length, area, and volume respectively
3) The user's desired output file units are in feet, acres, and ac-ft for length, area, and volume respectively
4) The user is using a 64 bit windows machine
    - A 32 bit windows machine could also work, just change filePath for IWFM-DLL in DLL_shortcuts.py
5) The user is analyzing a model that uses IWFM version 1129
    - IWFM-DLL v1129 is the IWFM version used by C2VSim v1.01
    - More recent versions are available at https://data.cnra.ca.gov/dataset/iwfm-integrated-water-flow-model/resource/64b1047a-39ff-46db-8b93-1e6f95e50865?inner_span=True
    - This code repository may be compatable with other versions, but not all versions have been tested
6) For IW_Model_New and IW_Model_DeleteInquiryDataFile functions, user needs to specify the filenames of the simulation and/or preprocessor input (.in) files
    - Example filepaths provided are for C2VSim v1.01
7) The user will input model indices to functions for subregions as opposed to subregion number
    - For more info, refer to "IWFM Model Feature Indices versus Identification Numbers," section 7 of IWFM-DLL 1129 Documentation (Emin C. Dogrul and Tariq N. Kadir, Feb. 2021)
    - If Subregions are listed in order, starting with 1 and increasing by 1 each row, indices may be the same as region numbers
8) All Budget group functions depend on the model results being present in hdf form
    - This means the preprocessor, simulation, and budget exe files need to be ran before the budget group functions will work
    - This can take several hours

The DLL_shortcuts.py depends on the following python libraries:  
    - ctypes  
    - numpy  

### WARNINGS ABOUT customRead_functions and customPlot_functions  
Again, these scripts are designed for C2VSimFG v1.01, so the following assumptions are made:  
1) The binary (hdf) budget filenames and paths are not modified from the original C2VSimFG v1.01 file structure (though the folder name can be different)
2) There are 21 subregions, all listed in order starting at one, and the 22nd subregional budget reflects budget results from the entire model area
3) All units are in acres or acre-feet (one can double check units by looking at .out text budget files)
4) Similar to  DLL_shortcuts.py, it is assumed the user will input model indices for subregions as opposed to subregion number
    - For more info, refer to "IWFM Model Feature Indices versus Identification Numbers," section 7 of IWFM-DLL 1129 Documentation (Emin C. Dogrul and Tariq N. Kadir, Feb. 2021)  
    - If Subregions are listed in order, starting with 1 and increasing by 1 each row, indices may be the same as region numbers  
    - Plot titles list subregion index, not subregion number  

The customRead_functions and customPlot_functions need the following python libraries to work:  
    - numpy  
    - pandas  
    - matplotlib.pyplot   
These libraries should be included in the standard anaconda distribution.  

### Acknowledgements
Work on this IWFM-DLL python wrapper was suported by the National Science Foundation, award #1716130

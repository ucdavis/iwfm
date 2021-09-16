from DLL_shortcuts import *
import numpy as np
import pandas as pd

def read_subregionBudget(modelScenario_name, subregion_index='all', verbose=True):
    # Reads all budget items for specifed model subregion, returns pandas dataframe
    # Assumes subregions are listed in order in C2VSim input files (true for v1 public release)
    # Assumes there are 21 subregions (true for v1 public release)
    # default is to retreive budget for all subregions, but this can be achieved by indicating "all" or 22 for the subregion index
    
    if subregion_index=='all' or subregion_index==22:
        subregion_index = 22
        if verbose:
            print('Loading Budget for Entire Simulation Area in AF for Model Scenario ', modelScenario_name, "...")
    elif (subregion_index <= 21) & (subregion_index > 0):
        if verbose:
            print('Loading Budget for Subregion', subregion_index, "in AF\nModel Scenario ", modelScenario_name, "...")
    else:
        print("Error: Subregion not allowed")
        return

    budFileName_list = ['C2VSimFG_GW_Budget.hdf',
                        'C2VSimFG_L&WU_Budget.hdf',
                        'C2VSimFG_RZ_Budget.hdf',
                        'C2VSimFG_Stream_Budget.hdf',
                        'C2VSimFG_SWatersheds_Budget.hdf',
                        'C2VSimFG_Unsat_Budget.hdf'
                       ]
    
    budType_list = ['GROUNDWATER BUDGET',
                    'LAND AND WATER USE BUDGET',
                    'ROOT ZONE MOISTURE BUDGET',
                    'STREAM FLOW BUDGET',
                    'SMALL WATERSHED FLOW COMPONENTS',
                    'UNSATURATED ZONE BUDGET'
                   ]
    
    df_name_list = ['GWBud_df',
                    'LWUBud_df',
                    'RZBud_df',
                    'StreamBud_df',
                    'SWatershedsBud_df',
                    'UnsatBud_df'
                   ]

    fileCounter = 0
    for budFileName in budFileName_list:
        IW_Budget_OpenFile(modelScenario_name, budFileName)
        df_name_list[fileCounter] = pd.DataFrame(data = IW_Budget_GetValues(subregion_index),
                                 index  = pd.to_datetime(IW_Budget_GetTimeSpecs(), format='%m/%d/%Y_24:00'),
                                 columns = IW_Budget_GetColumnHeaders(subregion_index)
                                )
        df_name_list[fileCounter].insert(0, 'budType', budType_list[fileCounter])
        IW_Budget_CloseFile()
        fileCounter += 1
        
    output_df = pd.concat(df_name_list)
    return output_df
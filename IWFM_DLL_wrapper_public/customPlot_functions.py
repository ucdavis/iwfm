from DLL_shortcuts import *
from customRead_functions import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_budItem_for_SubregionList_multiScenario(budType,
                                   budItem,
                                   scenario_list,
                                   label_list,
                                   subRegion_list,
                                   verbose=True):
    
    # check to make sure subregion is defined in C2VSim (must be in range 1 to 22)
    for subRegion in subRegion_list:
        if subRegion=='all' or subRegion==22:
            subRegion = 22
            if verbose:
                print('\nPlotting ', budItem, " from the ", budType, "for Entire Simulation Area...\n")
        elif (subRegion <= 21) & (subRegion > 0):
            if verbose:
                print('\nPlotting ', budItem, " from the ", budType, "for Subregion",subRegion, "...\n")
        else:
            print("Error: Subregion not allowed")
            return
        
        # for each scenario, plot the specified budget item
        counter = 0
        plt.figure(figsize=(15,7))
        for df in scenario_list:
            df = read_subregionBudget(df, subRegion, verbose=False)
            dfBud = df.where(df.budType == budType).dropna(axis = 0, how='all').dropna(axis = 1, how='all')
            colNames = dfBud.columns
            
            # check to make sure budget item is in the specified budget
            if budItem not in colNames:
                print("Error: Budget item not in desired budget.\n")
                print("The following are available budget items for the ",budType, ":")
                for col in colNames.values[2:]:
                    print(col)
                plot = False
                plt.close()
                return
            
            # assign units for plots
            # double check units if different scenarios have budgets w/ min value that differ by an order of magnitude
            # units are adjusted only according to the first scenario
            if counter == 0:
                if dfBud[budItem].min() > 1000000:
                    plt.plot(dfBud[budItem]/1000000)
                    unitCorrection = 1000000
                    if 'acres' in budItem:
                        unit = 'million acres'
                    else:
                        unit =  'million AF'
                elif dfBud[budItem].min() > 1000:
                    plt.plot(dfBud[budItem]/1000)
                    unitCorrection = 1000
                    if 'acres' in budItem:
                        unit = 'thousand acres'
                    else:
                        unit =  'thousand AF'
                else:
                    plt.plot(dfBud[budItem])
                    unitCorrection = 1
                    if 'acres' in budItem:
                        unit = 'acres'
                    else:
                        unit =  'AF'
            else:
                plt.plot(dfBud[budItem]/unitCorrection)
            
            counter += 1
                    
        plt.xlabel('Year')                
        plt.legend(label_list)
        budItem_plot = budItem.replace('(-)','').replace('(+)','').replace('(=)','').replace('(acres)','').replace('&',' & ')
        
        # write the plot title and verticle axis label with subregion number and units respectively
        if (subRegion == 'all') or (subRegion == 22):
            plt.title(budItem_plot + 'for Entire Simulation Area')

        else:
            plt.title(budType + ": " + budItem_plot + 'for Subregion '+str(subRegion))
            
        if 'acres' in budItem_plot:
            plt.ylabel(budItem_plot)
            
        else:
            plt.ylabel(budItem_plot + ' ('+ unit +')')
        
        # plt.savefig('output_Figure')
        plt.show()
        
    if verbose:
        print("The following are available budget items for the ",budType, ":")
        for col in colNames.values[2:]:
            print(col)
    return
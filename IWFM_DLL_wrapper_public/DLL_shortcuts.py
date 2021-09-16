import ctypes
import numpy as np

#### WARNING ####
# Please review this branch's ReadMe file for assumptions made in DLL_shortcuts.py
# Code base is desinged with C2VSim v 1.01 in mind and may not be immediately applicable to all IWFM models

# Specify homePath
homePath = 'modelRuns\\'
## homePath should point to the folder that contains at least one IWFM model run
## Be sure homePath ends in '\\' or '/'
###  Each model run should be contained in it's own folder, and should include the standard C2VSim file architecture: (bin, Preprocessor, Simulation, Results, Budget, Zbudget)

# Specify file path for IWFM-DLL file
IWFM_DLL_path = 'IWFM-2015.0.1129\\DLL\\Bin\\IWFM2015_C_x64.dll'

# Load IWFM-DLL
IWFM_dll = ctypes.windll.LoadLibrary(IWFM_DLL_path)

# Initiate error code; returns 0 if the procedure call was successful
iStat = ctypes.c_int()


# Custom function to split concatenated strings using index arrays, both returned from IWFM-DLL
def split_stringList(stringList, iLocArray):
    # Input: binary string & list of indices (encoded, starting at 1) by which to spit the string
    # Output: array of strings
    stringList = stringList.value.decode()
    iLocArray = np.array(iLocArray)-1
    
    i = 0
    outputList = []
    while i <= len(iLocArray) - 1:
        if i < len(iLocArray) - 1:
            name = stringList[iLocArray[i]:iLocArray[i+1]]
            outputList = np.append(outputList, name)

        elif i == len(iLocArray) - 1:
            name = stringList[iLocArray[i]:]
            outputList = np.append(outputList, name)
        i += 1
    return outputList


#########################################################
##################### Misc Group ########################
#########################################################
def IW_SetLogFile(errorLog_path = "IW_API_errorLog.txt"):
    errorLog_path = homePath + '\\' + errorLog_path
    cFileName = ctypes.create_string_buffer(errorLog_path.encode('ascii'))
    iLen =  ctypes.c_int(ctypes.sizeof(cFileName))
    IWFM_dll.IW_SetLogFile(ctypes.byref(iLen),cFileName,ctypes.byref(iStat))
    if iStat.value == 0:
        print("Success! Error Log Specified")
    else:
        print("Error")
    return

def IW_CloseLogFile():
    IWFM_dll.IW_CloseLogFile(ctypes.byref(iStat))
    if iStat.value == 0:
        print("Error Log Closed")
    else:
        print("Error")
    return

#########################################################
##################### Model Group #######################
#########################################################
# for each of the following functions, the "modelScenario_name" is name of folder containing the model scenario you seek to assess
# see IWFM-DLL 1129 documentation for info on each function's use

def IW_Model_New(modelScenario_name, iIsForInquiry = 1):
    ## Create model object for finite grid model
    ### (Change FileNames paths below if course grid)
    ## default iIsForInquiry value means unless specified or  there is no iIsForInquiry.bin file, a partial model obect will be created
    
    # Specify file path for preprocessor input file relative to modelScenario_name
    preprocessor_input_FilePath = "Preprocessor/C2VSimFG_Preprocessor.in"

    # Specify file path for simulation input file relative to homePath
    simulation_input_FilePath = "Simulation/C2VSimFG.in"
    
    # Preprocessor Main Input Filename
    cPPFileName = homePath + modelScenario_name + '/' + preprocessor_input_FilePath
    cPPFileName = ctypes.create_string_buffer(cPPFileName.encode('ascii'))

    # Character length of Preprocessor Main Input Filename
    iLenPPFileName = ctypes.c_int(ctypes.sizeof(cPPFileName))

    # Simulation Main Input Filename
    cSimFileName = homePath + modelScenario_name + '/' +  simulation_input_FilePath
    cSimFileName = ctypes.create_string_buffer(cSimFileName.encode('ascii'))

    # Character length of Simulation Main Input Filename
    iLenSimFileName = ctypes.c_int(ctypes.sizeof(cSimFileName))

    # 1 = stream flows are simulated within IWFM; 
    # 0 = stream network is defined but stream flows are simulated outside IWFM
    iIsRoutedStreams =  ctypes.c_int(1)

    # 1 = Model object is instantiated to retrieve data;
    # 0 = Model object is instantiated to perform a simulation
    iIsForInquiry =  ctypes.c_int(iIsForInquiry)
        
    IWFM_dll.IW_Model_New(ctypes.byref(iLenPPFileName),
                              cPPFileName,
                              ctypes.byref(iLenSimFileName),
                              cSimFileName,
                              ctypes.byref(iIsRoutedStreams),
                              ctypes.byref(iIsForInquiry),
                              ctypes.byref(iStat)
                     )
    if iStat.value == 0:
        print("Model Instantiated: ", modelScenario_name)
    else:
        print("Error")
    return

def IW_Model_IsModelInstantiated():
    iInstantiated = ctypes.c_int()
    IWFM_dll.IW_Model_IsModelInstantiated(ctypes.byref(iInstantiated),ctypes.byref(iStat))
    if ((iStat.value == 0) & (iInstantiated.value == 1)):
        return True
    elif ((iStat.value == 0) & (iInstantiated.value == 0)):
        return False
    else:
        print("Error")
        return
    
def IW_Model_ReadTSData():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_ReadTSData(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error")
        return
    
def IW_Model_AdvanceTime():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_AdvanceTime(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error")
        return
        
def IW_Model_AdvanceState():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_AdvanceState(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error")
        return
        
def IW_Model_GetCurrentDateAndTime():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    iLenDateAndTime = ctypes.c_int(16)
    cCurrentDateAndTime = ctypes.create_string_buffer(iLenDateAndTime.value)
    IWFM_dll.IW_Model_GetCurrentDateAndTime(ctypes.byref(iLenDateAndTime), 
                                            cCurrentDateAndTime,
                                            ctypes.byref(iStat)
                                           )
    if iStat.value == 0:
        return cCurrentDateAndTime.value.decode()
    else:
        print("Error")
        return
    
def IW_Model_SimulateForOneTimeStep():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_SimulateForOneTimeStep(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error")
        return
    
def IW_Model_SimulateAll():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_SimulateAll(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error")
        return    

def IW_Model_PrintResults():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_PrintResults(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error")
        return 
    
def IW_Model_IsEndOfSimulation():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    iEndOfSimulation = ctypes.c_int(-1)
    IWFM_dll.IW_Model_IsEndOfSimulation(ctypes.byref(iEndOfSimulation), ctypes.byref(iStat))
    if iStat.value == 0:
        if iEndOfSimulation.value == 0:
            return False
        elif iEndOfSimulation.value == 1:
            # end of simulation is reached
            return True
        else:
            print("Error")
            return
    else:
        print("Error")
        return 
        
def IW_Model_Kill():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    IWFM_dll.IW_Model_Kill(ctypes.byref(iStat))
    if iStat.value == 0:
        print("Model Killed")
    else:
        print("Error: Model could not be killed")
    return

def IW_Model_DeleteInquiryDataFile():
    # Specify file path for simulation input file relative to homePath
    simulation_input_FilePath = "Simulation/C2VSimFG.in"
    
    cSimFileName = homePath + modelScenario_name + '/' + simulation_input_FilePath
    cSimFileName = ctypes.create_string_buffer(cSimFileName.encode('ascii'))
    iLenSimFileName = ctypes.c_int(ctypes.sizeof(cSimFileName))
    
    IWFM_dll.IW_Model_DeleteInquiryDataFile(ctypes.byref(iLenSimFileName),
                                            cSimFileName,
                                            ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error: Inquiry file could not be deleted")
        return

def IW_Model_GetNNodes():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    NNodes = ctypes.c_int()
    IWFM_dll.IW_Model_GetNNodes(ctypes.byref(NNodes),
                                ctypes.byref(iStat)
                               )
    if iStat.value == 0:
        return NNodes.value
    else:
        print("Error")
        return
    

def IW_Model_GetNodeXY():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    NNodes = ctypes.c_int(IW_Model_GetNNodes())
    X = (ctypes.c_double*NNodes.value)()
    Y = (ctypes.c_double*NNodes.value)()
    IWFM_dll.IW_Model_GetNodeXY(ctypes.byref(NNodes),
                                X,
                                Y,
                                ctypes.byref(iStat))

    if iStat.value == 0:
        return {'X':np.array(X), 'Y':np.array(Y)}
    else:
        print("Error")
        return

def IW_Model_GetNSubregions():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    NSubregions = ctypes.c_int()
    IWFM_dll.IW_Model_GetNSubregions(ctypes.byref(NSubregions),ctypes.byref(iStat))
    if iStat.value == 0:
        return NSubregions.value
    else:
        print("Error")
        return
    
def IW_Model_GetSubregionIDs():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    
    NSubregion = ctypes.c_int(IW_Model_GetNSubregions())
    IDs = (ctypes.c_int*NSubregion.value)()
    IWFM_dll.IW_Model_GetSubregionIDs(ctypes.byref(NSubregion),
                                      IDs,
                                      ctypes.byref(iStat)
                                     )
    if iStat.value == 0:
        return np.array(IDs)
    else:
        print("Error")
        return
    
def IW_Model_ReadTSData():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    
    IWFM_dll.IW_Model_ReadTSData(ctypes.byref(iStat))
    
    if iStat.value == 0:
        return
    else:
        print("Error")
        return
    
def IW_Model_GetNLayers():
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    
    NLayers = ctypes.c_int()
    IWFM_dll.IW_Model_GetNLayers(ctypes.byref(NLayers),
                                 ctypes.byref(iStat))
    
    if iStat.value == 0:
        return NLayers.value
    else:
        print("Error")
        return
    
def IW_Model_GetTimeSpecs():    
    NData = 2
    iLenDates = 16*NData
    
    # Note: if simulation is not in months, this needs to change
    cInterval = "1MON"
    cInterval = ctypes.create_string_buffer(cInterval.encode('ascii'))
    iLenInterval = ctypes.c_int(8)
    cDataDatesAndTimes = ctypes.create_string_buffer(iLenDates)
    iLocArray = (ctypes.c_int*NData)()
    iLenDates = ctypes.c_int(iLenDates)
    NData = ctypes.c_int(NData)
    
    IWFM_dll.IW_Model_GetTimeSpecs(cDataDatesAndTimes,
                                    ctypes.byref(iLenDates),
                                    cInterval,
                                    ctypes.byref(iLenInterval),
                                    ctypes.byref(NData),
                                    iLocArray,
                                    ctypes.byref(iStat))
    if iStat.value == 0:
        return split_stringList(cDataDatesAndTimes,iLocArray)
    else:
        print("Error")
    return

def IW_GetNIntervals(): # yes this is misc. group, but it uses a model group function
    if IW_Model_IsModelInstantiated() == False:
        print('Need to initiate model')
        return
    
    cBeginDateAndTime = IW_Model_GetTimeSpecs()[0]
    cBeginDateAndTime = ctypes.create_string_buffer(cBeginDateAndTime.encode('ascii'))
    
    cEndDateAndTime = IW_Model_GetTimeSpecs()[1]
    cEndDateAndTime = ctypes.create_string_buffer(cEndDateAndTime.encode('ascii'))
    
    iLenDateAndTime = ctypes.c_int(ctypes.sizeof(cEndDateAndTime))
    
    # Note: if simulation is not in months, this needs to change
    cInterval = "1MON"
    cInterval = ctypes.create_string_buffer(cInterval.encode('ascii'))
    iLenInterval = ctypes.c_int(ctypes.sizeof(cInterval))
    NIntervals = ctypes.c_int()
    
    IWFM_dll.IW_GetNIntervals(cBeginDateAndTime,
                              cEndDateAndTime,
                              ctypes.byref(iLenDateAndTime),
                              cInterval,
                              ctypes.byref(iLenInterval),
                              ctypes.byref(NIntervals),
                              ctypes.byref(iStat)
                             )
    
    if iStat.value == 0:
        return NIntervals.value
    else:
        print("Error")
        return

# This Head function is not yet working
# def IW_Model_GetModelData_GWHeadsAll_ForALayer(layerNumber=2):
#     if IW_Model_IsModelInstantiated() == False:
#         print('Need to initiate model')
#         return
    
#     NLayers = IW_Model_GetNLayers() # number of aquifer layers in simulation
#     if (layerNumber > NLayers) or (layerNumber < 1):
#         print('Invalid aquifer layer! Max number of aquifer layers: ', NLayers)
#         return
        
#     iLayer = ctypes.c_int(layerNumber)
#     cOutputBeginDateAndTime = IW_Model_GetTimeSpecs()[0]
#     cOutputBeginDateAndTime = ctypes.create_string_buffer(cOutputBeginDateAndTime.encode('ascii'))
    
#     cOutputEndDateAndTime = IW_Model_GetTimeSpecs()[1]
#     cOutputEndDateAndTime = ctypes.create_string_buffer(cOutputEndDateAndTime.encode('ascii'))
    
#     iLenDateAndTime = ctypes.c_int(ctypes.sizeof(cOutputEndDateAndTime)*2)
    
#     # Note: if simulation unit is not the same as desired output, this needs to change
#     rFact_LT = ctypes.c_double(1.0) # from ft. to ft.
#     iNNodes = ctypes.c_int(IW_Model_GetNNodes())
#     iNTime = ctypes.c_int(IW_GetNIntervals())   
#     rOutputDates = (ctypes.c_double*iNTime.value)()
#     rGWHeads = ((ctypes.c_double*iNNodes.value)*iNTime.value)()
    
#     IWFM_dll.IW_Model_GetModelData_GWHeadsAll_ForALayer(ctypes.byref(iLayer),
#                                                         cOutputBeginDateAndTime,
#                                                         cOutputEndDateAndTime,
#                                                         ctypes.byref(iLenDateAndTime),
#                                                         ctypes.byref(rFact_LT),
#                                                         ctypes.byref(iNNodes),
#                                                         ctypes.byref(iNTime),
#                                                         rOutputDates,
#                                                         ctypes.byref(iNTime), # repeat
#                                                         rOutputDates, # repeat
#                                                         rGWHeads,
#                                                         ctypes.byref(iStat))
#     if iStat.value == 0:
#         return np.array(rGWHeads)
#     else:
#         print("Error")
#         return

#########################################################
##################### Budget ############################
#########################################################
def IW_Budget_OpenFile(modelScenario_name, budFileName):
    # budFileName is the name of the hdf budget file in the results folder that you aim to open
    cFileName = homePath + modelScenario_name + "\\Results\\" + budFileName
    cFileName =  ctypes.create_string_buffer(cFileName.encode('ascii'))
    iLen = ctypes.c_int(ctypes.sizeof(cFileName))
    
    IWFM_dll.IW_Budget_OpenFile(cFileName,
                                ctypes.byref(iLen),
                                ctypes.byref(iStat)
                                )
    if iStat.value == 0:
        return
    else:
        print("Error: Could not open budget file")
        return
    
def IW_Budget_CloseFile():
    IWFM_dll.IW_Budget_CloseFile(ctypes.byref(iStat))
    if iStat.value == 0:
        return
    else:
        print("Error:  Could not close budget file")
        return

def IW_Budget_GetNLocations():
    NLocations = ctypes.c_int()
    IWFM_dll.IW_Budget_GetNLocations(ctypes.byref(NLocations),ctypes.byref(iStat))
    if iStat.value == 0:
        return NLocations.value
    else:
        print("Error")
    return

def IW_Budget_GetLocationNames():
    NLocations = IW_Budget_GetNLocations()
    NLocations = ctypes.c_int(NLocations)
    iLenLocNames = ctypes.c_int(30*NLocations.value)
    cLocNames = ctypes.create_string_buffer(iLenLocNames.value)
    iLocArray = (ctypes.c_int*NLocations.value)()
    
    IWFM_dll.IW_Budget_GetLocationNames(cLocNames,
                                        ctypes.byref(iLenLocNames),
                                        ctypes.byref(NLocations),
                                        iLocArray,
                                        ctypes.byref(iStat)
                                       )
    
    if iStat.value == 0:
        return split_stringList(cLocNames,iLocArray)
    else:
        print("Error")
    return

def IW_Budget_GetNTimeSteps():
    NTimeSteps = ctypes.c_int()
    IWFM_dll.IW_Budget_GetNTimeSteps(ctypes.byref(NTimeSteps),ctypes.byref(iStat))
    
    if iStat.value == 0:
        return NTimeSteps.value
    else:
        print("Error")
    return

def IW_Budget_GetTimeSpecs():    
    NData = IW_Budget_GetNTimeSteps()
    iLenDates = 16*NData
    
    # Note: if simulation is not in months, this needs to change
    cInterval = "1MON"
    cInterval = ctypes.create_string_buffer(cInterval.encode('ascii'))
    iLenInterval = ctypes.c_int(ctypes.sizeof(cInterval))
    cDataDatesAndTimes = ctypes.create_string_buffer(iLenDates)
    iLocArray = (ctypes.c_int*NData)()
    iLenDates = ctypes.c_int(iLenDates)
    NData = ctypes.c_int(NData)
    
    IWFM_dll.IW_Budget_GetTimeSpecs(cDataDatesAndTimes,
                                    ctypes.byref(iLenDates),
                                    cInterval,
                                    ctypes.byref(iLenInterval),
                                    ctypes.byref(NData),
                                    iLocArray,
                                    ctypes.byref(iStat))
    if iStat.value == 0:
        return split_stringList(cDataDatesAndTimes,iLocArray)
    else:
        print("Error")
    return

def IW_Budget_GetNTitleLines():
    NTitles = ctypes.c_int()
    IWFM_dll.IW_Budget_GetNTitleLines(ctypes.byref(NTitles),
                                    ctypes.byref(iStat))
    
    if iStat.value == 0:
        return NTitles.value
    else:
        print("Error")
    return

def IW_Budget_GetTitleLength():
    iLen  = ctypes.c_int()
    IWFM_dll.IW_Budget_GetTitleLength(ctypes.byref(iLen),
                                    ctypes.byref(iStat))
    if iStat.value == 0:
        return iLen.value
    else:
        print("Error")
    return

    
def IW_Budget_GetNColumns(iLoc):
    iLoc = ctypes.c_int(iLoc)
    NColumns = ctypes.c_int()
    
    IWFM_dll.IW_Budget_GetNColumns(ctypes.byref(iLoc), 
                                   ctypes.byref(NColumns),
                                  ctypes.byref(iStat))
    if iStat.value == 0:
        return NColumns.value
    else:
        print("Error")
    return

def IW_Budget_GetColumnHeaders(iLoc):
    NColumns = IW_Budget_GetNColumns(iLoc)
    iLenColumnHeaders = NColumns*30
    cColumnHeaders = ctypes.create_string_buffer(iLenColumnHeaders)
    
    LengthUnit = "feet"
    LengthUnit = ctypes.create_string_buffer(LengthUnit.encode('ascii'))
    
    AreaUnit = "acres"
    AreaUnit = ctypes.create_string_buffer(AreaUnit.encode('ascii'))
    
    VolumeUnit = "acre-feet"
    VolumeUnit = ctypes.create_string_buffer(VolumeUnit.encode('ascii'))

    iLenUnit = (ctypes.c_int*3)(ctypes.sizeof(LengthUnit),
                                ctypes.sizeof(AreaUnit),
                                ctypes.sizeof(VolumeUnit)
                                )
    iLocArray = (ctypes.c_int*NColumns)()
    
    NColumns = ctypes.c_int(NColumns)
    iLenColumnHeaders = ctypes.c_int(iLenColumnHeaders)
    iLoc = ctypes.c_int(iLoc)
    
    IWFM_dll.IW_Budget_GetColumnHeaders(ctypes.byref(iLoc),
                                        cColumnHeaders,
                                        ctypes.byref(iLenColumnHeaders),
                                        ctypes.byref(NColumns),
                                        LengthUnit,
                                        AreaUnit,
                                        VolumeUnit,
                                        iLenUnit,
                                        iLocArray,
                                        ctypes.byref(iStat))
    
    if iStat.value == 0:
        return split_stringList(cColumnHeaders,iLocArray)
    else:
        print("Error")
    return
                                                     
def IW_Budget_GetValues(iLoc):
    nReadCols = IW_Budget_GetNColumns(iLoc)+1
    iReadCols = np.array(range(1,nReadCols))
    
    # conversion factors from simulation unit to desired output (should align with IW_Budget_GetColumnHeaders)
    rFact_LT = ctypes.c_double(1.0) # from ft. to ft.
    rFact_AR = ctypes.c_double(0.000022957) # from sq. ft. to acre (0.000022957 = 1/43560)
    rFact_VL = ctypes.c_double(0.000022957) # from cubic ft. to ac-ft

    # note for nTimes_In: If an output interval other than the buget file's interval is specifed, use IW_GetNIntervals instead
    nTimes_In = IW_Budget_GetNTimeSteps()
    nTimes_Out = nTimes_In
    Values = ((ctypes.c_double*(nReadCols))*nTimes_In)()
    iLoc = ctypes.c_int(iLoc)
    iReadCols = (ctypes.c_int*(len(iReadCols)))(*iReadCols)
    nReadCols = ctypes.c_int(nReadCols-1)
    nTimes_In = ctypes.c_int(nTimes_In)
    nTimes_Out = ctypes.c_int(nTimes_Out)
    
    cDateAndTimeBegin = IW_Budget_GetTimeSpecs()[0]
    cDateAndTimeBegin = ctypes.create_string_buffer(cDateAndTimeBegin.encode('ascii'))
    cDateAndTimeEnd = IW_Budget_GetTimeSpecs()[-1]
    cDateAndTimeEnd = ctypes.create_string_buffer(cDateAndTimeEnd.encode('ascii'))
    iLenDateAndTime = ctypes.c_int(ctypes.sizeof(cDateAndTimeBegin))
    
    # Note: if desired output timestep is not months, this needs to change
    cOutputInterval = "1MON"
    cOutputInterval = ctypes.create_string_buffer(cOutputInterval.encode('ascii'))
    iLenInterval = ctypes.c_int(ctypes.sizeof(cOutputInterval))
    
    IWFM_dll.IW_Budget_GetValues(ctypes.byref(iLoc),
                                 ctypes.byref(nReadCols),
                                 iReadCols,
                                 cDateAndTimeBegin,
                                 cDateAndTimeEnd,
                                 ctypes.byref(iLenDateAndTime),
                                 cOutputInterval,
                                 ctypes.byref(iLenInterval),
                                 ctypes.byref(rFact_LT),
                                 ctypes.byref(rFact_AR),
                                 ctypes.byref(rFact_VL),
                                 ctypes.byref(nTimes_In),
                                 Values,
                                 ctypes.byref(nTimes_Out),
                                 ctypes.byref(iStat)
                                )
    if iStat.value == 0:
        return np.delete(np.array(Values), -1, 1)

    else:
        print("Error")
    return



# def IW_Budget_GetTitleLines(iLocation):
#     NTitles = IW_Budget_GetNTitleLines()
    
#     FactArea = ctypes.c_int(1)
# #     LengthUnit = ctypes.c_int(1)

#     LengthUnit = "feet"
#     LengthUnit = ctypes.create_string_buffer(LengthUnit.encode('ascii'))
    
#     AreaUnit = "acres"
#     AreaUnit = ctypes.create_string_buffer(AreaUnit.encode('ascii'))
    
#     VolumeUnit = "acre-feet"
#     VolumeUnit = ctypes.create_string_buffer(VolumeUnit.encode('ascii'))

#     iLenUnit = (ctypes.c_int*ctypes.c_int(3))(ctypes.sizeof(LengthUnit.value),
#                                               ctypes.sizeof(AreaUnit.value),
#                                               ctypes.sizeof(VolumeUnit.value)
#                                              )

#     iLocation = ctypes.c_int(iLocation) 
#     IWFM_dll.IW_Budget_GetTitleLines(ctypes.byref(NTitles),
#                                      ctypes.byref(iLocation),
#                                      ctypes.byref(FactArea),
#                                      LengthUnit,
#                                      AreaUnit,
#                                      VolumeUnit,
#                                      ctypes.byref(iLenUnit),
#                                      cAltLocName,
#                                      ctypes.byref(iLenAltLocName),
#                                      cTitles,
#                                      ctypes.byref(iLenTitles),
#                                      iLocArray,
#                                      ctypes.byref(iStat))
    
#     if iStat.value == 0:
#         return iLen.value
#     else:
#         print("Error")
#     return


#########################################################
##################### ZBudget Group #####################
#########################################################
# no ZBudget functions yet! Check back later :)





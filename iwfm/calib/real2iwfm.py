# real2iwfm.py
# Read parameter values for model nodes and combine into an IWFM
# overwrite file
# Copyright (C) 2020-2023 University of California
# Based on a PEST utility written by Matt Tonkin
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------




def real2iwfm(verbose=False):
    '''  real2iwfm() - prompts the user for the no. of layers (nlay) in
         and IWFM model application; and the no. of parameter types (ntype)
         for which pilot points have been employed in order to define node
         values. program real2iwfm then prompts for (nlay*ntype) file names
         where each of these files is the output from running program
         ppk2fac_iwfm in order to use pilot points to define nodal parameter
         values. These files are formatted with a header indicating the number
         of nodes that are in the full IWFM application, and the number of nodes
         that are 'informed' by the contents of that file on the basis of
         pilot points. program real2iwfm then concatenates these files, for each
         layer and for each parameter type, into a file compatible with the new
         IWFM external node-value replacement file designed by Can Dogrul.

         From REAL2IGSM.F90 by Matt Tonkin, with modifications by others

    Parameters
    ----------
    verbose : bool, default=False
        Print to screen?

    '''

    import sys
    import iwfm as iwfm

    param_types = ['PKH', 'PS', 'PN', 'PV', 'PL', 'SCE', 'SCI']
    # factors for scaling parameters = 1.0 unless otherwise
    factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    if verbose:
        print(' Program REAL2IWFM reformats the outputs of one or more  ')
        print(' output files from FAC2REALI into a node overwrite file that can ')
        print(' be read by IWFM.')

    new_file = input(
        'Create a new overwrite file from scratch [y/n]? : ').lower()

    if new_file[0] == 'n':
        updatef = True
        overwrite_file = input('Name of existing overwrite file: ')
        iwfm.file_test(overwrite_file)

    else:
        updatef = False
        overwrite_file = input('Name of new overwrite file: ')

    nlay = int(input('Number of model layers: '))

    nnodes = int(input('Number of nodes with parameter values: '))

    ctime = input('Parameter time-step units: ')

    if updatef:
        nwrite, factors, ctime, parvals = read_overwrite_file(
            overwrite_file, nnodes, nlay, len(param_types), verbose)

    parvals, parnodes = [], []
    for ptype in param_types:
        ans = input(f'\n Include data for parameter type {ptype}? [y/n]').lower()

        pvals, pnodes = [], []
        if ans[0] == 'y':

            for layer in range(0, nlay):

                param_file = input(
                    f'\n Parameter value file for parameter type {ptype}, layer {layer+1}, or \'none\': ')

                layer_vals, layer_nodes = [], []
                if param_file == 'none':
                    layer_vals, layer_nodes = [-1.0] * nnodes, [-1] * nnodes

                else:
                    iwfm.file_test(param_file)
                    file_lines = open(param_file).read().splitlines()
                    for line in file_lines:
                        text = line.split()
                        layer_nodes.append(int(text[1]))
                        layer_vals.append(float(text[3]))
                    if verbose:
                        print(
                            f' Read values for {len(file_lines)} nodes from {param_file}')

                pvals.append(layer_vals)
                pnodes.append(layer_nodes)

        else:
            pvals.append([-1] * nnodes)
            pnodes.append(list(range(1,nnodes+1)))

        parvals.append(pvals)
        parnodes.append(pnodes)





    write_overwrite_file(overwrite_file, parnodes, nlay, param_types, parvals, factors, ctime, verbose)

    if verbose:
        print(f' Overwrite file {overwrite_file} has been written. If this was created on ')
        print( ' the basis of an existing overwrite file, the scaling factors from that ')
        print( ' file have been preserved. If it was created from scratch, all scaling ')
        print( ' factors have been set equal to 1. In each case this assumes that the ')
        print( ' user has correctly accounted for the scaling.')

    return
# --------------------------------------------------------------------------------






def write_overwrite_file(overwrite_file, parnodes, nlay, partypes, parvals, fp, ctime, verbose=False):
    '''  write_overwrite_file() - receive a list of parameters and write them to 
         an IWFM-2015 overwrite file    

         From REAL2IGSM.F90 by Matt Tonkin, with modifications by others

    Parameters
    ----------
    overwrite_file : str
        Overwrite file name

    parnodes : list
        Node numbers corresponding to paramvals items

    nlay : int
        Number of model layers

    partypes : list of strs
        Parameter type codes

    parvals : list
        Parameter values

    factors : list
        Multiplier actors

    ctime : str
        Time step in DSS format

    verbose : bool, default=False
        Print to screen?

    '''

    header1 =['C*******************************************************************************', \
        'C',\
        'C               INTEGRATED WATER FLOW MODEL (IWFM)', 'C', \
        'C*******************************************************************************', \
        'C', \
        'C               AQUIFER PARAMETER OVER-WRITE DATA FILE', \
        'C                       Groundwater Component', \
        'C                         *** Version 2015 ***', \
        'C', \
        'C', \
        'C             Project : ', \
        'C             Filename: ', \
        'C', \
        'C*******************************************************************************', \
        'C                           File Description', 'C', \
        'C   This data file contains node and layer numbers, and associated parameter', \
        'C   values to over-write values specified in the Groundwater Parameter Data File.', \
        'C', \
        'C*******************************************************************************', \
        'C               Over-writing Parameter Value Data Specifications', 'C', \
        'C   NWRITE; Total number of groundwater nodes at which previously defined', \
        'C            parameter values will be over-written.', 'C', \
        'C-------------------------------------------------------------------------------', \
        'C   VALUE                       DESCRIPTION', \
        'C-------------------------------------------------------------------------------']

    header2 =['C-------------------------------------------------------------------------------', \
        'C', \
        'C         Conversion factors for over-writing parameter values', \
        'C', \
        'C   FKH   ;  Conversion factor for horizontal hydraulic conductivity', \
        'C              It is used to convert only the spatial component of the unit; ', \
        'C              DO NOT include the conversion factor for time component of the unit.', \
        'C              * e.g. Unit of hydraulic conductivity listed in this file = IN/DAY', \
        'C                     Consistent unit used in simulation                 = FT/MONTH ', \
        'C                     Enter FKH (IN/MONTH -> FT/MONTH)                   = 8.33333E-02 ', \
        'C                      (conversion of DAY -> MONTH is performed automatically) ', \
        'C   FS    ;  Conversion factor for specific storage coefficient', \
        'C   FN    ;  Weighting factor for specific yield value', \
        'C   FV    ;  Conversion factor for aquitard vertical hydraulic conductivity', \
        'C              It is used to convert only the spatial component of the unit;', \
        'C              DO NOT include the conversion factor for time component of the unit.', \
        'C              * e.g. Unit of hydraulic conductivity listed in this file = IN/DAY', \
        'C                     Consistent unit used in simulation                 = FT/MONTH ', \
        'C                     Enter FKH (IN/MONTH -> FT/MONTH)                   = 8.33333E-02 ', \
        'C                      (conversion of DAY -> MONTH is performed automatically) ', \
        'C   FL    ;  Conversion factor for aquifer vertical hydraulic conductivity', \
        'C              It is used to convert only the spatial component of the unit; ', \
        'C              DO NOT include the conversion factor for time component of the unit.', \
        'C              * e.g. Unit of hydraulic conductivity listed in this file = IN/DAY', \
        'C                     Consistent unit used in simulation                 = FT/MONTH', \
        'C                     Enter FKH (IN/MONTH -> FT/MONTH)                   = 8.33333E-02 ', \
        'C                      (conversion of DAY -> MONTH is performed automatically) ', \
        'C   FSCE  ;  Conversion factor for elastic storage coefficient', \
        'C   FSCI  ;  Conversion factor for inelastic storage coefficient', \
        'C   TUNITKH;  Time unit of horizontal hydraulic conductivity.  This should be one of the units ', \
        'C              recognized by HEC-DSS that are listed in the Main Control File.  ', \
        'C   TUNITV ;  Time unit of aquitard vertical conductivity.  This should be one of the units ', \
        'C              recognized by HEC-DSS that are listed in the Main Control File.  ', \
        'C   TUNITL ;  Time unit of aquifer vertical conductivity.  This should be one of the units ', \
        'C              recognized by HEC-DSS that are listed in the Main Control File.  ', \
        'C', \
        'C    *** NOTE: This file created by utility program REAL2IWFM   ***',  \
        'C    *** NOTE:      All factors set to 1.0                      ***', \
        'C', \
        'C-----------------------------------------------------------------------------------------------------', \
        'C  FKH            FS             FN             FV             FL             FSCE           FSCI', \
        'C-----------------------------------------------------------------------------------------------------' ]

    header3 =['C---------------------------------------------------------------------------', \
        'C     VALUE              DESCRIPTION', \
        'C---------------------------------------------------------------------------' ]

    header4 =['C---------------------------------------------------------------------------', \
        'C', \
        'C   The following lists the groundwater nodenumber, aquifer layer number and', \
        'C    associated parameter values that will over-write the previously defined', \
        'C    values.', \
        'C    *** Enter -1.0 not to over-write the previously set values ***', \
        'C    *** NOTE: This file created by utility program REAL2IWFM   ***', 
        'C   ID   ;   Groundwater node number', 'C   LAYER;   Aquifer layer', \
        'C   PKH  ;   Hydraulic conductivity; [L/T]', 'C   PS   ;   Specific storage; [1/L]', \
        'C   PN   ;   Specific yield; [L/L]', \
        'C   PV   ;   Aquitard vertical hydraulic conductivity; [L/T]', \
        'C   PL   ;   Aquifer vertical hydraulic conductivity; [L/T]', \
        'C   SCE  ;   Elastic storage coefficient; [1/L]', \
        'C   SCI  ;   Inelastic storage coefficient; [1/L]', \
        'C            *Note* The above land subsidence parameters are only for interbed', \
        'C                    layers (i.e. clay layers)', \
        'C', \
        'C-------------------------------------------------------------------------------------------------------------------', \
        'C                Hydr.          Spec.          Spec.         Aquitard       Aquifer       Elastic       Inelastic', \
        'C                cond.          Stor.          Yld.           Vert. K       Vert. K      Stg. Coef.     Stg. Coef', \
        'C  ID   LAYER     PKH            PS             PN              PV             PL           SCE            SCI', \
        'C-------------------------------------------------------------------------------------------------------------------']

    with open(overwrite_file, 'w') as f:
        for h in header1:
            f.write(f'{h}\n')

        f.write(f'    {len(parnodes[0][0])}                       / NWRITE\n')


        for h in header2:
            f.write(f'{h}\n')

        f.write(f'\t{fp[0]}\t{fp[1]}\t{fp[2]}\t{fp[3]}\t{fp[4]}\t{fp[5]}\t{fp[6]}\n')

        for h in header3:
            f.write(f'{h}\n')

        f.write(f'    {ctime}               / TUNITKH\n')
        f.write(f'    {ctime}               / TUNITV \n')
        f.write(f'    {ctime}               / TUNITL \n')

        for h in header4:
            f.write(f'{h}\n')

        for n in range(0, len(parnodes[0][1])):           # cycle through nodes
            for l in range(0, nlay):
                for p in range(0, len(partypes)): 
                    pkh = parvals[0][l][n]
                    ps  = parvals[1][l][n]
                    pn  = parvals[2][l][n]
                    pv  = parvals[3][l][n]
                    pl  = parvals[4][l][n]
                    sce = parvals[5][l][n]
                    sci = parvals[6][l][n]
                f.write(f'\t{parnodes[0][l][n]}\t{l+1}\t{pkh}\t{ps}\t{pn}\t{pv}\t{pl}\t{sce}\t{sci}\n')

    return
# --------------------------------------------------------------------------------





def read_overwrite_file(overwrite_file, verbose=False):
    '''  read_overwrite_file() - open and read an IWFM-2015 overwrite file    

         From REAL2IGSM.F90 by Matt Tonkin, with modifications by others

    Parameters
    ----------
    overwrite_file : str
        Overwrite file name

    verbose : bool, default=False
        Print to screen?

    Returns
    -------
    nwrite : int
        number of model nodes

    factors : list
        multiplication factors
    
    ctime : str
        date in DSS format
    
    '''

    import iwfm as iwfm
    in_lines = open(overwrite_file).read().splitlines()               # open and read input file

    line_index = iwfm.skip_ahead(line_index,in_lines,0)               # skip comments 
    nwrite = int(in_lines[line_index].split()[0])                     # no. of nodes

    line_index = iwfm.skip_ahead(line_index,in_lines,1)               # skip comments
    factors = in_lines[line_index]

    line_index = iwfm.skip_ahead(line_index,in_lines,1)
    ctime = int(in_lines[line_index].split()[0])                      # time unit in DSS format

    return nwrite, factors, ctime
# --------------------------------------------------------------------------------



if __name__ == "__main__":
    ''' Run real2iwfm() from command line '''
    import iwfm.debug as idb

    idb.exe_time()  # initialize timer
    real2iwfm(verbose=False)
    print('\n')
    idb.exe_time()  # print elapsed time


# iwfm_lu2refined.py
# Modify IWFM land use files for a scenario
# Copyright (C) 2020-2024 University of California
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

def refined_lu_factors(orig_elems_file,refined_elems_file,elem2elem_file):
    ''' refined_lu_factors() - Calculate land use factors for refined model elements

    Parameters
    ----------
    orig_elems_file : str
        original model element areas file name

    refined_elems_file : str
        refined model element areas file name

    elem2elem_file : str
        element to element file name

    Returns
    -------
    lu_factors : list
        list of land use factors for refined model elements

    '''

    import csv
    import numpy as np
    import pandas as pd

    # -- read the original model element areas file
    with open(orig_elems_file, 'r') as file:
        orig_elems = list(csv.reader(file))[1:]
    for line in orig_elems:
        line[0], line[1] = int(line[0]), float(line[1])
    orig_elems_d = dict(orig_elems)

    # -- read the refined model element areas file
    with open(refined_elems_file, 'r') as file:
        refined_elems = list(csv.reader(file))[1:]
    for line in refined_elems:
        line[0], line[1] = int(line[0]), float(line[1])

    # -- read the element to element file
    with open(elem2elem_file, 'r') as file:
        elem2elem = list(csv.reader(file))[1:]
    for line in elem2elem:
        line[0], line[1] = int(line[0]), int(line[1])
    elem2elem_d = dict(elem2elem)

    # -- calculate the land use factors
    lu_factors = []
    for elem in refined_elems:
        refined_elem, refined_area = elem[0], elem[1]
        orig_elem = elem2elem_d[refined_elem]
        orig_area = orig_elems_d[orig_elem]
        lu_factors.append([refined_elem, orig_elem, refined_area / orig_area ]) 

    return lu_factors

def iwfm_lu2refined(in_lu_file,lu_factors,verbose=False):
    ''' iwfm_lu2refined() - Modify IWFM land use file for a refined model

    Parameters
    ----------
    in_lu_file : str
        IWFM Land Use file name

    lu_factors : list
        list of land use factors for refined model elements

    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import os
    import re
    import iwfm as iwfm


    # read the original IWFM Land Use file
    lu_lines = open(in_lu_file).read().splitlines()  # open and read input file
    line_index = iwfm.skip_ahead(0, lu_lines, 4)  # skip comments and header

    # open the output land use file
    out_lu_file_name = os.path.basename(in_lu_file).split('.')[0]+'_refined.dat'
    out_lu_file = open(out_lu_file_name, 'w')

    # write the header to the new land use file
    for line in range(line_index):
        out_lu_file.write(lu_lines[line]+'\n')

    # get number of time periods in the original land use file
    ntimes = 0
    l_index = line_index
    while l_index < len(lu_lines):
        if re.search('/', lu_lines[l_index]):
            ntimes += 1
        l_index += 1

    # get the number of lines per time period
    nlines = int((len(lu_lines) - line_index) / ntimes)


    # step through time periods, reading the original land use file and writing the new land use file
    for time_period in range(0,ntimes):
        orig_land_use = {}
        # get date from the first line of the time period
        for line in range(0,nlines):
            this_line = lu_lines[line_index].split()

            if len(orig_land_use) == 0:                 # first line contains date
                this_date = this_line.pop(0)
                if verbose: print(f'  Processing {this_date}')

            key = int(this_line[0])
            vals = []
            for item in this_line[1:]:
                vals.append(float(item))
            orig_land_use[key] = vals
            line_index += 1

        # write one time period of land use data to the new land use file
        count = 0
        for factor in lu_factors:
            refined_elem, orig_elem, area_mult = factor[0], factor[1], factor[2]

            orig_areas = orig_land_use[orig_elem]
            new_areas = [round(orig_areas[i]*area_mult,3) for i in range(0,len(orig_areas))]

            new_areas_txt = '\t'.join([str(i) for i in new_areas])

            if count == 0:  # first element -> add date
                new_areas_txt = this_date + '\t' + str(refined_elem) + '\t' + new_areas_txt
            else:
                new_areas_txt = '\t' + str(refined_elem) + '\t' + new_areas_txt

            out_lu_file.write(f'{new_areas_txt}\n')
            count += 1

    out_lu_file.close()

    if verbose: print(f'  Wrote {ntimes} time periods of land use data to {out_lu_file_name}')

    return


if __name__ == '__main__':
    ' Run iwfm_lu2refined() from command line '
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    args = sys.argv
    verbose=True


    if len(args) > 1:  # arguments are listed on the command line
        orig_elems_file = args[1]
        refined_elems_file = args[2]
        elem2elem_file = args[3]
        in_lu_file = args[4]
    else:  # ask for file names from terminal
        orig_elems_file  = input('Original model element areas file name (csv): ')
        refined_elems_file   = input('Refined model element areas file name (csv): ')
        elem2elem_file = input('Element to element file name (csv): ')
        in_lu_file = input('IWFM Land Use file name (dat): ')

    iwfm.file_test(orig_elems_file)
    iwfm.file_test(refined_elems_file)
    iwfm.file_test(elem2elem_file)
    iwfm.file_test(in_lu_file)

    idb.exe_time()  # initialize timer

    lu_factors = iwfm.refined_lu_factors(orig_elems_file,refined_elems_file,elem2elem_file)

    iwfm_lu2refined(in_lu_file,lu_factors,verbose=verbose)
    
    idb.exe_time()  # print elapsed time

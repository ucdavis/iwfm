# read_wells.py
# Reads from Groundwater.dat file and builds a dictionary of groundwater hydrograph
# info and gwhyd_sim columns, and returns the dictionary
# Copyright (C) 2020-2026 University of California
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


def read_wells(infile):
    ''' read_wells() - Read IWFM Groundwater.dat file and build a dictionary
        of groundwater hydrograph info and gwhyd_sim columns

    Parameters
    ----------
    infile : str
        IWFM Groundwaer.dat file name

    Returns
    -------
    well_dict : dictionary
        key = well name (i.e. state ID), values = simulated heads

    '''
    import iwfm as iwfm

    with open(infile) as f:
        gwhyd_info = f.read().splitlines() 

    # skip to NOUTH, number of hydrographs
    line_index = iwfm.skip_ahead(1, gwhyd_info, 20)  
    nouth = int(gwhyd_info[line_index].split()[0])

    well_dict = {}
    line_index = iwfm.skip_ahead(line_index, gwhyd_info, 3)  # skip to first hydrograph
    for i in range(0, nouth): 
        items = []
        line = gwhyd_info[line_index].split()
        items.append(line[5].upper())  # well name = key
        items.append(int(line[0]))     # column number in hydrograph file
        items.append(float(line[3]))   # x
        items.append(float(line[4]))   # y
        items.append(int(line[2]))     # model layer
        items.append(line[5].lower())  # well name (state well number)
        key, values = items[0], items[1:]
        well_dict[key] = values
        line_index = line_index + 1
    return well_dict

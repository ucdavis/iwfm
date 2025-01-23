# read_hyd_dict.py
# R Read hydrograph info from Groundwater.dat file and build a dictionary of 
# groundwater hydrograph info
# Copyright (C) 2020-2025 University of California
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


def read_hyd_dict(gw_dat_file):
    ''' read_hyd_dict() -  Read hydrograph info from Groundwater.dat file and build
        a dictionary of groundwater hydrograph info

    Parameters
    ----------
    gw_dat_file : str
        IWFM Groundwaer.dat file name

    Returns
    -------
    well_dict : dictionary
        key = well name (i.e. state well ID), value = well information, 
                                
    '''
    import iwfm as iwfm

    well_dict = {}
    gwhyd_info = open(gw_dat_file).read().splitlines()  # open and read input file

    # skip to NOUTH, number of hydrographs
    line_index = iwfm.skip_ahead(1, gwhyd_info, 20)  
    nouth = int(gwhyd_info[line_index].split()[0])

    line_index = iwfm.skip_ahead(line_index, gwhyd_info, 3)  # skip to first hydrograph
    for i in range(0, nouth): 
        items = []
        line = gwhyd_info[line_index].split()
        items.append(line[5])          # well name = key
        items.append(int(line[0]))     # column number in hydrograph file
        items.append(float(line[3]))   # x
        items.append(float(line[4]))   # y
        items.append(int(line[2]))     # model layer
        items.append(line[5].lower())  # well name
        well_dict[items[0]] = items[1:]
        line_index += 1
    return well_dict

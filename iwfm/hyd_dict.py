# hyd_dict.py
# Read Groundwater.dat file and return dictionary of well info
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


def hyd_dict(gwhyd_info_file):
    ''' hyd_dict() - Read hydrograph info from Groundwater.dat file and build
        a dictionary of groundwater hydrograph info

    Parameters
    ----------
    gwhyd_info_file : str
        IWFM Groundwaer.dat file name

    Returns
    -------
    well_dict : dictionary
        key = well name (i.e. state well ID), value = well information,

    '''
    import iwfm

    well_dict = {}
    iwfm.file_test(gwhyd_info_file)
    with open(gwhyd_info_file) as f:
        gwhyd_info = f.read().splitlines()  # open and read input file

    # skip to NOUTH, number of hydrographs
    line_index = iwfm.skip_ahead(1, gwhyd_info, 20)
    nouth = int(gwhyd_info[line_index].split()[0])

    line_index = iwfm.skip_ahead(line_index, gwhyd_info, 3)  # skip to first hydrograph (skips NOUTH, FACTXY, GWHYDOUTFL)
    for i in range(0, nouth):
        items = []
        line = gwhyd_info[line_index].split()

        # Handle both HYDTYP formats:
        # HYDTYP=0 (X-Y coordinates): 6 fields [ID, HYDTYP, LAYER, X, Y, NAME]
        # HYDTYP=1 (node number): 5 fields [ID, HYDTYP, LAYER, NODE, NAME]
        if len(line) >= 6:
            # HYDTYP=0 format with X-Y coordinates
            items.append(line[5].lower())  # well name = key
            items.append(int(line[0]))     # column number in hydrograph file
            items.append(float(line[3]))   # x
            items.append(float(line[4]))   # y
            items.append(int(line[2]))     # model layer
            items.append(line[5].lower())  # well name
        else:
            # HYDTYP=1 format with node number
            items.append(line[4].lower())  # well name = key
            items.append(int(line[0]))     # column number in hydrograph file
            items.append(0.0)              # x (not available for node format)
            items.append(0.0)              # y (not available for node format)
            items.append(int(line[2]))     # model layer
            items.append(line[4].lower())  # well name

        well_dict[items[0]] = items[1:]
        line_index += 1
    return well_dict

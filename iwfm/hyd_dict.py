# hyd_dict.py
# Read Groundwater.dat file and return dictionary of well info
# Copyright (C) 2020-2021 Hydrolytics LLC
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
    """ hyd_dict() - Read hydrograph info from Groundwater.dat file and build
        a dictionary of groundwater hydrograph info

    Parameters:
      gwhyd_info_file (str):  IWFM Groundwaer.dat file name

    Returns:
      well_dict       (dict): Dictionary of well information, 
                                key = state well ID
    """
    import iwfm as iwfm

    well_dict = {}
    gwhyd_info = open(gwhyd_info_file).read().splitlines()  # open and read input file
    line_index = 1  # skip first line
    line_index = iwfm.skip_ahead(
        line_index, gwhyd_info, 20
    )  # skip to NOUTH, number of hydrographs
    line = gwhyd_info[line_index].split()
    nouth = int(line[0])
    line_index = iwfm.skip_ahead(line_index, gwhyd_info, 3)  # skip to first hydrograph
    for i in range(0, nouth):  # open(gwhyd_list_file, 'r') as f:
        items = []
        line = gwhyd_info[line_index].split()
        items.append(line[5].lower())  # state well number = key
        items.append(int(line[0]))     # column number in hydrograph file
        items.append(float(line[3]))   # x
        items.append(float(line[4]))   # y
        items.append(int(line[2]))     # model layer
        items.append(line[5].lower())  # state well number
        key, values = items[0], items[1:]
        well_dict[key] = values
        line_index = line_index + 1
    return well_dict

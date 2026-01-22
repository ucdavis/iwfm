# read_sim_wells.py
# Read observation well information from IWFM Groundater.dat file
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


def read_sim_wells(gw_file, verbose=False):
    ''' read_sim_wells() - Read Groundwater.dat file and build a dictionary of
        groundwater hydrograph info and gwhyd_sim columns, and returns the
        dictionary

    Parameters
    ----------
    gw_file : str
        IWFM Groundwater.dat file name

    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------
    well_dict : dictionary
        key = well name, values = well information (hydrograph file column,
        x, y, model layer, well name)

    well_list : list
        list of well names

    '''
    import iwfm
    from iwfm.file_utils import read_next_line_value

    if verbose: print(f"Entered read_sim_wells() with {gw_file}")

    well_dict, well_list = {}, []
    with open(gw_file) as f:
        gwhyd_info = f.read().splitlines()

    # skip to NOUTH, number of hydrographs (skip 20 non-comment lines after start)
    nouth_str, line_index = read_next_line_value(gwhyd_info, 0, skip_lines=20)
    nouth = int(nouth_str)

    # skip to first hydrograph (skip 3 lines: NOUTH, FACTXY, GWHYDOUTFL)
    _, line_index = read_next_line_value(gwhyd_info, line_index, skip_lines=2)

    for i in range(0, nouth):
        items, line = [], gwhyd_info[line_index].split()
        items.append(line[5].upper())  # state well number = key
        items.append(int(line[0]))     # column number in hydrograph file
        items.append(float(line[3]))   # x
        items.append(float(line[4]))   # y
        items.append(int(line[2]))     # model layer
        items.append(line[5].lower())  # well name (state well number)
        well_dict[items[0]] = items[1:]
        well_list.append(items[0])
        line_index += 1

    if verbose: print(f"Leaving read_sim_wells()")

    return well_dict, well_list

# read_obs_wells.py
# Read a PEST-style settings file
# Copyright (C) 2018-2026 University of California
# Based on a PEST utility written by John Doherty
#-----------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------


def read_obs_wells(gw_file):
    ''' read_obs_wells() read observation well information from the Groundwater.dat file
                and return a dictionary of groundwater hydrograph info and gwhyd_sim columns

    Parameters
    ----------
    gw_file : str
        name of Groundwater.dat file to read

    Returns
    -------
    well_dict : dict
        dictionary of groundwater hydrograph info, values are WellInfo instances
    '''
    import iwfm
    from iwfm.dataclasses import WellInfo

    well_dict = {}
    iwfm.file_test(gw_file)
    with open(gw_file) as f:
        gwhyd_info = f.read().splitlines()           # open and read input file
    line_index = iwfm.skip_ahead(1,gwhyd_info,20)            # skip to NOUTH, number of hydrographs
    line = gwhyd_info[line_index].split()
    nouth = int(line[0])

    line_index = iwfm.skip_ahead(line_index,gwhyd_info,3)    # skip to first hydrograph
    for i in range(0,nouth):                                 # process each hydrograph
        line = gwhyd_info[line_index].split()
        key = line[5]                 # well name = key
        well_dict[key] = WellInfo(
            column=int(line[0]),
            x=float(line[3]),
            y=float(line[4]),
            layer=int(line[2]),
            name=line[5].lower(),
        )
        line_index = iwfm.skip_ahead(line_index,gwhyd_info,1)
    return well_dict


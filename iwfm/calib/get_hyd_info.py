# get_hyd_info.py
# unpack control variables from file_dict for one hydrograph type
# Copyright (C) 2020-2021 University of California
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


def get_hyd_info(ftype,file_dict):
    ''' get_hyd_info() - unpack control variables from file_dict for one hydrograph type

    Parameters
    ----------
    ftype : str
        IWFM input file type

    file_dict : dictionary
        information for ftypes

    Returns
    -------
    hyd_file : str
        hydrograph file name

    hyd_names : list
        hydrograph names
    
    '''

    import os
    import iwfm as iwfm

    main_file = file_dict[ftype][0]   # IWFM input file
    colid     = file_dict[ftype][8]   # col no of observation site name
    skips     = file_dict[ftype][9]   # lines to skip, different for each ftype

    in_lines = open(main_file).read().splitlines()                      # open and read input file
    line_index = 5  # skip first few lines

    if ftype == 'Tile drains':
        # -- the first part of the tile drain file is different
        line_index = iwfm.skip_ahead(line_index,in_lines,0)
        td_no = int(in_lines[line_index].split()[0])                      # no. tile drain param rows
        line_index = iwfm.skip_ahead(line_index,in_lines,td_no + 3)            # skip tile drain parameters + 3 lines
        line_index = iwfm.skip_ahead(line_index,in_lines,1)
        sd_no = int(in_lines[line_index].split()[0])                      # no. subsurface irrigation points
        line_index = iwfm.skip_ahead(line_index,in_lines,sd_no + 4)            # skip subsurface irrigation params + 4  lines
    else:
        # -- all of the other types
        line_index = iwfm.skip_ahead(line_index,in_lines,skips[0])

    # -- get NOUT - number of hydrographs
    nout = int(in_lines[line_index].split()[0])

    # -- get hydrographs output file name
    line_index = iwfm.skip_ahead(line_index,in_lines,skips[1])
    hyd_file = in_lines[line_index].split()[0]
    if not os.path.isfile(hyd_file):                                    # test for input file
        iwfm.file_missing(hyd_file)                                            # stop

    # -- get hydrograph names and locations as list
    hyd_names = []
    for i in range(0,nout):
        line_index = iwfm.skip_ahead(line_index,in_lines,1)
        hyd_names.append(in_lines[line_index].split()[colid])

    return hyd_file, hyd_names

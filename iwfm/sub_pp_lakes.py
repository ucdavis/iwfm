# sub_pp_lakes.py
# Reads the lake file and returns information on lakes in the submodel
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


def sub_pp_lakes(lake_file, elem_list):
    ''' sub_pp_lakes() - Read the lake file and return information for
        lakes in the submodel

    Parameters
    ----------
    lake_file : str
        name of existing preprocessor lake file
    
    elem_list : list of ints
        list of existing model elements in submodel

    Returns
    -------
    lake_info : list
        description of each lake in the submodel
    
    have_lake : bool
        True if the submodel includes any lakes

    '''
    import iwfm as iwfm

    have_lake = False

    #print(f'  ==> elem_list: {elem_list}')
    elems = [int(e[0]) for e in elem_list]

    with open(lake_file) as f:
        lake_lines = f.read().splitlines()  # open and read input file

    # Check if first line has at least 2 characters before slicing
    if not lake_lines:
        raise ValueError("Lake file is empty")
    lake_type = lake_lines[0][1:] if len(lake_lines[0]) > 1 else ''

    line_index = iwfm.skip_ahead(0, lake_lines, 0)  # skip comments
    parts = lake_lines[line_index].split()
    if not parts:
        raise ValueError(f"{lake_file} line {line_index}: Expected number of lakes, got empty line")
    nlakes = int(parts[0])

    lake_info = []
    for lake in range(0, nlakes):
        line_index = iwfm.skip_ahead(line_index + 1, lake_lines, 0)
        temp = lake_lines[line_index].split()
        if len(temp) < 5:
            raise ValueError(
                f"{lake_file} line {line_index}: Expected at least 5 values for lake {lake}, got {len(temp)}"
            )
        nelake = int(temp[3])

        lake_elems = []
        if int(temp[4]) in elems:
            lake_elems.append(int(temp[4]))
        for elem in range(0, nelake - 1):
            line_index = iwfm.skip_ahead(line_index + 1, lake_lines, 0)
            parts = lake_lines[line_index].split()
            if not parts:
                raise ValueError(f"{lake_file} line {line_index}: Expected lake element ID, got empty line")
            e = int(parts[0])
            if e in elems:
                lake_elems.append(e)
        if len(lake_elems) > 0:  # at least one lake element in submodel
            have_lake = True
            lake_info.append(
                [
                    temp[0],
                    temp[1],
                    temp[2],
                    str(len(lake_elems)),
                    ' '.join(temp[5:]),
                    lake_elems,
                ]
            )

    return lake_info, have_lake

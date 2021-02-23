# sub_pp_lakes.py
# Reads the lake file and returns information on lakes in the submodel
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


def sub_pp_lakes(lake_file, elem_list):
    """sub_pp_lakes() reads the lake file and returns information for
        lakes in the submodel

    Parameters:
      lake_file      (str):  Name of existing preprocessor lake file
      elem_list      (ints): List of existing model elements in submodel

    Returns:
      lake_info      (list): Description of each lake in the submodel
      have_lake      (bool): Does the submodel include any lakes?

    """
    import iwfm as iwfm

    have_lake = False

    elems = []
    for e in elem_list:
        elems.append(int(e[0]))

    # -- read the lake file into array elem_lines
    lake_lines = open(lake_file).read().splitlines()  # open and read input file

    # -- determine lake file version
    lake_type = lake_lines[0][1:]

    # -- skip to number of lakes
    line_index = iwfm.skip_ahead(0, lake_lines, 0)  # skip comments
    nlakes = int(lake_lines[line_index].split()[0])

    # -- read in model lake info
    lake_info = []
    for lake in range(0, nlakes):
        line_index = iwfm.skip_ahead(line_index + 1, lake_lines, 0)  # skip comments
        temp = lake_lines[line_index].split()
        nelake = int(temp[3])

        lake_elems = []
        if int(temp[4]) in elems:
            lake_elems.append(int(temp[4]))
        for elem in range(0, nelake - 1):
            line_index = iwfm.skip_ahead(line_index + 1, lake_lines, 0)  # skip comments
            e = int(lake_lines[line_index].split()[0])  # element number
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

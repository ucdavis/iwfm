# sub_pp_lake_file.py
# Copies the old lake file and replaces the contents with those of the new
# submodel, and writes out the new file
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


def sub_pp_lake_file(lake_file, new_lake_file, lake_info):
    ''' sub_pp_lake_file() - Copy the old lake file and replace the contents with
        those of the new model, and write out the new IWFM lake file

    Parameters
    ----------
    lake_file : str
        name of existing preprocessor node file
    
    new_lake_file : str
        name of submodel preprocessor node file
    
    lake_info : list
        info describing of each lake in the submodel

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    lake_lines = open(lake_file).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, lake_lines, 0)  # skip comments
    lake_lines[line_index] = iwfm.pad_both(str(len(lake_info)), f=4, b=35) + ' '.join(
        lake_lines[line_index].split()[1:]
    )

    line_index = iwfm.skip_ahead(line_index + 1, lake_lines, 0)

    new_lake_lines = lake_lines[:line_index]

    for i in range(0, len(lake_info)):
        new_lake_lines.append(
            '\t'
            + '\t'.join(lake_info[i][0:4])
            + '\t'
            + str(lake_info[i][5][0])
            + '\t'
            + lake_info[i][4]
        )

        for j in range(1, len(lake_info[i][5])):
            new_lake_lines.append('\t\t\t\t\t' + str(lake_info[i][5][j]))

    new_lake_lines.append('')

    with open(new_lake_file, 'w') as outfile:
        outfile.write('\n'.join(new_lake_lines))

    return

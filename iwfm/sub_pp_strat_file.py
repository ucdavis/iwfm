# sub_pp_strat_file.py
# Copies the old strat file and replaces the contents with those of the new
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


def sub_pp_strat_file(strat_file, new_strat_file, node_list):
    """sub_pp_strat_file() copies the old stratigraphy file and
        replaces the contents with those of the new submodel,
        and writes out the new file

    Parameters:
      strat_file     (str):  Name of existing preprocessor stratigraphy file
      new_strat_file (str):  Name of submodel preprocessor stratigraphy file
      node_list      (ints): List of submodel nodes

    Returns:
      nothing

    """
    import iwfm as iwfm

    # -- read the strat file into array strat_lines
    strat_lines = open(strat_file).read().splitlines()  # open and read input file

    while len(strat_lines[-1]) < 2:
        strat_lines.pop()

    line_index = iwfm.skip_ahead(0, strat_lines, 0)  # skip comments
    # -- skip layers and factor
    line_index = iwfm.skip_ahead(line_index + 3, strat_lines, 0)  # skip comments

    # -- copy strat_lines[:line_index] to new_strat_lines
    new_strat_lines = strat_lines[:line_index]

    # --  add lines for the nodes of the submodel
    for i in range(line_index, len(strat_lines)):
        if int(strat_lines[i].split()[0]) in node_list:
            new_strat_lines.append(strat_lines[i])

    new_strat_lines.append('')
    # -- write new strats file
    with open(new_strat_file, 'w') as outfile:
        outfile.write('\n'.join(new_strat_lines))

    return

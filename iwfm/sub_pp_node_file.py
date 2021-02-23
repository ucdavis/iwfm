# sub_pp_node_file.py
# Copies the old node file and replaces the contents with those of the new
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


def sub_pp_node_file(node_file, new_node_file, node_list):
    """sub_pp_node_file() - Copies the old node file and replaces the contents
        with those of the new model, and writes out the new file

    Parameters:
      node_file      (str):  Name of existing preprocessor node file
      new_node_file  (str):  Name of submodel preprocessor node file
      node_list      (ints): List of submodel nodes

    Returns:
      nothing

    """
    import iwfm as iwfm

    # -- read the node file into array node_lines
    node_lines = open(node_file).read().splitlines()  # open and read input file

    # -- number of nodes
    line_index = iwfm.skip_ahead(0, node_lines, 0)  # skip comments
    node_lines[line_index] = iwfm.pad_both(str(len(node_list)), f=4, b=35) + ' '.join(
        node_lines[line_index].split()[1:]
    )

    # -- skip factor
    line_index = iwfm.skip_ahead(line_index + 2, node_lines, 0)  # skip comments

    # -- copy node_lines[:line_index] to new_node_lines
    new_node_lines = node_lines[:line_index]

    # --  add lines for the nodes of the submodel
    for i in range(line_index, len(node_lines)):
        if int(node_lines[i].split()[0]) in node_list:
            new_node_lines.append(node_lines[i])

    new_node_lines.append('')
    # -- write new nodes file
    with open(new_node_file, 'w') as outfile:
        outfile.write('\n'.join(new_node_lines))

    return

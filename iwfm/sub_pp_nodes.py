# sub_pp_nodes.py
# Reads the element file and returns a list of the nodes in the submodel
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


def sub_pp_nodes(elem_file, elem_list):
    """sub_pp_nodes() reads the element file and returns a list of the
        nodes in the submodel

    Parameters:
      elem_file      (str):   Existing model preprocessor element file name
      elem_list      (ints):  List of existing model elements in submodel

    Returns:
      node_list      (ints):  List of existing model nodes in submodel

    """
    import iwfm as iwfm

    comments = ['Cc*#']
    elems = []
    for e in elem_list:
        elems.append(int(e[0]))

    # -- read the element file into array elem_lines
    elem_lines = open(elem_file).read().splitlines()  # open and read input file

    # -- skip to number of elements
    line_index = iwfm.skip_ahead(0, elem_lines, 0)  # skip comments
    # -- skip to number of subregions
    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments
    # -- skip to start of subregion list
    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments
    # -- skip the subregion lines
    while elem_lines[line_index][0] not in comments:
        line_index += 1
    # -- skip to start of element list
    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments

    # -- get node list
    node_list = []
    for i in range(line_index, len(elem_lines)):
        temp = [int(n) for n in elem_lines[i].split()]
        elem = temp[0]
        nodes = temp[1:5]
        if elem in elems:
            for node in nodes:
                if node not in node_list:
                    node_list.append(node)
    node_list.sort()
    if (
        node_list[0] == 0
    ):  # remove 0, it is not a node number, just indicates a triangular element
        node_list.pop(0)
    return node_list

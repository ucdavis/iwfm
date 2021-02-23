# iwfm_read_nodes.py
# read IWFM preprocessor nodes file
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


def iwfm_read_nodes(node_file):
    """ iwfm_read_nodes() - Read an IWFM Node file and return a list of the
        nodes and their coordinates

    Parameters:
      node_file       (str):  IWFM preprocessor node file

    Returns:
      node_coord      (list): Nodes and coordinates
      node_list       (list): Nodes
    """
    import iwfm as iwfm
    import re

    # -- read the Node file into array file_lines
    node_lines = open(node_file).read().splitlines()  # open and read input file

    line_index = 0  # start at the top
    line_index = iwfm.skip_ahead(line_index, node_lines, 0)  # skip comments

    inodes = int(re.findall("\d+", node_lines[line_index])[0])  # read no. nodes

    line_index = iwfm.skip_ahead(line_index + 1, node_lines, 0)  # skip comments

    factor = float(node_lines[line_index].split()[0])  # read factor

    line_index = iwfm.skip_ahead(line_index + 1, node_lines, 0)  # skip comments

    node_list = []
    node_coord = []
    for i in range(0, inodes):  # read nodes information
        l = node_lines[line_index + i].split()
        node_list.append(int(l.pop(0)))
        coords = [float(s) * factor for s in l]
        node_coord.append(coords)

    return node_coord, node_list

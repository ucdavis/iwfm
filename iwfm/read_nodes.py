# read_nodes.py 
# Read an IWFM Node file and return a list of the
# nodes and their coordinates
# Copyright (C) 2018-2026 University of California
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

# NOTE: Copied from the iwfm package file where it is already written
# NOTE: Changed to remove the id number from the split lists of each line
def read_nodes(node_file, factor=0.0):
    ''' read_nodes() - Read an IWFM Node file and return a list of the
        nodes and their coordinates

    Parameters
    ----------
    node_file : str
        IWFM preprocessor node file

    Returns
    -------
    node_coord : list
        Nodes and coordinates

    node_list : list
        Node numbers

    factor : float
        If factor = 0.0, use the factor from the input file
        Else if factor <> 0.0 use this as the factor

    '''
    import iwfm
    import re

    iwfm.file_test(node_file)

    with open(node_file) as f:
        node_lines = f.read().splitlines()  

    line_index = iwfm.skip_ahead(0, node_lines, 0)  

    inodes = int(re.findall('\d+', node_lines[line_index])[0])  

    line_index = iwfm.skip_ahead(line_index + 1, node_lines, 0) 

    read_factor = float(node_lines[line_index].split()[0])

    if factor == 0:
        factor = read_factor

    line_index = iwfm.skip_ahead(line_index + 1, node_lines, 0)  

    node_list, node_coord = [], []
    for i in range(inodes):  
        l = node_lines[line_index + i].split()
        l[0], l[1], l[2] = int(l[0]), float(l[1]), float(l[2])
        node_list.append(l[0])
        node_coord.append(l[1:])

    return node_coord, node_list

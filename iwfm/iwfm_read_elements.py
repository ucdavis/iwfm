# iwfm_read_elements.py
# read IWFM preprocessor elements file
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


def iwfm_read_elements(elem_file, verbose=False):
    ''' iwfm_read_elements() - Read an IWFM Element file, and return a list
        of the nodes making up each element

    Parameters
    ----------
    elem_file : str
        IWFM Preprocessor Elements file name

    Returns
    -------
    elem_ids : list
        element numbers
    
    elem_nodes : list
        nodes for each element
    
    elem_sub : list
        subregion for each element

    '''
    import re
    import iwfm as iwfm

    iwfm.file_test(elem_file)

    elem_lines = open(elem_file).read().splitlines()  
    line_index = iwfm.skip_ahead(0, elem_lines, 0) 

    elements = int(elem_lines[line_index].split()[0])  

    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  

    subregions = int(elem_lines[line_index].split()[0])  

    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  
    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, subregions - 1)

    elem_ids, elem_nodes, elem_sub = [], [], []
    for i in range(0, elements):  
        l = elem_lines[line_index + i].split()
        this_elem = int(l.pop(0))
        elem_ids.append(this_elem)
        nodes = [int(s) for s in l[0:5]]
        elem_sub.append(nodes.pop(4))
        if nodes[3] == 0:
            nodes.pop(3)  # remove empty node on triangles
        elem_nodes.append(nodes)
    if verbose:
        print(f'  Read {len(elem_nodes):,} elements from {elem_file}')
    return elem_ids, elem_nodes, elem_sub

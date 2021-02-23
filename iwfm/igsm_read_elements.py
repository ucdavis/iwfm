# igsm_read_elements.py
# Read an IGSM pre-processor element file
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


def igsm_read_elements(elem_file):
    """ igsm_read_elements() - Read an IGSM Element file, and returns a list
        of the nodes making up each element
    """
    import iwfm as iwfm

    # -- read the Element file into array file_lines
    elem_lines = open(elem_file).read().splitlines()  # open and read input file

    line_index = 0  # start at the top
    line_index = iwfm.skip_ahead(line_index, elem_lines, 0)  # skip comments

    import re

    elements = int(
        re.findall('\d+', elem_lines[line_index])[0]
    )  # read number of elements

    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments

    elem_nodes, elem_list = [], []
    for i in range(0, elements):  # read element information
        l = elem_lines[line_index + i].split()
        this_elem = int(l.pop(0))
        nodes = [int(s) for s in l]
        if nodes[3] == 0:
            nodes.pop(3)  # remove empty node on triangles
        elem_nodes.append(nodes)
        elem_list.append(this_elem)
    return elem_nodes, elem_list

# sub_remove_items.py
# Remove lines from IWFM input file block for components (elements, nodes, 
# stream nodes, etc) that are not in the submodel
# Copyright (C) 2020-2022 University of California
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


def sub_remove_items(file_lines, line_index, items, skip=0):
    '''sub_remove_items() - Remove lines for components (elements, nodes, stream 
       nodes, etc) that are not in the submodel

    Parameters
    ----------
    file_lines : list of strings
        each element is a line from the input file

    line_index : int
        starting line number for processing

    items : list of ints
        list of existing model compnents (elements, nodes, stream nodes, etc) in submodel

    skip : int, default=0
        turn command-line output on or offnumber of lines to skip in addition to comments

    Returns
    -------
    line_index: int
        ending line number after processing

    '''
    import iwfm as iwfm
    comments = ['C','c','*','#']

    line_index = iwfm.skip_ahead(line_index, file_lines, skip)       # skip comments
    if int(file_lines[line_index].split()[0]) > 0:
        while file_lines[line_index][0] not in comments:
            if int(file_lines[line_index].split()[0]) not in items:
                del file_lines[line_index]
            else:
                line_index += 1
    else:
        line_index += 1

    return line_index

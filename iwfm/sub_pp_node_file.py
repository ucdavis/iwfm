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
    ''' sub_pp_node_file() - Copy the original node file, replace the 
        contents with those of the new model, and write out the new file

    Parameters
    ----------
    node_file : str
        name of existing preprocessor node file
    
    new_node_file : str
        name of submodel preprocessor node file
    
    node_list : llist of ints
        list of submodel nodes

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    node_lines = open(node_file).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, node_lines, 0)  # skip comments
    node_lines[line_index] = iwfm.pad_both(str(len(node_list)), f=4, b=35) + ' '.join(
        node_lines[line_index].split()[1:])

    line_index = iwfm.skip_ahead(line_index + 2, node_lines, 0)

    new_node_lines = node_lines[:line_index]

    for i in range(line_index, len(node_lines)):
        if int(node_lines[i].split()[0]) in node_list:
            new_node_lines.append(node_lines[i])
    new_node_lines.append('')

    with open(new_node_file, 'w') as outfile:
        outfile.write('\n'.join(new_node_lines))

    return

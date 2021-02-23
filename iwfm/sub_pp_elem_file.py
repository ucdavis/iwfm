# sub_pp_elem_file.py
# Copies the old element file and replaces the contents with those of the new
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


def sub_pp_elem_file(elem_file, new_elem_file, elem_list, new_srs):
    """sub_pp_elem_file() copies the old element file and
        replaces the contents with those of the new model,
        and writes out the new file

    Parameters:
      elem_file      (str):  Name of existing preprocessor element file
      new_elem_file  (str):  Name of submodel preprocessor element file
      elem_list      (ints): List of submodel elements
      new_srs        (ints): List of submodel subregions

    Returns:
      nothing

    """
    import iwfm as iwfm

    comments = ['Cc*#']
    elems = []
    for e in elem_list:
        elems.append(e[0])

    # -- read the element file into array elem_lines
    elem_lines = open(elem_file).read().splitlines()  # open and read input file

    # -- number of elements
    line_index = iwfm.skip_ahead(0, elem_lines, 0)  # skip comments
    elem_lines[line_index] = iwfm.pad_both(str(len(elem_list)), f=4, b=35) + ' '.join(
        elem_lines[line_index].split()[1:]
    )

    # -- number of subregions
    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments
    elem_lines[line_index] = iwfm.pad_both(str(len(new_srs)), f=4, b=35) + ' '.join(
        elem_lines[line_index].split()[1:]
    )

    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments

    # -- replace the list of subregions (always <= length of original list)
    for sr in range(0, len(new_srs)):
        elem_lines[line_index] = iwfm.pad_both(
            'Subregion ' + str(new_srs[sr]), f=4, b=25
        ) + ' '.join(elem_lines[line_index].split()[2:])
        line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments
    # remove the remaining 'Subregion' lines
    while elem_lines[line_index][0] not in comments:
        del elem_lines[line_index]

    line_index = iwfm.skip_ahead(line_index + 1, elem_lines, 0)  # skip comments

    # -- copy elem_lines[:line_index] to new_elem_lines
    new_elem_lines = elem_lines[:line_index]

    # --  add lines for the elements of the submodel
    for i in range(line_index, len(elem_lines)):
        if int(elem_lines[i].split()[0]) in elems:
            new_elem_lines.append(elem_lines[i])

    new_elem_lines.append('')
    # -- write new preprocessor input file
    with open(new_elem_file, 'w') as outfile:
        outfile.write('\n'.join(new_elem_lines))

    return

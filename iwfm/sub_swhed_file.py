# sub_swhed_file.py
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


def sub_swhed_file(old_filename, new_filename, node_list, snode_list, verbose=False):
    """sub_swhed_file() reads the old small watershed file, determines which
        small watersheds are in the submodel, and writes out a new file

    Parameters:
      old_filename   (str):  Name of existing nmodel small watersheds file
      new_filename   (str):  Name of new subnmodel small watersheds file
      node_list      (ints): List of existing model nodes in submodel
      snode_list     (ints): List of existing model stream nodes in submodel
      verbose        (bool): Turn command-line output on or off

    Returns:
      nothing

    """
    import iwfm as iwfm

    # -- read the small watershed file into array swshwd_lines
    swshwd_lines = open(old_filename).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, swshwd_lines, 2)  # skip factors and comments

    # -- number of small watersheds
    nsw_line, nsw = line_index, int(swshwd_lines[line_index].split()[0])

    line_index = iwfm.skip_ahead(
        line_index + 4, swshwd_lines, 0
    )  # skip factors and comments

    sw_list = []
    for sw in range(0, nsw):  # small watershed descriptions
        change, line, items = 0, line_index, swshwd_lines[line_index].split()

        if int(items[4]) in node_list:  # if IWB in submodel keep small watershed
            sw_list.append(int(items[0]))  # ID

            if (
                int(items[2]) not in snode_list
            ):  # if IWBTS not in submodel, replace with '0'
                change, items[2] = 1, '0'

            for l in range(
                1, int(items[3])
            ):  # check that each arc node is in the submodel
                line_index = iwfm.skip_ahead(
                    line_index, swshwd_lines, 1
                )  # skip comments
                if (
                    int(swshwd_lines[line_index].split()[0]) not in snode_list
                ):  # remove this arc node and decrement nwb
                    del swshwd_lines[line_index]
                    change, items[3] = 1, str(int(items[3]) - 1)
                    line_index -= 1

            if change:
                swshwd_lines[line] = '\t'.join([i for i in items])

        else:  # remove these lines
            for i in range(0, int(items[3])):
                del swshwd_lines[line_index]
            line_index -= 1
        line_index = iwfm.skip_ahead(line_index, swshwd_lines, 1)  # skip comments

    if verbose:
        print(f'  ==> Kept {len(sw_list)} of {nsw} small watersheds')

    # replace NSW
    swshwd_lines[nsw_line] = iwfm.pad_both(str(len(sw_list)), f=6, b=50) + ' '.join(
        swshwd_lines[nsw_line].split()[1:]
    )

    line_index = iwfm.skip_ahead(
        line_index, swshwd_lines, 6
    )  # skip factors and comments

    for sw in range(
        0, nsw
    ):  # remove root zone parameters for small watersheds outside submodel
        if int(swshwd_lines[line_index].split()[0]) not in node_list:  # remove the line
            del swshwd_lines[line_index]
        line_index = iwfm.skip_ahead(line_index, swshwd_lines, 1)  # skip comments

    line_index = iwfm.skip_ahead(
        line_index, swshwd_lines, 3
    )  # skip factors and comments

    for sw in range(
        0, nsw
    ):  # remove aquifer parameters for small watersheds outside submodel
        if int(swshwd_lines[line_index].split()[0]) not in node_list:  # remove the line
            del swshwd_lines[line_index]
        line_index = iwfm.skip_ahead(line_index, swshwd_lines, 1)  # skip comments

    line_index = iwfm.skip_ahead(
        line_index, swshwd_lines, 1
    )  # skip factors and comments

    for sw in range(
        0, nsw
    ):  # remove initial conditions for small watersheds outside submodel
        if int(swshwd_lines[line_index].split()[0]) not in node_list:  # remove the line
            del swshwd_lines[line_index]
        line_index = iwfm.skip_ahead(line_index, swshwd_lines, 0)  # skip comments

    swshwd_lines.append('')
    # -- write submodel small watersheds file
    with open(new_filename, 'w') as outfile:
        outfile.write('\n'.join(swshwd_lines))

    return

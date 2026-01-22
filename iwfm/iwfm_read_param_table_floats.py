# iwfm_read_param_table_floats.py
# Read a table of integer parameters from a file and organize them into lists
# and return a numpy array of floats
# Copyright (C) 2020-2026 University of California
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


def iwfm_read_param_table_floats(file_lines, line_index, lines):
    """read_param_table_floats() - Read a table of integer parameters from a file and organize them into lists
                and return a numpy array of floats.

    Parameters
    ----------
    file_lines : list
        File contents as list of lines

    line_index : int
        The index of the line to start reading from.

    lines : int
        The number of lines to read.

    Returns
    -------

    params : list
        A list of parameters
    """

    import numpy as np
    from iwfm.file_utils import read_next_line_value

    params = []
    parts = file_lines[line_index].split()
    if int(parts[0]) == 0:                                              # one set of parameter values for all elements
        params = [float(e) for e in parts[1:]]                          # skip the first value which is the element number
        _, line_index = read_next_line_value(file_lines, line_index)    # skip to next value line
    else:
        for i in range(lines):
            parts = file_lines[line_index].split()
            params.append([float(e) for e in parts[1:]])                # skip the first value which is the element number
            line_index += 1                                             # skip to next line
    line_index -= 1

    params = np.array(params)

    return params, line_index

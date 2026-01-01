# read_gw_params.py
# Read groundwater parameters from a file and organize them into lists
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

def read_gw_params(file):
    """read_gw_params() - Read groundwater parameters from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the groundwater data.

    Returns
    -------
    kh : list
        A list containing hydraulic conductivity [L/T] values for each layer. It consists of four sublists,
        each representing a separate layer.

    ss : list
        A list containing specific storage [1/L] values for each layer. It follows the same structure as `kh`.

    sy : list
        A list containing specific yield [L/L] values for each layer. It follows the same structure as `kh`.

    kq : list
        A list containing aquitard vertical hydraulic conductivity [L/T] values for each layer. 
        It follows the same structure as `kh`.

    kv : list
        A list containing aquifer vertical hydraulic conductivity [L/T] values for each layer. 
        It follows the same structure as `kh`.

    """
    import iwfm


    #  Fild line number
    # TODO: Add functions to skip file contents to desired input, search for string not reliable
    desired = "C           ID         PKH          PS             PN          PV              PL"

    line_num = iwfm.find_line_num(file, desired)


    #  Lists for each parameter
    kh = [[0],[1],[2],[3]]
    ss = [[0],[1],[2],[3]]
    sy = [[0],[1],[2],[3]]
    kq = [[0],[1],[2],[3]]
    kv = [[0],[1],[2],[3]]

    #  Read the relevant lines of the Groundwater.dat file
    lines = iwfm.read_from_index(file, line_num + 2)
    
    #  Loop through all of the lines
    for i, values in enumerate(lines):
        #  Calculate layer number
        idx = i % 4

        #  Add values to their corresponding parameter's list
        kh[idx].append(float(values[0]))
        ss[idx].append(float(values[1]))
        sy[idx].append(float(values[2]))
        kq[idx].append(float(values[3]))
        kv[idx].append(float(values[4]))
    return kh, ss, sy, kq, kv
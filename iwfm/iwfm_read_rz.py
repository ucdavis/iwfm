# iwfm_read_rz.py 
# Read root zone parameters from a file and organize them into lists
# Copyright (C) 2023 University of California
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

def get_name(s):
    temp = s.split()[0]
    if temp[0] == '/':   # check for presence of file name
        name = 'none'
    else:
        name = temp
    return name


def iwfm_read_rz(file):
    """iwfm_read_rz() - Read root zone parameters from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the root zone data.
  
    Returns
    -------
    params : list
        A list containing parameter values. It consists of 13 sublists, each representing a different parameter.

    """

    # TODO: Add functions to skip file contents to desired input, search for string not reliable

    import iwfm as iwfm

    #  Find the number of the line with column labels, occurs before data but after comments
    desired = "C         IE     WP      FC      TN     LAMBDA    K    RHC  CSDTH     IRNE    FRNE    IMSRC  TYPDEST   DEST	PondedK"
    line_num = iwfm.find_line_num(file, desired)
    print(f'Line number: {line_num}')

    #  Lists for each parameter
    params = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
   
    #  Read the relevant lines of the RootZone.dat file
    lines = iwfm.read_from_index(file, line_num + 2)

    #  Loop through all of the lines
    for values in lines:
        values = values[1:]
        #  Add values to their corresponding parameter's list
        for idx, value in enumerate(values):
            params[idx].append(float(value))
        
    return params


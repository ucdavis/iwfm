# iwfm_read_rz_npc.py
# Read non-ponded crop data from a file and organize them into lists
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


def iwfm_read_rz_npc(file):
    """iwfm_read_rz_npc() - Read non-ponded crop data from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the non-ponded crop data.
  
    Returns
    -------
    wp : list
        A list of lists containing curve numbers for each grid element and crop combination. It consists of 20 sublists,
        each representing a different crop.
    """
    import iwfm as iwfm

    #  Find the number of the line with column labels, occurs before data but after comments
    desired = "GR      CO      SB      CN      DB      SA      FL      AL      PA      TP      TF      CU      OG      PO      TR      AP      OR      CS      VI      ID"
    line_num = iwfm.find_line_num(file, desired)

    #  Lists for each parameter
    crops = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19]]

    #  Read the relevant lines of the NonPondedCrop.dat file
    lines = iwfm.read_from_index(file, line_num + 2)
    
    #  Loop through all of the lines
    for values in lines:
        #  Add values to their corresponding parameter's list
        for idx, value in enumerate(values):
            crops[idx].append(float(value))
         
    return crops

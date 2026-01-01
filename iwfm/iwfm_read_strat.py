# iwfm_read_strat.py
# read IWFM preprocessor stratigraphy file
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


def iwfm_read_strat(strat_file, node_coords):
    ''' iwfm_read_strat() - Read an IWFM Stratigraphy file and return a 
        list of stratigraphy for each node
    
    Parameters:
    -----------
    strat_file : str
        name of existing IWFM stratigraphy file
    
    node_coords : list
        (x,y) locations of IWFM model nodes

    Returns
    -------
    strat : list
        stratigraphy for each node
    
    nlayers : int
        number of layers

    '''
    import iwfm as iwfm
    import re

    iwfm.file_test(strat_file)

    with open(strat_file) as f:
        strat_lines = f.read().splitlines()
    line_index = iwfm.skip_ahead(0, strat_lines, 0)

    layers = int(re.findall(r'\d+', strat_lines[line_index])[0])  

    line_index = iwfm.skip_ahead(line_index + 1, strat_lines, 0)
    factor = float(re.findall(r'[-+]?\d*\.?\d+', strat_lines[line_index])[0])

    line_index = iwfm.skip_ahead(line_index + 1, strat_lines, 0) 

    strat = []
    for i in range(0, len(node_coords)):
        l = strat_lines[line_index + i].split()
        s = []
        s.append(int(l.pop(0))) 
        for j in range(0, len(l)):
            s.append(factor * float(l.pop(0)))  
        strat.append(s)
    nlayers = int((len(strat[0]) - 1) / 2)
    return strat, nlayers

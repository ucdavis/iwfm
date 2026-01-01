# igsm_read_strat.py
# Read an IGSM pre-processor stratigraphy file
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


def igsm_read_strat(strat_file, node_coords):
    ''' igsm_read_strat() - Read an IGSM Stratigraphy file and return a list
        of stratigraphy for each node

    Parameters
    ----------
    strat_file : str
        IGSM nodal stratigraphy file name
    
    node_coords: list
        nodes and coordinates

    Returns
    -------
    strat : list
        stratigraphy information
    
    nlayers : int
        number of aquifer layers
    
    '''
    import iwfm as iwfm

    with open(strat_file) as f:
        strat_lines = f.read().splitlines() 

    strat_index = iwfm.skip_ahead(0, strat_lines, 0)  # skip comments
    layers = strat_lines[strat_index].split()[0]

    strat = []
    strat_index = iwfm.skip_ahead(strat_index + 1, strat_lines, 0)
    for i in range(0, len(node_coords)):
        s = []
        l = strat_lines[strat_index + i].split()
        s.append(int(l.pop(0)))
        for j in range(0, len(l)):
            s.append(float(l.pop(0)))
        strat.append(s)
    nlayers = int((len(strat[0]) - 1) / 2)
    return strat, nlayers

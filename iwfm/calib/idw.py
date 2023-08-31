# idw.py
# Inverse distance weighting... for what?
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

# ** INFOMPLETE ** #


def idw(x, y, elem, nnodes, nlayers, nodexy, elevations, debug=0):
    ''' idw() - Inverse distance weighting

    ** INCOMPLETE **
    TODO: only partially developed

    Parameters
    ----------
    x : list of floats
        X values of points
    
    y : list of floats
        y values of points
    
    elem : list
        list of model elements and nodes
    
    nnodes : list
        list of model nodes
    
    nlayers : int
        number of model layers
    
    nodexy : list
        spatial locations of nodes
    
    elevations : list
        Top row of table data in excel spreadsheets
    
    debug : int, default=0
        1 == Turn on debug printing to cli

    Returns
    -------
    nothing

    '''
    import numpy as np

    # inverse distance weighting
    if debug:
        print('\n  ==> iwfm.idw()')
        print(f'      =>  elem: \t{elem}')
        print(f'      =>  nnodes: \t{nnodes}')
        print(f'      =>  nlayers: \t{nlayers}')
        print(f'      =>  nodexy: \t{nodexy}')
        print(f'      =>  elevations: \t{elevations}')

    interp_values = [[0.0 for _ in nnodes] for _ in nlayers]

    if debug:
        print(f'      =>  interp_values: \t{interp_values}')

    for i in range(nlayers):
        if debug:
            print(f'\n      =>  i: \t{i}')
        wgt = 0
        for j in range(len(nnodes)):  # for each node of element
            if debug:
                print(f'\n      =>  j: \t{j}')
            # if elem > 0:   # all ObsElem > 0
            nodeID = nnodes[i]
            if debug:
                print(f'      =>  nodeID: \t{nodeID}')
            if nodeID > 0:
                if debug:
                    print(f'      =>  x, y: \t{x}, {y}')
                if debug:
                    print(f'      =>  nodexy[j]: \t{nodexy[j]}')
                distance = float(
                    np.sqrt((x - nodexy[j][0]) ** 2 + (y - nodexy[j][1]) ** 2)
                )
                if debug:
                    print(f'      =>  distance: \t{distance}')
                wgt_tmp = 1.0 / distance
                if debug:
                    print(f'      =>  wgt_tmp: \t{wgt_tmp}')
                wgt += wgt_tmp
                for k in range(nlayers):
                    if debug:
                        print(f'      =>  i: {i} \tk: {k}')
                    if debug:
                        print(f'      =>  interp_values[i][k]: \t{interp_values[i][k]}')
                    if debug:
                        print(f'      =>  elevations[i][k]: \t{elevations[i][k]}')
                    interp_values[i][k] += wgt_tmp * elevations[i][k]
                    if debug:
                        print(f'      =>  interp_values[i][k]: \t{interp_values[i][k]}')
        if debug:
            print(f'      =>  wgt: \t{wgt}')
        for k in range(nlayers):
            interp_values[i][k] = interp_values[i][k] / wgt
        if debug:
            print(f'      =>  interp_values: \t{interp_values}')

    if debug:
        print('\n  ** incomplete: IDW.py **')
    return interp_values

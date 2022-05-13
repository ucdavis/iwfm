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
        print('      =>  {}: \t{}'.format('elem', elem))
        print('      =>  {}: \t{}'.format('nnodes', nnodes))
        print('      =>  {}: \t{}'.format('nlayers', nlayers))
        print('      =>  {}: \t{}'.format('nodexy', nodexy))
        print('      =>  {}: \t{}'.format('elevations', elevations))

    InterpValues = [[0.0 for j in range(0, len(nnodes))] for i in range(0, nlayers)]
    if debug:
        print('      =>  {}: \t{}'.format('InterpValues', InterpValues))

    for i in range(0, nlayers):
        if debug:
            print('\n      =>  {}: \t{}'.format('i', i))
        wgt = 0
        for j in range(0, len(nnodes)):  # for each node of element
            if debug:
                print('\n      =>  {}: \t{}'.format('j', j))
            # if elem > 0:   # all ObsElem > 0
            nodeID = nnodes[i]
            if debug:
                print('      =>  {}: \t{}'.format('nodeID', nodeID))
            if nodeID > 0:
                if debug:
                    print('      =>  {}, {}: \t{}, {}'.format('x', 'y', x, y))
                if debug:
                    print('      =>  {}: \t{}'.format('nodexy[j]', nodexy[j]))
                Distance = float(
                    np.sqrt((x - nodexy[j][0]) ** 2 + (y - nodexy[j][1]) ** 2)
                )
                if debug:
                    print('      =>  {}: \t{}'.format('Distance', Distance))
                wgt_tmp = 1.0 / Distance
                if debug:
                    print('      =>  {}: \t{}'.format('wgt_tmp', wgt_tmp))
                wgt += wgt_tmp
                for k in range(0, nlayers):
                    if debug:
                        print('      =>  i: {} \tk: {}'.format(i, k))
                    if debug:
                        print(
                            '      =>  {}: \t{}'.format(
                                'InterpValues[i][k]', InterpValues[i][k]
                            )
                        )
                    if debug:
                        print(
                            '      =>  {}: \t{}'.format(
                                'elevations[i][k]', elevations[i][k]
                            )
                        )
                    InterpValues[i][k] += wgt_tmp * elevations[i][k]
                    if debug:
                        print(
                            '      =>  {}: \t{}'.format(
                                'InterpValues[i][k]', InterpValues[i][k]
                            )
                        )
        if debug:
            print('      =>  {}: \t{}'.format('wgt', wgt))
        for k in range(0, nlayers):
            InterpValues[i][k] = InterpValues[i][k] / wgt
        if debug:
            print('      =>  {}: \t{}'.format('InterpValues', InterpValues))

    if debug:
        print('\n  ** incomplete: IDW.py **')
    return InterpValues

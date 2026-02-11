# idw.py
# Inverse distance weighting... for what?
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

# ** INFOMPLETE ** #

from iwfm.debug.logger_setup import logger


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
    logger.debug(f'iwfm.idw() {elem=} {nnodes=} {nlayers=} {nodexy=} {elevations=}')

    interp_values = [[0.0 for _ in range(len(nnodes))] for _ in range(nlayers)]

    logger.debug(f'{interp_values=}')

    for i in range(nlayers):
        logger.debug(f'{i=}')
        wgt = 0
        for j in range(len(nnodes)):  # for each node of element
            logger.debug(f'{j=}')
            # if elem > 0:   # all ObsElem > 0
            nodeID = nnodes[i]
            logger.debug(f'{nodeID=}')
            if nodeID > 0:
                logger.debug(f'{x=}, {y=}, {nodexy[j]=}')
                distance = float(
                    np.sqrt((x - nodexy[j][0]) ** 2 + (y - nodexy[j][1]) ** 2)
                )
                logger.debug(f'{distance=}')
                wgt_tmp = 1.0 / distance
                logger.debug(f'{wgt_tmp=}')
                wgt += wgt_tmp
                for k in range(nlayers):
                    logger.debug(f'{i=} {k=} {interp_values[i][k]=} {elevations[i][k]=}')
                    interp_values[i][k] += wgt_tmp * elevations[i][k]
                    logger.debug(f'{interp_values[i][k]=}')
        logger.debug(f'{wgt=}')
        for k in range(nlayers):
            interp_values[i][k] = interp_values[i][k] / wgt
        logger.debug(f'{interp_values=}')

    logger.debug('** incomplete: IDW.py **')
    return interp_values

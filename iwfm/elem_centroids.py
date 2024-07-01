# elem_centroids.py
# Return a list of the element id and (x,y) coordinates for the centroid of each elememnt
# Copyright (C) 2020-2024 University of California
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


def elem_centroids(node_filename, elem_filename):
    ''' elem_centroids() - Return a list of element centroids
        in the form: [[x0,y0],[x1,y1],[x2,y2]<,...>]

    Parameters
    ----------
    nose_filename : str
        Path to node file
    
    elem_filename : str
        Path to elelment file
    

    Returns
    -------
    centroids : list
        list of element centroids
    
    '''
    import iwfm as iwfm

    node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_filename)

    elem_ids, elem_nodes, elem_sub = iwfm.iwfm_read_elements(elem_filename)
    
    centroids = iwfm.get_elem_centroids(elem_ids, elem_nodes, node_coords)#    print(f" ==> {node_coord[0:2]=}")

    return centroids

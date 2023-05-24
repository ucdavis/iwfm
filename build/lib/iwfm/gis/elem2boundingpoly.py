# elem2boundingpoly.py
# Create shapely Polygon of boundary for an IWFM model
# Copyright (C) 2020-2022 University of California
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


def elem2boundingpoly(elem_nodes, node_coords, verbose=False):
    ''' elem2boundingpoly() - Creates a shapely Polygon of the boundary of an IWFM model

    Parameters
    ----------
    elem_nodes : list
        list of elements and associated nodes
    
    node_coords : list
        list of nodes and associated X and Y coordinates
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    submodel_bounds : shapely Polygon
        Model boundary polygon

    '''
    import iwfm as iwfm
    from shapely.geometry import Point, Polygon
    from shapely.ops import unary_union

    # create dictionary of nodal coordinates
    d_nodes = {}
    for node in node_coords:
        key, values = node[0], [node[1], node[2]]
        d_nodes[key] = values


    # create a Polygon for each model element
    polys = []
    for elem in elem_nodes:  # for each element ...
        points = []
        for node in elem[1:5]:  # for each node in the element ...
            if node > 0:        # skip empty nodes
                points.append([d_nodes[node][0],d_nodes[node][1]])
        poly = Polygon([[p[0], p[1]] for p in points])
        polys.append(poly)

    poly_union = unary_union(polys)

    bounding_polygon = Polygon(poly_union.exterior.coords)

    if verbose:
        print(f'  Created bounding polygon for model')

    return bounding_polygon    

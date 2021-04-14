# snodes2shp.py
# Create stream node shapefiles for an IWFM model
# Copyright (C) 2020-2021 Hydrolytics LLC
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


def snodes2shp(nsnodes, stnodes_dict, node_coords, shape_name, epsg=26910, verbose=False):
    ''' snodes2shp() - Creates an IWFM stream nodes shapefile 

    Parameters
    ----------
    nsnodes : int
        number of stream nodes
    
    stnodes_dict : dictionary
        key = stream node, values = groundwater node, ...
    
    node_coords : list
        stream node coordinates
    
    shape_name : str
        output shapefile name
    
    epsg : int, default = 26910 (UTM 10N, CA)
        EPSG projection code
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import sys

    import fiona  # read and write shapefiles
    import fiona.crs  # fiona module defining crs
    from shapely.geometry import Point, mapping

    snode_shapename = f'{shape_name}_StreamNodes.shp'

    # Define the Point feature geometry
    snode_schema = {
        'geometry': 'Point',
        'properties': {
            'snode_id': 'int',
            'gw_node': 'int',
            'reach': 'int',
            'bottom': 'float:9.2',
        },
    }

    # Write a new stream node shapefile - EPSG 26910 = NAD 83 UTM 10
    with fiona.open(
        snode_shapename,
        'w',
        crs=fiona.crs.from_epsg(epsg),
        driver='ESRI Shapefile',
        schema=snode_schema,
    ) as out:
        for i in range(0, nsnodes):
            this_node = stnodes_dict.get(i + 1)  # gw_node, reach, bottom
            gw_node = this_node[0]
            if gw_node != 0:
                point = Point(
                    [(node_coords[gw_node - 1][0], node_coords[gw_node - 1][1])]
                )
                out.write(
                    {
                        'geometry': mapping(point),
                        'properties': {
                            'snode_id': i + 1,
                            'gw_node': this_node[0],
                            'reach': this_node[1],
                            'bottom': float(this_node[2]),
                        },
                    }
                )
    if verbose:
        print(f'  Wrote shapefile {snode_shapename}')
    return

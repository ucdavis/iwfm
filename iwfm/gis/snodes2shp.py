# snodes2shp.py
# Create stream node shapefiles for an IWFM model
# Copyright (C) 2020-2023 University of California
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


def snodes2shp(nsnodes, snodes_list, node_coords, shape_name, epsg=26910, verbose=False):
    ''' snodes2shp() - Creates an IWFM stream nodes shapefile 

    TODO:
      - change from fiona to pyshp and wkt format?

    Parameters
    ----------
    nsnodes : int
        number of stream nodes
    
    snodes_list : list of lists
        each contains [snode: int, gwnode: int, reach: int]
    
    node_coords : list
        stream node coordinates
    
    shape_name : str
        output shapefile name
    
    epsg : int, default=26910 (NAD 83 UTM 10, CA)
        EPSG projection code
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import fiona
    from shapely.geometry import Point, mapping

    shapename = f'{shape_name}_StreamNodes.shp'

    # Define the Point feature geometry
    schema = {
        'geometry': 'Point',
        'properties': {
            'snode_id': 'int',
            'gw_node': 'int',
            'reach': 'int',
        },
    }

    # Write a new stream node shapefile
    with fiona.open(
            shapename,
            'w',
            crs=f'epsg:{epsg}',      #depricated: crs=fiona.crs.from_epsg(epsg),
            driver='ESRI Shapefile',
            schema=schema,
        ) as out:
        for i in range(nsnodes):
            snode_id, gw_node, reach = snodes_list[i]
            if gw_node != 0:
                x, y = node_coords[gw_node - 1][1],node_coords[gw_node - 1][2]
                point = Point(x,y)
                properties = {
                    'snode_id': snode_id,
                    'gw_node': gw_node,
                    'reach': reach,
                    }
                feature = {'geometry': mapping(point), 'properties': properties}
                out.write(feature)
    if verbose:
        print(f'  Wrote shapefile {shapename}')
    return

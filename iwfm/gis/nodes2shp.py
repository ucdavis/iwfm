# nodes2shp.py
# Create node shapefiles for an IWFM model
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


def nodes2shp(node_coords, shape_name, epsg=26910, verbose=False):
    ''' nodes2shp() - Create an IWFM nodes shapefile 

    TODO:
      - change from fiona to pyshp and wkt format?

    Parameters
    ----------
    node_coords : list
        node coordinates
    
    shape_name : str
        output file name
    
    epsg : int, default=26910 (NAD 83 UTM 10, CA)
        EPSG projection
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import fiona
    from shapely.geometry import mapping, Point

    shapename = f'{shape_name}_Nodes.shp'

    # Define the point feature geometry
    schema = {
        'geometry': 'Point',
        'properties': {'node_id': 'int'},
    }

    # Write a new node shapefile
    with fiona.open(
            shapename,
            'w',
            crs=f'epsg:{epsg}',      #depricated: crs=fiona.crs.from_epsg(epsg),
            driver='ESRI Shapefile',
            schema=schema,
        ) as out:
        for i in range(len(node_coords)):
            x, y = node_coords[i][1],node_coords[i][2]
            point = Point(x,y)
            properties = {'node_id': node_coords[i][0]}
            feature = {'geometry': mapping(point), 'properties': properties}
            out.write(feature)

    if verbose:
        print(f'  Wrote shapefile {shapename}')

    return


def calc_base(node_strat):
    # calculate base altitude for each node
    nlayers = int(len(node_strat[0])/2 - 1)
    base = []
    for i in range(len(node_strat)):
        temp = node_strat[i][1]  # gse
        for j in range(nlayers * 2):
            temp = temp - node_strat[i][j + 2]
        base.append(temp)
    return base

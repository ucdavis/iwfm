# nodes2shp.py
# Create node shapefiles for an IWFM model
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


def nodes2shp(node_coords, node_list, node_strat, nlayers, shape_name, epsg=26910, verbose=False):
    ''' nodes2shp() - Create an IWFM nodes shapefile 

    Parameters
    ----------
    node_coords : list
        node coordinates
    
    node_list : list
        Node numbers

    node_strat : list
        stratigraphy for each node
    
    nlayers : int
        number of model layers
    
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
    import sys
    import pandas as pd
    import geopandas as gpd
    import os
    import shapefile

    node_shapename = f'{shape_name}_Nodes.shp'
    print(f"Current working dir : {os.getcwd()}")
    # calculate base altitude for each node
    base = []
    for i in range(0, len(node_strat)):
        temp = node_strat[i][1]  # gse
        for j in range(0, nlayers * 2):
            temp = temp - node_strat[i][j + 2]
        base.append(temp)

    # Create field names for layer properties
    field_names = ['node_id','gse','base']
    for i in range(0, nlayers):
        field_names.append('aqthick_' + str(i + 1))
        field_names.append('laythick_' + str(i + 1))

    nodes = shapefile.Writer(shapefile.POINT)
    [nodes.field(field) for field in field_names]
    for row in range(0,len(node_coords)):
        nodes.point((float(node_coords[row][0])),(float(node_coords[row][1])))
        temp_rec = []
        temp_rec.append(node_list[row])       # node_id
        temp_rec.append(node_strat[row][1])   # gse
        temp_rec.append(base[row])            # basement altitude
        for i in range(0, nlayers * 2):  
            temp_rec.append(node_strat[row][i+1])   # aquicluse and aquifer thicknesses
        nodes.record(*tuple([temp_rec]))

    nodes.save(node_shapename)
#    nodes.save(os.getcwd() + '\'' + node_shapename)

#    # Create a pandas dataframe
#    df = pd.DataFrame(
#        {
#            'node_id': [row[0] for row in node_strat],
#            'gse': [row[1] for row in node_strat],
#            'base': base,
#            'easting': [row[0] for row in node_coords],
#            'northing': [row[1] for row in node_coords],
#        }
#    )
#    # Add two fields for each layer (aquiclude thickness and aquifer thickness)
#    for i in range(0, nlayers * 2):  
#        df.insert(i + 2, field_names[i], [row[i + 2] for row in node_strat])
#    if verbose:
#        print(f'  Created pandas dataframe for {node_shapename}')
#
#    # Convert pandas dataframe to geopandas geodataframe
#    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.easting, df.northing))
#    gdf.crs = f'epsg:{str(epsg)}'
#
#    # Write a new node shapefile - EPSG 26910 = NAD 83 UTM 10
#    gdf.to_file(node_shapename)
#    if verbose:
#        print(f'  Wrote shapefile {node_shapename}')
 
    return

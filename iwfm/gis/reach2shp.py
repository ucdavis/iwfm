# reach2shp.py
# Create stream reach shapefile for an IWFM model
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


def reach2shp(reach_list, stnodes_dict, node_coords, shape_name, epsg=26910, 
        verbose=False):
    ''' reach2shp() - Creates an IWFM stream reaches shapefile from IWFM
        Preprocessor stream specification information

    Parameters
    ----------
    reach_list : list
        list of elements and associated nodes
    
    stnodes_dict : dictionary
        key = stream nodes, values = associated groundeater nodes
    
    node_coords : list
        list of nodes and associated X and Y coordinates
    
    shape_name : str
        base name for output shapefiles
    
    epsg : int, default=26910 (NAD 83 UTM 10, CA)
        EPSG projection
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import sys
    import fiona
    import fiona.crs
    from shapely.geometry import mapping, LineString

    reach_shapename = f'{shape_name}_StreamReaches.shp'

    stream_schema = {
        'geometry': 'LineString',
        'properties': {'reach_id': 'int', 'flows_to': 'int'},
    }

    with fiona.open(
            reach_shapename,
            'w',
            crs=fiona.crs.from_epsg(epsg),
            driver='ESRI Shapefile',
            schema=stream_schema,
        ) as out:
        for i in range(len(reach_list)):
            upper, lower = reach_list[i][1], reach_list[i][2]
            sncoords, n = [], 0
            for j in range(upper, lower + 1):
                this_node = stnodes_dict.get(j)
                gw_node = this_node[0]
                if gw_node != 0:
                    sncoords.append(
                        (node_coords[gw_node - 1][0], node_coords[gw_node - 1][1])
                    )
                    n += 1
            if sncoords:
                line = LineString(sncoords)
                out.write(
                    {
                        'geometry': mapping(line),
                        'properties': {'reach_id': i + 1, 'flows_to': reach_list[i][3]},
                    }
                )
    if verbose:
        print(f'  Wrote shapefile {reach_shapename}\n')
    return

# igsm_elem2shp.py
# Create an elements shapefile for an IGSM model
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


def igsm_elem2shp(elem_nodes,node_coords,elem_char,lake_elems,shape_name,
    epsg=26910,verbose=False):
    ''' igsm_elem2shp() - Create an elements shapefile for an IGSM model

    TODO:
      - change from fiona to pyshp and wkt format

    Parameters
    ----------
    elem_nodes : list
        list of elements and associated nodes
    
    node_coords : list
        list of nodes and associated X and Y coordinates
    
    elem_sub : list
        list of elements and associated subregions
    
    lake_elems : list
        list of lakes and associated elements
    
    shape_name : str
        output shapefiles base name
    
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
    from shapely.geometry import mapping, Polygon

    import iwfm as iwfm

    elem_shapename = f'{shape_name}_Elements.shp'

    polygons = iwfm.elem_poly_coords(elem_nodes, node_coords)

    # Define the polygon feature geometry
    elem_schema = {
        'geometry': 'Polygon',
        'properties': {
            'elem_id': 'int',
            'raingage': 'int',
            'rainfactor': 'float:6.3',
            'drainnode': 'int',
            'subregion': 'int',
            'soiltype': 'float:4.2',
            'lake_no': 'int',
        },
    }

    # Write a new element shapefile 
    with fiona.open(
        elem_shapename,
        'w',
        crs=fiona.crs.from_epsg(epsg),
        driver='ESRI Shapefile',
        schema=elem_schema,
    ) as out:
        for i in range(0, len(polygons)):
            poly = Polygon(polygons[i])
            lake_no = 0
            for j in range(0, len(lake_elems)):
                if lake_elems[j][1] == i + 1:  # lake on this element
                    lake_no = lake_elems[j][0]
            out.write(
                {
                    'geometry': mapping(poly),
                    'properties': {
                        'elem_id': i + 1,
                        'raingage': elem_char[i][0],
                        'rainfactor': elem_char[i][1],
                        'drainnode': elem_char[i][2],
                        'subregion': elem_char[i][3],
                        'soiltype': elem_char[i][4],
                        'lake_no': lake_no,
                    },
                }
            )
    if verbose:
        print(f'  Wrote shapefile {elem_shapename}')
    return 

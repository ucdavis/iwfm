# elem2shp.py
# Create elements shapefile for an IWFM model
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


def elem2shp(elem_ids,elem_nodes, node_coord_dict, elem_sub, lake_elems, shape_name,
    epsg=26910, verbose=False):
    ''' elem2shp() - Creates an IWFM element shapefile 

    TODO:
      - change from fiona to pyshp and wkt format?

    Parameters
    ----------
    elem_ids : list
        list of element id numbers
    
    elem_nodes : list
        list of elements and associated nodes

    node_coord_dict : dictionary
        key = node_id, values = associated X and Y coordinates
    
    elem_sub : list
        list of elements and associated subregions
    
    lake_elems : list
        list of lakes and associated elements
    
    shape_name : str
         output shapefiles base name
    
    epsg : int, default=26910 (NAD 83 UTM 10N, CA)
        EPSG projection
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import fiona
    import fiona.crs
    import shapefile as shp # pyshp
    from shapely.geometry import mapping, Polygon
    import iwfm as iwfm

    shapename = f'{shape_name}_Elements.shp'

    # Create list of element polygons
    polygons = iwfm.elem_poly_coords(elem_nodes, node_coord_dict)

    # Define the polygon feature geometry
    schema = {
        'geometry': 'Polygon',
        'properties': {'elem_id': 'int', 'subregion': 'int', 'lake_no': 'int'},
    }

    # Write a new element shapefile
    with fiona.open(
            shapename,
            'w',
            crs=f'epsg:{epsg}',      #depricated: crs=fiona.crs.from_epsg(epsg),
            driver='ESRI Shapefile',
            schema=schema,
        ) as out:
        for i in range(len(polygons)):
            poly = Polygon(polygons[i])
            lake_no = 0
            if lake_elems > 0:
                for j in range(len(lake_elems)):
                    if lake_elems[j][1] == i + 1:  # lake on this element
                        lake_no = lake_elems[j][0]
            out.write(
                {
                    'geometry': mapping(poly),
                    'properties': {
                        'elem_id': elem_ids[i],
                        'subregion': elem_sub[i],
                        'lake_no': lake_no,
                    },
                }
            )
    if verbose:
        print(f'  Wrote shapefile {shapename}')

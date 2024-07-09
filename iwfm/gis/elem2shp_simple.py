# elem2shp_simple.py
# Read csv files of elements and nodes and create a shapefile of the elements
# with no information other than the element id and the node ids
# Copyright (C) 2024 University of California
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

def elem2shp_simple(elem_nodes, node_coord_dict, shapename='elem', epsg=26910, verbose=True):

    # Create list of element polygons
    polygons = []
    for elem in elem_nodes:  # for each element ...
        coords = []
        for j in elem[1:]:  # for each node in the element ...
            coords.append((node_coord_dict[j][0],node_coord_dict[j][1]))
        coords.append(
            (node_coord_dict[elem[0]][0], node_coord_dict[elem[0]][1])
        )  # close the polygon with the first node
        polygons.append(coords)

    # Define the polygon feature geometry
    schema = {
        'geometry': 'Polygon',
        'properties': {'elem_id': 'int', 'node1': 'int', 'node2': 'int', 'node3': 'int', 'node4': 'int'},
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
            out.write(
                {
                    'geometry': mapping(poly),
                    'properties': {
                        'elem_id': elem_nodes[i][0],
                        'node1':   elem_nodes[i][1],
                        'node2':   elem_nodes[i][2],
                        'node3':   elem_nodes[i][3],
                        'node4':   elem_nodes[i][4],
                    },
                }
            )
    if verbose: print(f'  Wrote shapefile {shapename}')


if __name__ == "__main__":
    ''' Run elem2shp_simple from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm.gis as igis
    import iwfm as iwfm
    import fiona
    from shapely.geometry import mapping, Polygon

    args = sys.argv
    verbose=True
    epsg=26910

    if len(sys.argv) > 1:  # arguments are listed on the command line
        elem_file_name  = args[1]
        node_file_name  = args[2]
    else:  # ask for file names from terminal
        elem_file_name  = input('Elements csv file name: ')
        node_file_name  = input('Nodes csv file name: ')

    iwfm.file_test(elem_file_name)
    iwfm.file_test(node_file_name)

    idb.exe_time()                                              # initialize timer

    # Read coarse elements and nodes
    node_ids, node_coord_dict = iwfm.read_nodes_csv(node_file_name)          
    if verbose: print(f'  Read {len(node_ids):,} nodes from {node_file_name}')

    elem_ids, elem_nodes = iwfm.read_elements_csv(elem_file_name)       
    if verbose: print(f'  Read {len(elem_ids):,} elements from {elem_file_name}')

    shapename = elem_file_name.replace('.csv', '_nodes.shp')

    # Wtrite elements to shapefile
    elem2shp_simple(elem_nodes, node_coord_dict, shapename=shapename, epsg=epsg, verbose=verbose)



    idb.exe_time()                                          # print elapsed time

# elems2shp_csv.py
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

def elems2shp_csv(elem_nodes, node_coord_dict, shapename='elems.shp', epsg=26910, verbose=True):
    ''' Create a shapefile of the elements with the element ids and node ids 
    
    Parameters
    ----------
    elem_nodes : list
        List of elements and their nodes
        
    node_coord_dict : dict
        Dictionary of node coordinates
        
    shapename : str, default 'elems.shp'
        Name of the shapefile to be created
        
    epsg : int, default 26910
        EPSG code for the shapefile
            
    verbose : bool, default True
        Print information to the console
                
    Returns
    -------
        nothing
    '''

    import shapefile
    import pyproj
    from shapely.geometry import Polygon  # mapping no longer needed

    # Create list of element polygons
    polygons = []
    for elem in elem_nodes:  # for each element ...
        if elem[-1]==0:  # remove the last item in list if zero
            elem = elem[:-1]

        coords = []
        for j in elem[1:]:  # for each node in the element ...
            coords.append((node_coord_dict[j][0],node_coord_dict[j][1]))
        coords.append(
            (node_coord_dict[elem[1]][0], node_coord_dict[elem[1]][1])
        )  # close the polygon with the first node
        polygons.append(coords)

    # Create a new shapefile writer object
    shapename = shapename.replace('.shp', '')  # remove extension if present
    w = shapefile.Writer(shapename, shapeType=shapefile.POLYGON)
    
    # Define fields
    w.field('elem_id', 'N', 10, 0)
    w.field('node1', 'N', 10, 0)
    w.field('node2', 'N', 10, 0)
    w.field('node3', 'N', 10, 0)
    w.field('node4', 'N', 10, 0)

    # Write features
    for i in range(len(polygons)):
        w.poly([polygons[i]])  # Add geometry
        w.record(              # Add attributes
            elem_nodes[i][0],  # elem_id
            elem_nodes[i][1],  # node1
            elem_nodes[i][2],  # node2
            elem_nodes[i][3],  # node3
            elem_nodes[i][4]   # node4
        )
    
    # Write projection file
    prj = open(f"{shapename}.prj", "w")
    epsg = f'EPSG:{epsg}'
    prj.write(pyproj.CRS(epsg).to_wkt())
    prj.close()
    
    w.close()
    if verbose: print(f'  Wrote shapefile {shapename}.shp')


if __name__ == "__main__":
    ''' Run elems2shp_csv from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

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

    shapename = elem_file_name.replace('.csv', '.shp')

    # Wtrite elements to shapefile
    elems2shp_csv(elem_nodes, node_coord_dict, shapename=shapename, epsg=epsg, verbose=verbose)



    idb.exe_time()                                          # print elapsed time

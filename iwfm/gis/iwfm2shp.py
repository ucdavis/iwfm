# iwfm2shp.py
# Create shapefiles for an IWFM model
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


def iwfm2shp(main_file, shape_name, epsg=26910, verbose=False):
    ''' iwfm2shp() - Takes the IWFM model main preprocessor file name
        and a base name for output files, and create node, element, 
        stream node and stream reach shapefiles

    Parameters
    ----------
    main_file : str
        IWFM Preprocessor main file name
    
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

    import os
    import iwfm as iwfm
    import iwfm.gis as gis

    topdir = os.getcwd()

    pre_dict, have_lake = iwfm.iwfm_read_preproc(main_file)
    if verbose:
        print(f'  Read preprocessor file {main_file}')

    elem_ids, elem_nodes, elem_sub = iwfm.iwfm_read_elements(pre_dict['elem_file']) 
    if verbose:
        print(f'  Read nodes of {len(elem_nodes):,} elements from {pre_dict["elem_file"]}')

    node_coords, node_list, factor = iwfm.iwfm_read_nodes(pre_dict['node_file'], factor = 1)
    if verbose:
        print(f'  Read coordinates of {len(node_coords):,} nodes from {pre_dict["node_file"]}')

    node_coord_dict = iwfm.list2dict(node_coords)    # Put node_coords into a dictionary

    node_strat, nlayers = iwfm.iwfm_read_strat(pre_dict['strat_file'], node_coords)
    if verbose:
        print(f'  Read stratigraphy for {len(node_strat):,} nodes from {pre_dict["strat_file"]}')

    if have_lake:
        lake_elems, lakes = iwfm.iwfm_read_lake(pre_dict['lake_file'])  
        if verbose:
            if len(lakes) > 1:
                print(f'  Read info for {len(lakes):,} lakes from {pre_dict["lake_file"]}')
            elif len(lakes) == 1:
                print(f'  Read info for {len(lakes):,} lake from {pre_dict["lake_file"]}')
    else:
        lake_elems, lakes = 0, [0]
        if verbose:
            print('  No lakes file')

    reach_list, snodes_list, stnodes_dict, nsnodes, rating_dict = iwfm.iwfm_read_streams(pre_dict['stream_file'])
    if verbose:
        print(f'  Read info for {len(reach_list):,} stream reaches and {nsnodes:,} stream nodes from {pre_dict["stream_file"]}')

    if verbose:
        print(' ')

    # == Create element shapefile
    gis.elem2shp(elem_ids,elem_nodes,node_coord_dict,elem_sub,lake_elems,shape_name,epsg=epsg,verbose=verbose)

    # == Create node shapefile
    gis.nodes2shp(node_coords, shape_name,epsg=epsg,verbose=verbose)

    # == Create stream node shapefile
    gis.snodes2shp(nsnodes, snodes_list, node_coords, shape_name,epsg=epsg,verbose=verbose)

    # == Create stream reach shapefile
    gis.reach2shp(reach_list, snodes_list, node_coords, shape_name,epsg=epsg,verbose=verbose)

    return 


if __name__ == '__main__':
    ' Run iwfm2shp() from command line '
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    epsg=26910	# default UTM 10N (CA)

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
        output_basename = sys.argv[2]
        if len(sys.argv) > 3:
       		epsg=int(sys.argv[3]) 
    else:  # ask for file names from terminal
        input_file = input('IWFM Preprocessor main file name: ')
        output_basename = input('Output shapefile basename: ')
        projection = input('Projection EPSG integer value (blank for default UTM 10N): ')
        if len(projection) >1:
        	epsg=int(projection) 

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    iwfm2shp(input_file, output_basename, epsg, verbose=True)

    idb.exe_time()  # print elapsed time

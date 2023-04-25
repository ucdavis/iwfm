# iwfm_sub_preproc.py 
# Read in a list of element pairs for a submodel. Use existing model Elements, 
# Nodes, Stream specification and stratigraphy files to produce new 
# preprocessor files for the submodel and a list of model node pairs
# Copyright (C) 2018-2021 University of California
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


def iwfm_sub_preproc(
    in_pp_file, elem_pairs_file, out_base_name, verbose=False):
    ''' iwfm_sub_preproc() - Read in the Preprocessor main file of a model and a list
    of element pairs for a submodel. Use existing model Elements, Nodes, Stream
    specification, Lake and Stratigraphy files to produce new preprocessor files for
    the submodel, and pickle files of submodel nodes, stream nodes and lakes

    Parameters
    ----------
    in_pp_file : str
        name of existing preprocessor main input file

    elem_pairs_file : str
        name of file listing elements of existing nmodel and submodel

    out_base_name : str
        root of submodel output file names

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    pre_dict_new : dict
        dictionary of submodel preprocessor file names

    sub_elem_list : ints
        list of existing model elements in submodel

    new_srs : ints
        list of existing model subregions in submodel

    elem_dict : dict
        dictionary existing model element to submodel element

    sub_node_list : ints
        list of existing model nodes in submodel

    snode_dict : ints
        list of existing model stream nodes in submodel

    lake_info : list
        description of each lake in the submodel

    '''
    import iwfm as iwfm
    import pickle
    import pandas as pd
    import geopandas as gpd

    # -- get list of file names from preprocessor input file
    pre_dict, have_lake = iwfm.iwfm_read_preproc(in_pp_file)
    if verbose:
        print(f'  Read preprocessor file {in_pp_file}')

    # -- create list of new file names
    pre_dict_new = iwfm.new_pp_dict(out_base_name)

    # -- read submodel elements
    sub_elem_list, new_srs, elem_dict, rev_elem_dict = iwfm.get_elem_list(elem_pairs_file)
    pickle.dump(sub_elem_list, open(out_base_name + '_elems.bin', 'wb'))  # dump sub_elem_list to file
    if verbose:
        print(f'  Read submodel element pairs file {elem_pairs_file}')

    # -- determine submodel nodes
    sub_node_list = iwfm.sub_pp_nodes(pre_dict['elem_file'], sub_elem_list)
    pickle.dump(sub_node_list, open(out_base_name + '_nodes.bin', 'wb'))  # dump sub_node_list to file
    if verbose:
        print('  Compiled list of submodel nodes')

    # -- get submodel node coordinates
    node_coord, node_list = iwfm.iwfm_read_nodes(pre_dict['node_file'])

    i = 0
    while i < len(node_coord):
        if node_coord[i][0] not in sub_node_list:
            del(node_coord[i])
        else:
            i += 1
 
    pickle.dump(node_coord, open(out_base_name + '_node_coords.bin', 'wb'))  # dump node_coords to file
    if verbose:
        print('  Compiled list of submodel nodal coordinates')

    # -- determine submodel stream nodes
    reach_info, snode_dict, rattab_dict, rating_header, stream_aq, sub_snodes = iwfm.sub_pp_streams(
        pre_dict['stream_file'], sub_node_list
    )

    # dump sub_nodes to file
    pickle.dump(sub_snodes, open(out_base_name + '_sub_snodes.bin', 'wb'))  

    # dump snode_dict to file
    pickle.dump(snode_dict, open(out_base_name + '_snodes.bin', 'wb'))  

    if verbose:
        print('  Compiled list of submodel stream nodes')

    # -- determine submodel lakes
    if have_lake:
        lake_info, have_lake = iwfm.sub_pp_lakes(pre_dict['lake_file'], sub_elem_list)
        # dump lake_info to file
        pickle.dump(lake_info, open(out_base_name + '_lakes.bin', 'wb'))  
        if have_lake and verbose:
            print('  Compiled list of submodel lakes')

    # create pandas dataframe for submodel
    df = pd.DataFrame(
        {
            'node_id':  [row[0] for row in node_coord],
            'easting':  [row[1] for row in node_coord],
            'northing': [row[2] for row in node_coord],
        }
    )
    df.to_pickle(out_base_name + '_df.bin')

    if verbose:
        print(' ')

    # -- write new node file
    iwfm.sub_pp_node_file(pre_dict['node_file'], pre_dict_new['node_file'], sub_node_list)
    if verbose:
        print(f'  Wrote submodel node file {pre_dict_new["node_file"]}')

    # -- write new element file
    elem_nodes = iwfm.sub_pp_elem_file(
        pre_dict['elem_file'], pre_dict_new['elem_file'], sub_elem_list, new_srs
    )
    pickle.dump(elem_nodes, open(out_base_name + '_elemnodes.bin', 'wb'))  
    if verbose:
        print(f'  Wrote submodel element file {pre_dict_new["elem_file"]}')

    # -- write new stratigraphy file
    iwfm.sub_pp_strat_file(
        pre_dict['strat_file'], pre_dict_new['strat_file'], sub_node_list
    )
    if verbose:
        print(f'  Wrote submodel stratigraphy file {pre_dict_new["strat_file"]}')

    # -- write new stream specification file
    iwfm.sub_pp_stream_file(
        pre_dict['stream_file'],
        pre_dict_new['stream_file'],
        snode_dict,
        reach_info,
        rattab_dict,
        rating_header,
        stream_aq,
    )
    if verbose:
        print(f'  Wrote submodel stream specification file {pre_dict_new["stream_file"]}')

    # -- write new lake file
    if have_lake:
        iwfm.sub_pp_lake_file(
            pre_dict['lake_file'], pre_dict_new['lake_file'], lake_info
        )
        if verbose:
            print(
                f'  Wrote submodel lake specification file {pre_dict_new["lake_file"]}'
            )

    # -- write new preprocesor main input file
    iwfm.sub_pp_file(in_pp_file, pre_dict, pre_dict_new, have_lake)
    if verbose:
        print(f'  Wrote submodel preprocessor file {pre_dict_new["prename"]}')

    if have_lake == False:
        lake_info=[]
    return pre_dict_new, sub_elem_list, new_srs, elem_dict, sub_node_list, snode_dict, lake_info
    

if __name__ == "__main__":
    ''' Run iwfm_sub_preproc() from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    verbose = True

    if len(sys.argv) > 1:  # arguments are listed on the command line
        in_pp_file = sys.argv[1]       # in: old model preprocessor.in file
        elem_pairs_file = sys.argv[2]  # in: file with element pairs
        out_base_name = sys.argv[3]    # output file base name
    else:  # ask for file names from terminal
        in_pp_file      = input('Existing IWFM Preprocessor.in file: ')
        elem_pairs_file = input('Element pairs file: ')
        out_base_name   = input('Output file base name: ')

    # == test that the input files exist
    iwfm.file_test(in_pp_file)
    iwfm.file_test(elem_pairs_file)

    idb.exe_time()  # initialize timer
    iwfm_sub_preproc(in_pp_file, elem_pairs_file, out_base_name, verbose=verbose)

    if verbose:
        print(' ')
        print(f'  Created submodel {out_base_name} preprocessor files from {in_pp_file}')
    idb.exe_time()  # print elapsed time



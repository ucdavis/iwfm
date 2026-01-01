# iwfm_sub_sim.py  - Read in a list of element pairs for a submodel.
# Use existing model Elements, Nodes, Stream specification and stratigraphy files
# to produce new preprocessor files for the submodel and a list of model node pairs
# Copyright (C) 2018-2026 University of California
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


def iwfm_sub_sim(in_sim_file, elem_pairs_file, out_base_name, verbose=False, debug=False):
    '''iwfm_sub_sim.py - Read in a list of element pairs for a submodel.
    Use existing model Elements, Nodes, Stream specification and stratigraphy
    files to produce new preprocessor files for the submodel and a list of
    model node pairs

    *** INCOMPLETE - UNDER DEVELOPMENT ***

    Parameters
    ----------
    in_sim_file : str
        name of existing simulation main input file

    elem_pairs_file : str
        name of file listing elements of existing nmodel and submodel

    out_base_name : str
        root of submodel output file names

    verbose : bool, default=False
        turn command-line output on or off

    debug : bool, default=False
        turn debugging output on or off

    Returns:
      # -- to be determined --

    TODO:
      - test for nodes pickle file, read info from source if not present, error if no source
      - test for node_coords pickle file, read info from source if not present, error if no source
      - test for elem_list pickle file, read info from source if not present, error if no source
      - test for lake_info pickle file, read info from source if not present, error if no source
      - test for geopandas dataframe pickle file, create from node_coords if not present, error if no source
      - process Lake files

    '''
    import iwfm as iwfm
    import iwfm.gis as gis
    import pickle

    # -- get list of file names from preprocessor input file
    sim_dict, have_lake = iwfm.iwfm_read_sim_file(in_sim_file)
    if verbose:
        print(f'  Read simulation file {in_sim_file}')

    # -- create list of new file names
    sim_dict_new = iwfm.new_sim_dict(out_base_name)

    # ** TODO: test for pickle files, read info from source if not present, error if no source
    # read information from previous dump
    with open(out_base_name + '_elems.bin', 'rb') as f:
        elem_list = pickle.load(f)
    with open(out_base_name + '_nodes.bin', 'rb') as f:
        node_list = pickle.load(f)
    with open(out_base_name + '_elemnodes.bin', 'rb') as f:
        elem_nodes = pickle.load(f)
    with open(out_base_name + '_node_coords.bin', 'rb') as f:
        node_coords = pickle.load(f)
    with open(out_base_name + '_snodes.bin', 'rb') as f:
        snode_dict = pickle.load(f)
    with open(out_base_name + '_sub_snodes.bin', 'rb') as f:
        sub_snodes = pickle.load(f)
    if verbose:
        print('  Read model elements, nodes, node coordinates and stream nodes')

    if have_lake:
        with open(out_base_name + '_lakes.bin', 'rb') as f:
            lake_info = pickle.load(f)
        if verbose:
            print('  Read model lakes')

    # -- create bounding polygon
    bounding_poly = gis.elem2boundingpoly(elem_nodes, node_coords)

    # -- create submodel Small Watersheds file
    iwfm.sub_swhed_file(sim_dict['swshed_file'], sim_dict_new['swshed_file'], node_list, snode_dict, verbose)

    # -- create submodel Unsaturated Zone file
    iwfm.sub_unsat_file(sim_dict['unsat_file'], sim_dict_new['unsat_file'], elem_list, verbose)

    # -- process submodel Groundwater files 
    iwfm.sub_gw_file(sim_dict, sim_dict_new, node_list, elem_list, bounding_poly, verbose=verbose)

    # -- process submodel Streams file
    iwfm.sub_streams_file(sim_dict, sim_dict_new, elem_list, sub_snodes, verbose)

    # -- process submodel Rootzone file
    iwfm.sub_rootzone_file(sim_dict, sim_dict_new, elem_list, sub_snodes, verbose)

    # -- process submodel Lake file
    if have_lake:
        if verbose:                
            print('\n   ==> TO DO: Lake process files')

    if verbose:
        print(" ")




    # -- write new simulation main input file
    iwfm.sub_sim_file(in_sim_file, sim_dict_new, have_lake)
    if verbose:
        print(f'  Wrote submodel simulation file {sim_dict_new["sim_name"]}')

    return  # ================================================================
    return


if __name__ == "__main__":
    ''' Run iwfm_sub_sim() from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    verbose = True

    if len(sys.argv) > 1:              # arguments are listed on the command line
        in_sim_file = sys.argv[1]      # old model simulaiton.in file
        elem_pairs_file = sys.argv[2]  # file with element pairs
        out_base_name = sys.argv[3]    # output file base name
    else:  # ask for file names from terminal
        in_sim_file     = input('Existing IWFM Simulation.in file: ')
        elem_pairs_file = input('Element pairs file: ')
        out_base_name   = input('Output file base name: ')

    # == test that the input files exist
    iwfm.file_test(in_sim_file)
    iwfm.file_test(elem_pairs_file)

    idb.exe_time()  # initialize timer
    iwfm_sub_sim(in_sim_file, elem_pairs_file, out_base_name, verbose=verbose)

    if verbose:
        print(' ')
        print(
            f'  Created submodel {out_base_name} simulation files from {in_sim_file}.'
        )  # update cli
    idb.exe_time()  # print elapsed time

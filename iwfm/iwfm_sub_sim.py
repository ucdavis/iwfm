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


from iwfm.debug.logger_setup import logger


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
    import iwfm
    import iwfm.gis as gis
    import pickle
    from pathlib import Path

    # -- get list of file names from preprocessor input file
    sim_dict, have_lake = iwfm.iwfm_read_sim_file(in_sim_file)
    if verbose:
        print(f'  Read simulation file {in_sim_file}')

    # -- resolve relative paths in sim_dict to absolute paths
    sim_base_path = Path(in_sim_file).resolve().parent
    for key in sim_dict:
        if isinstance(sim_dict[key], str) and key.endswith('_file'):
            # Convert Windows backslashes and resolve relative to simulation file directory
            sim_dict[key] = str(sim_base_path / sim_dict[key].replace('\\', '/'))

    # -- verify that required input files exist
    import os
    import sys
    missing_files = []
    required_files = ['gw_file', 'swshed_file', 'unsat_file']

    for key in required_files:
        if key not in sim_dict:
            missing_files.append(f'  - {key}: Not specified in simulation input file')
        elif not os.path.exists(sim_dict[key]):
            missing_files.append(f'  - {key}: {sim_dict[key]}')

    if missing_files:
        print('\n*** ERROR: Required input file(s) not found:')
        for msg in missing_files:
            print(msg)
        print('\nPlease check:')
        print('  1. The simulation input file contains correct file paths')
        print('  2. All referenced files exist at the specified locations')
        print('  3. File paths are correct relative to the simulation input file location')
        print(f'\nSimulation file location: {sim_base_path}')
        sys.exit(1)

    # -- create list of new file names
    sim_dict_new = iwfm.new_sim_dict(out_base_name)

    # ** TODO: test for pickle files, read info from source if not present, error if no source
    # Check that required pickle files exist
    pickle_files = [
        (out_base_name + '_elems.bin', 'elements'),
        (out_base_name + '_nodes.bin', 'nodes'),
        (out_base_name + '_elemnodes.bin', 'element nodes'),
        (out_base_name + '_node_coords.bin', 'node coordinates'),
        (out_base_name + '_snodes.bin', 'stream nodes'),
        (out_base_name + '_sub_snodes.bin', 'submodel stream nodes')
    ]

    missing_pickle_files = []
    for filepath, description in pickle_files:
        if not os.path.exists(filepath):
            missing_pickle_files.append(f'  - {description}: {filepath}')

    if have_lake:
        lake_file = out_base_name + '_lakes.bin'
        if not os.path.exists(lake_file):
            missing_pickle_files.append(f'  - lake information: {lake_file}')

    if missing_pickle_files:
        print('\n*** ERROR: Required preprocessed data file(s) not found:')
        for msg in missing_pickle_files:
            print(msg)
        print('\nThese binary files contain preprocessed model data and must be')
        print('generated before running this script. Please run the preprocessing')
        print('step that creates these files first.')
        print(f'\nExpected base name: {out_base_name}')
        sys.exit(1)

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
    iwfm.sub_gw_file(sim_dict, sim_dict_new, node_list, elem_list, bounding_poly, sim_base_path, verbose=verbose)

    # -- process submodel Streams file
    iwfm.sub_streams_file(sim_dict, sim_dict_new, elem_list, sub_snodes, sim_base_path, verbose)

    # -- process submodel Rootzone file
    iwfm.sub_rootzone_file(sim_dict, sim_dict_new, elem_list, sub_snodes, sim_base_path, verbose)

    # -- process submodel Lake file
    if have_lake:
        logger.debug('TO DO: Lake process files')

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
    import iwfm
    from iwfm.debug import parse_cli_flags

    verbose, debug = parse_cli_flags()


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

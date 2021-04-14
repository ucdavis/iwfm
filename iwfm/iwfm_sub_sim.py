# iwfm_sub_sim.py  - Read in a list of element pairs for a submodel.
# Use existing model Elements, Nodes, Stream specification and stratigraphy files
# to produce new preprocessor files for the submodel and a list of model node pairs
# Copyright (C) 2018-2021 Hydrolytics LLC
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
      - test for node_list pickle file, read info from source if not present, error if no source
      - test for elem_list pickle file, read info from source if not present, error if no source
      - test for lake_info pickle file, read info from source if not present, error if no source
      - process Groundwater file
      - process Streams file
      - process Rootzone file
      - process Lake file

    '''
    import iwfm as iwfm
    import pickle

    # -- get list of file names from preprocessor input file
    sim_dict, have_lake = iwfm.iwfm_read_sim_file(in_sim_file)
    if verbose:
        print(f'  Read simulation file {in_sim_file}')

    # -- create list of new file names
    sim_dict_new = iwfm.new_sim_dict(out_base_name)

    # -- read submodel elements
    elem_list, new_srs, elem_dict, rev_elem_dict = iwfm.get_elem_list(elem_pairs_file)
    elems = [e for e[0] in elem_list]
    if verbose:
        print(f'  Read submodel element pairs file {elem_pairs_file}')

    # ** TODO: test for pickle files, read info from source if not present, error if no source
    # read information from previous dump
    node_list = pickle.load(open(out_base_name + '_nodes.bin', 'rb'))  
    snode_dict = pickle.load(open(out_base_name + '_snodes.bin', 'rb'))
    if verbose:
        print('  Read submodel nodes and stream nodes')

    if have_lake:
        lake_info = pickle.load(open(out_base_name + '_lakes.bin', 'rb'))  
        if verbose:
            print('  Read submodel lakes')

    if verbose:
        print(" ")

    # -- create submodel Small Watersheds file
    iwfm.sub_swhed_file(
        sim_dict['swshed_file'], sim_dict_new['swshed_file'], node_list, snode_dict
    )
    if verbose:
        print(f'  Wrote small watershed file {sim_dict_new["swshed_file"]}')

    # -- create submodel Unsaturated Zone file
    iwfm.sub_unsat_file(sim_dict["unsat_file"], sim_dict_new["unsat_file"], elem_list)
    if verbose:
        print(f'  Wrote unsaturated zone file {sim_dict_new["unsat_file"]}')

    return  # ================================================================

    # -- process Groundwater file

    # -- process Streams file

    # -- process Rootzone file

    # -- process Lake file
    # if have_lake:

    if verbose:
        print(" ")


    # -- write new simulation main input file
    iwfm.sub_pp_file(in_sim_file, sim_dict, sim_dict_new, have_lake)
    if verbose:
        print(f'  Wrote submodel simulation file {sim_dict_new["prename"]}')

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

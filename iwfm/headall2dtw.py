# headall2dtw.py
# Read headall.out file and stratigraphy file and write depth to water with
# one csv file for each model layer
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


def headall2dtw(heads_file, pre_file, output_root, verbose=False):
    ''' headall2dtw() - Reads IWFM HeadAll.out file, subtracts heads from
        land surface elevation, and writes out as a time series with
        one csv file for each layer

    Parameters
    ----------
    heads_file : str
        name of headall.out file 
    
    pre_file : str
        name of IWFM Preprocessor main input file
    
    output_root : str
        basename of output file
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing
    
    '''
    import numpy as np
    import os
    import iwfm as iwfm

    pre_path, pre_proc = os.path.split(pre_file)
    pre_dict, _ = iwfm.iwfm_read_preproc(pre_file)

    node_file = os.path.join(pre_path, pre_dict['node_file'])
    node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

    strat_file = os.path.join(pre_path, pre_dict['strat_file'])
    strat, nlayers = iwfm.iwfm_read_strat(strat_file, node_coords)

    elevations = iwfm.iwfm_lse(strat)
    lse = np.asarray([i[1] for i in elevations])

    # -- get heads
    data, layers, dates, nodes = iwfm.headall_read(heads_file)
    heads = np.asarray(data)

    # -- calculate depth from land surface
    dtw = lse - heads

    # -- write to csv files
    iwfm.headall2csv(
        np.around(dtw, 3),
        layers,
        dates,
        nodes,
        output_root,
        verbose=verbose,
    )
    return


if __name__ == '__main__':
    ' Run headall2dtw() from command line '
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        heads_file = sys.argv[1]
        pre_file = sys.argv[2]
        output_root = sys.argv[3]
    else:  # ask for file names from terminal
        heads_file  = input('IWFM Headall file name: ')
        pre_file    = input('IWFM Preprocessor main file name: ')
        output_root = input('Output file rootname: ')

    iwfm.file_test(heads_file)
    iwfm.file_test(pre_file)

    output_file = heads_file.split('.')[0]

    idb.exe_time()  # initialize timer

    headall2dtw(heads_file, pre_file, output_root, verbose=True)

    idb.exe_time()  # print elapsed time

# headall2csv.py
# Read headall.out file and write out a csv file for each layer
# Copyright (C) 2020-2021 University of California
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


def headall2csv(data, layers, dates, nodes, output_file, verbose=False):
    ''' headall2csv() - Write out IWFM Headall.out data as one csv file
        for each layer

    Parameters
    ----------
    data : list
        numpy array of floats, size nodes x layers
    
    layers : int
        number of layers
    
    dates : list
        list of dates
    
    nodes : int
        number of nodes
    
    output_file : str
        output csv file base name
    
    verbose : bool, default=False
        True = command-line output on
    
    Return
    ------
    nothing
    
    '''
    import pandas as pd

    for i in range(0, layers):
        out_list = []
        for time_index in range(len(data)):
            out_list.append(data[time_index][i])
        out_df = pd.DataFrame(out_list, columns=nodes, index=dates).T
        of = output_file + '_' + str(i + 1) + '.csv'
        out_df.to_csv(of)
        if verbose:
            print(f'  Wrote layer {i + 1} to {of}')
    return

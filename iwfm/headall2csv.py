# headall2csv.py
# Read headall.out file and write out a csv file for each layer
# Copyright (C) 2020-2021 Hydrolytics LLC
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
    """ headall2csv() - Takes data from a IWFM HeadAll.out file and
        writes out one csv file for each layer

    Parameters:
      data            (list): numpy array of floats, size nodes x layers
      layers          (int):  Number of layers
      dates           (list): List of dates
      nodes           (int):  Number of nodes
      output_file     (str):  Root name of output csv file
      verbose         (bool): Turn command-line output on or off
    
    Return:
      nothing
    """
    import pandas as pd

    for i in range(0, layers):  # write out to csv
        out_list = []
        index = i
        while index < len(data):
            out_list.append(data[index])
            index += layers
        out_df = pd.DataFrame(out_list, columns=nodes, index=dates).T
        of = output_file + '_' + str(i + 1) + '.csv'
        out_df.to_csv(of)
        if verbose:
            print(f'  Wrote layer {i + 1} to {of}')
    return

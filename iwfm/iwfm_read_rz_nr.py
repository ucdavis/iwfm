# iwfm_read_rz_nr.py
# Read native and riparian data from a file and organize them into lists
# Copyright (C) 2020-2024 University of California
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


def iwfm_read_rz_nr(file, verbose=False):
    """iwfm_read_rz_nr() - Read native and riparian data from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the ponded crop data.
  
    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------

    crops : list
        A list of crop codes
    
    params : list
        A list of parameters: [cnnv, cnrv, icetnv, icetrv, istrmrv, ic]

    files : list
        A list of file names: [nr_area_file]

    """
    import iwfm as iwfm
    import numpy as np

    ncrops = 2                                                  # number of ponded crop types (may be variable in future IWFM versions)

    if verbose: print(f"Entered iwfm_read_rz_nr() with {file}")

    nr_lines = open(file).read().splitlines()                   # open and read input file

    line_index = iwfm.skip_ahead(0, nr_lines, 0)                # skip to number of crop types
    nr_area_file = nr_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, nr_lines, 0)           # skip budget file names
    fact = float(nr_lines[line_index].split()[0])                       # root zone depth conversion factor

    line_index = iwfm.skip_ahead(line_index + 1, nr_lines, 0)           # skip budget file names
    rd_nat = float(nr_lines[line_index].split()[0]) * fact              # root zone depth conversion factor

    line_index = iwfm.skip_ahead(line_index + 1, nr_lines, 0)           # skip budget file names
    rd_rip = float(nr_lines[line_index].split()[0]) * fact              # root zone depth conversion factor

    # how many elements?
    line_index = iwfm.skip_ahead(line_index + 1, nr_lines, 0)           # skip to next value line
    ne = 0
    while nr_lines[line_index+(ne)].split()[0] != 'C':
        ne += 1
    ne -= 1                                                             # one to convert to zero index

    # read native and riparian parameter table
    params, line_index = iwfm.iwfm_read_param_table_ints(nr_lines, line_index, ne)

    params = np.array(params)

    line_index = iwfm.skip_ahead(line_index + 1, nr_lines, 0)           # skip to next value line


    # initial condition
    ic, line_index = iwfm.iwfm_read_param_table_floats(nr_lines, line_index, ne)

    ic = np.array(ic)

    crops = ['nat_rip', 'ic']

    files = [nr_area_file]

    params = [params, ic]
        
    if verbose: print(f"Leaving iwfm_read_rz_nr()")

    return crops, params, files

# iwfm_read_rz_urban.py
# Read urban parameter data from a file and organize them into lists
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

def iwfm_read_rz_urban(file):
    """iwfm_read_rz_urban() - Read urban land use data from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the urban land use data.
  
    Returns
    -------

    crops : list
        A list of crop codes
    
    params : list
        A list of parameters: [perv, cnurb, icpopul, icwtruse, fracdm, iceturb, icrtfurb, icrufurb, icurbspec, ic]

    files : list
        A list of file names: [ur_area_file, ur_pop_file, ur_wtr_file, ur_spec_file]

    """
    import iwfm as iwfm
    import numpy as np

    ur_lines = open(file).read().splitlines()                   # open and read input file

    line_index = iwfm.skip_ahead(0, ur_lines, 0)                # skip to number of crop types
    ur_area_file = ur_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)   # skip to next value line
    factf = float(ur_lines[line_index].split()[0])              # root zone depth conversion factor

    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)   # skip to next value line
    rooturb = float(ur_lines[line_index].split()[0])*factf      # urban root zone depth

    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)   # skip to next value line
    ur_pop_file = ur_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)   # skip to next value line
    ur_wtr_file = ur_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)   # skip to next value line
    ur_spec_file = ur_lines[line_index].split()[0]

    # how many elements?
    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)           # skip to next value line
    ne = 0
    while ur_lines[line_index+(ne)].split()[0] != 'C':
        ne += 1
    ne -= 1                                                             # one to convert to zero index

    # parameters = ['perv','cnurb','icpopul', 'icwtruse', 'fracdm', 'iceturb', ,icrtfurb', 'icrufurb', 'icurbspec.']
    params, line_index = iwfm.iwfm_read_param_table_floats(ur_lines, line_index, ne)

    params = np.array(params)

    line_index = iwfm.skip_ahead(line_index + 1, ur_lines, 0)           # skip to next value line

    # initial condition
    ic, line_index = iwfm.iwfm_read_param_table_floats(ur_lines, line_index, ne)

    ic = np.array(ic)

    crops = ['urban','ic']

    files = [ur_area_file, ur_pop_file, ur_wtr_file, ur_spec_file]

    params = [params, ic]
        
    return crops, params, files

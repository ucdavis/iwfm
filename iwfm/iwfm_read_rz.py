# iwfm_read_rz.py 
# Read root zone parameters from a file and organize them into lists
# Copyright (C) 2023-2026 University of California
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

def iwfm_read_rz(rz_file):
    """iwfm_read_rz() - Read an IWFM Rootzone main input file and return a list of the 
                        files called

    Parameters
    ----------
    rz_file : str
        name of existing nmodel rootzone file

    Returns
    -------
    rz_dict : dicttionary
        dictionary of existing model file names
    
    """

    import iwfm as iwfm

    with open(rz_file) as f:
        rz_lines = f.read().splitlines()                # open and read input file
    line_index = iwfm.skip_ahead(0, rz_lines, 4)                # skip four parameters

    rz_dict = {}
    rz_dict['np_file'] = rz_lines[line_index].split()[0]        # non-ponded ag file

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    rz_dict['p_file'] = rz_lines[line_index].split()[0]         # ponded ag file

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    rz_dict['ur_file'] = rz_lines[line_index].split()[0]        # urban file

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    rz_dict['nr_file'] = rz_lines[line_index].split()[0]        # native and riparian file

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    rz_dict['rf_file'] = rz_lines[line_index].split()[0]        # return file file

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    rz_dict['ru_file'] = rz_lines[line_index].split()[0]        # reuse file

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    rz_dict['ir_file'] = rz_lines[line_index].split()[0]        # irrigation period file

    return rz_dict

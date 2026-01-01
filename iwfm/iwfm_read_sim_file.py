# iwfm_read_sim_file.py
# Read IWFM simulation main file and return dictionary of file names
# Copyright (C) 2020-2026 University of California
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


def iwfm_read_sim_file(sim_file):
    ''' iwfm_read_sim_file() - Read an IWFM Simulation main input file
        and return a list of the files called and some settings

    Parameters
    ----------
    sim_file : str
        name of existing nmodel main input file

    Returns
    -------
    sim_dict : dicttionary
        dictionary of existing model file names
    
    have_lake : bool
        True of existing model has a lake file

    '''
    import iwfm as iwfm

    with open(sim_file) as f:
        sim_lines = f.read().splitlines()              # open and read input file
    line_index = iwfm.skip_ahead(0, sim_lines, 3)               # skip comments

    sim_dict = {}
    sim_dict['preout'] = sim_lines[line_index].split()[0]       # preproc output file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_dict['gw_file'] = sim_lines[line_index].split()[0]      # groundwater main file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_dict['stream_file'] = sim_lines[line_index].split()[0]  # streams main file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    lake_file = sim_lines[line_index].split()[0]                # lake file
    have_lake = True
    if lake_file[0] == '/':
        lake_file = ''
        have_lake = False
    sim_dict['lake_file'] = lake_file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_dict['root_file'] = sim_lines[line_index].split()[0]    # root zone main file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_dict['swshed_file'] = sim_lines[line_index].split()[0]  # small watersheds file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_dict['unsat_file'] = sim_lines[line_index].split()[0]   # unsaturated zone file

    line_index = iwfm.skip_ahead(line_index + 3, sim_lines, 0) 
    sim_dict['precip_file'] = sim_lines[line_index].split()[0]  # precipitation file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_dict['et_file'] = sim_lines[line_index].split()[0]      # evapotranspiration file

    return sim_dict, have_lake

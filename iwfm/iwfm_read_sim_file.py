# iwfm_read_sim_file.py
# Read IWFM simulation main file and return dictionary of file names
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


def iwfm_read_sim_file(sim_file, debug=0):
    """ iwfm_read_sim_file() - Reads an IWFM Simulation main input file
        and returns a list of the files called and some settings.

    Parameters:
      sim_file       (str):  Name of existing nmodel main input file

    Returns:
      sim_dict       (dict):  Dictionary of existing model file names
      have_lake      (bool):  Does the existing model have a lake file?

    """
    import iwfm as iwfm

    if debug:
        print(f' --> Function iwfm_read_sim_file({sim_file})')

    # -- read the preprocessor file into array sim_lines
    sim_lines = open(sim_file).read().splitlines()  # open and read input file
    line_index = iwfm.skip_ahead(0, sim_lines, 3)  # skip comments

    # -- read input file names and create a dictionary ------------------
    sim_dict = {}
    sim_dict['preout'] = sim_lines[line_index].split()[0]  # preproc output file
    if debug:
        print(f'    --> {"preout"}: {sim_dict["preout"]}')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sim_dict['gw_file'] = sim_lines[line_index].split()[0]  # element file
    if debug:
        print(f'    --> {"gw_file"}: {sim_dict["gw_file"]}')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sim_dict['stream_file'] = sim_lines[line_index].split()[0]  # node file
    if debug:
        print(f'    --> {"stream_file"}: {sim_dict["stream_file"]}')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    lake_file = sim_lines[line_index].split()[0]  # lake file
    have_lake = True
    if lake_file[0] == '/':
        lake_file = ''
        have_lake = False
    sim_dict['lake_file'] = lake_file
    if debug:
        print(f'    --> {"lake_file"}: {sim_dict["lake_file"]}')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sim_dict['root_file'] = sim_lines[line_index].split()[0]  # stratigraphy file
    if debug:
        print(f'    --> {"root_file"}: {sim_dict["root_file"]}')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sim_dict['swshed_file'] = sim_lines[line_index].split()[0]  # stream file
    if debug:
        print(f'    --> {"swshed_file"}: {sim_dict["swshed_file"]}')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  # skip comments
    sim_dict['unsat_file'] = sim_lines[line_index].split()[0]  # stream file
    if debug:
        print(f'    --> {"unsat_file"}: {sim_dict["unsat_file"]}')

    return sim_dict, have_lake

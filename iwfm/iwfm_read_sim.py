# iwfm_read_sim.py
# Read IWFM Simulation main file
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


def iwfm_read_sim(sim_file, verbose=False):
    ''' iwfm_read_sim() - Read an IWFM Simulation main input file, and
        return a dictionary with the files called and some settings

    Parameters
    ----------
    sim_file : str
        Name of IWFM Simulation file

    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------
    sim_dict : dictionary
        Dictionary with fixed keys, file names for corresponding values
          Keys            Refers to
          ----            ----------
          preout          Preprocessor output file name
          gw              Groundwater main file name
          stream          Stream main file name
          lake            Lake main file name
          rootzone        Rootzone main file name
          smallwatershed  Small Watershed file name
          unsat           Unsaturated Zone file name
          irrfrac         Irrigation Fractions file name
          supplyadj       Supply Adjustment file name
          precip          Precipitation file name
          et              Evapotranspiration file name
          start           Starting date (DSS format)
          step            Time step (IWFM fixed set)
          end             Ending date (DSS format)

    '''
    import iwfm
    from iwfm.file_utils import read_next_line_value

    if verbose: print(f"Entered iwfm_read_sim() with {sim_file}")

    sim_dict = {}
    iwfm.file_test(sim_file)
    with open(sim_file) as f:
        sim_lines = f.read().splitlines()

    sim_dict['preout'], line_index = read_next_line_value(sim_lines, -1, skip_lines=3)

    sim_dict['gw'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['stream'], line_index = read_next_line_value(sim_lines, line_index)

    temp, line_index = read_next_line_value(sim_lines, line_index)
    if temp[0] == '/':   # check for presence of lake file
        lake_file = ''
    else:
        lake_file = temp
    sim_dict['lake'] = lake_file

    sim_dict['rootzone'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['smallwatershed'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['unsat'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['irrfrac'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['supplyadj'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['precip'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['et'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['start'], line_index = read_next_line_value(sim_lines, line_index)

    sim_dict['step'], line_index = read_next_line_value(sim_lines, line_index, skip_lines=1)

    sim_dict['end'], line_index = read_next_line_value(sim_lines, line_index)

    if verbose: print(f"Leaving iwfm_read_sim()")

    return sim_dict

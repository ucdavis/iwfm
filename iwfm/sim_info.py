# sim_info.py
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


def sim_info(in_file):
    ''' sim_info() - reads simulation input file and returns the starting date, ending
        date and time step of the simulation
        
    Parameters
    ----------
    in_file : str
        IWFM Simulation main input file

    Returns
    -------
    start_date : str
        simulation start date in DSS format

    end_date : str
        simulation end date in DSS format

    time_step : str
        time step in DSS format

    '''

    import iwfm as iwfm

    with open(in_file) as f:
        sim_lines = f.read().splitlines()          # open and read input file

    in_index = iwfm.skip_ahead(0,sim_lines,skip=14)
    start_date = sim_lines[in_index].split()[0]

    # Validate start_date format
    try:
        iwfm.validate_date_format(start_date, f'{in_file} line {in_index+1} start_date')
    except ValueError as e:
        raise ValueError(f"Error reading start date from {in_file} line {in_index+1}: {str(e)}") from e

    in_index = iwfm.skip_ahead(in_index,sim_lines,skip=2)
    time_step = sim_lines[in_index].split()[0]

    in_index += 1
    end_date = sim_lines[in_index].split()[0]

    # Validate end_date format
    try:
        iwfm.validate_date_format(end_date, f'{in_file} line {in_index+1} end_date')
    except ValueError as e:
        raise ValueError(f"Error reading end date from {in_file} line {in_index+1}: {str(e)}") from e

    return start_date, end_date, time_step

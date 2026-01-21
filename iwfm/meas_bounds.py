# meas_bounds.py
# determine upper and lower bounds of a list of values
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

# ** in development **


def meas_bounds(gwhyd_obs):
    ''' meas_bounds() - Determine the earliest and latest measurement dates 
        for a group of head observations in a linear list gwhyd_obs

    TODO: incomplete - finish this

    Parameters
    ----------
    gwhyd_obs : str
        observation file name
        format:       ' well_name              MM/DD/YYYY   HH:MM:SS   head_obs'
        example line: ' 11N19W05Q001S          01/28/1987   00:00:00   108.530'

    Returns
    -------
    nothing (yet)

    '''

    well_names, earliest, latest = [], [], []

    # Dead code - commented out due to undefined variables (incomplete implementation)
    # get the info from the first line
    # temp = gwhyd_obs[0].split()  # Fixed: added parentheses
    # with open(filename) as f:  # Error: 'filename' undefined - needs to be passed as parameter
    #     line = f.readline().split()  # Fixed: changed readline(f) to f.readline()
    #     well_name_temp = line[0]  # Fixed: changed line(0) to line[0]
    #  early_temp      =
    #  late_temp       =
    #    for i in range(0,len(gwhyd_obs[j])):
    #      date_temp.append(datetime.datetime.strptime(gwhyd_obs[j][i][0],'%m/%d/%Y'))
    #      sim_temp.append(gwhyd_obs[j][i][col])
    #    sim_dates.append(date_temp)
    #    sim_heads.append(sim_temp)
    print(f'  *** iwfm.meas_bounds.py: meas_bounds() not implemented yet ***')

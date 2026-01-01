# get_sim_hyd.py
# Get simulated hydrograph values
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


def get_sim_hyd(nt,file_name,start_date):
    ''' get_sim_hyd() - get simulated hydrograph values and return as a list of lists
        with row=timestep, 1st col=dates and remaining cols=sites, dates as datetime
        objects, everything else as numpy arrays of floats

    Parameters
    ----------
    nt : str
        hydrograph type

    file_name : str
        simulation hydrograph file name

    start_date : datetime object
        start date in 

    Returns
    -------
    sim_hyd : array
        simulation hydrograph values

    dates : list of ints
        days since start date for each row of sim_hyd

    '''
    import iwfm as iwfm
    import numpy as np

    with open(file_name) as f:
        hyd_lines = f.read().splitlines()
    hyd_index, dates, sim_hyd = 1, [], []

    while hyd_lines[hyd_index][0].isdigit() != True:                    # skip to the dates
        hyd_index += 1

    while hyd_index < len(hyd_lines) and hyd_lines[hyd_index][0].isdigit() == True:   # get the dates
        temp = hyd_lines[hyd_index].split()
        dates.append(iwfm.dts2days(iwfm.str2datetime(temp[0][:10]), start_date))    # days since start_date

        arr = []
        for i in range(1,len(temp)):
            arr.append(float(temp[i]))
        sim_hyd.append(np.array(arr))
        hyd_index += 1

    return sim_hyd, dates

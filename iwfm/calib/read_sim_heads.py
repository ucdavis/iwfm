# read_sim_heads.py
# reads simulated values from one IWFM output hydrograph files
# Copyright (C) 2018-2024 University of California
#-----------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------

def read_sim_heads(gwhyd_file):
    ''' read_sim_heads() reads simulated values from one IWFM output hydrograph files

    Parameters
    ----------
    gwhyd_file : str
        name of Groundwater.dat file to read

    Returns
    -------
    gwhyd_sim : list
        list of lists of simulated values
    
    dates : list
        list of dates corresponding to simulated values
    '''
    from datetime import datetime

    with open(gwhyd_file) as f:
        gwhyd_lines = f.read().splitlines()       # open and read input file
    gwhyd_lines = [word.replace('_24:00',' ') for word in gwhyd_lines]

    dates = []
    gwhyd_sim = []

    for j in range(9,len(gwhyd_lines)):     # process each libe
        line = gwhyd_lines[j].split()
        dates.append(datetime.strptime(line[0], "%m/%d/%Y"))
        line = list(map(float, line[1:]))
        gwhyd_sim.append(line)

    return gwhyd_sim, dates


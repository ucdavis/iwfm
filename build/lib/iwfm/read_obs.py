# read_obs.py
# Reads observed values smp file into array obs, including observation data
# hydrographs as lines, with observed values vs time as dots, saved as the well_name.pdf
# Copyright (C) 2020-2021 University of California
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


def read_obs(file):
    ''' read_obs() - Read observed values PEST-format smp file into array obs,
        including observation dates and measurements

    Parameters
    ----------
    file : str
        observation file name

    Returns
    -------
    obs : list
        observation dates and measurements
    
    '''

    file_lines = open(file).read().splitlines() 
    file_lines = [word.replace('_', ' ') for word in file_lines]

    obs = []
    for item in file_lines:
        item = item.split()
        obs.append([item[0], item[1], item[2], float(item[3])])
    return obs

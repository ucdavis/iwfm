# read_obs_smp.py
# Read observations from an smp file (PEST observation file)
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


def read_obs_smp(smp_file):
    ''' read_obs_smp() - Read the contents of the observed values smp file
    and return as array

    Parameters
    ----------
    smp_file : str
        PEST-style data file name (smp format)

    Returns
    -------
    obs : list
        data file contents
    
    '''
    file_lines = open(smp_file).read().splitlines() 
    file_lines = [word.replace("_", " ") for word in file_lines]

    obs = []
    for j in range(0, len(file_lines)):
        temp = file_lines[j].split()
        obs.append([temp[0], temp[1], temp[2], float(temp[3])])

    return obs

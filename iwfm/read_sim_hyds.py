# read_sim_hyds.py
# Read simulated hydrographs from IWFM hydrograph.out file
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


def read_sim_hyds(gwhyd_files):
    ''' read_sim_hyds() - Read simulated values from multiple IWFM output 
        hydrograph files into numpy arrays

    Parameters
    ----------
    gwhyd_files : list
        list of input file names

    Returns
    -------
    gwhyd_sim : list
        list with one item of hydrograph values for each input hydrograph file

    '''
    import numpy as np
    import datetime
    gwhyd_sim = []

    for k in range(0, len(gwhyd_files)):
        with open(gwhyd_files[k]) as f:
            gwhyd_lines = (f.read().splitlines())
        gwhyd_lines = [word.replace('_24:00', ' ') for word in gwhyd_lines]

        temp_sim = []
        for j in range(9, len(gwhyd_lines)):
            items= gwhyd_lines[j].split()
            temp = [datetime.datetime.strptime(items.pop(0),'%m/%d/%Y')]                   # date
            alist = [float(x) for x in items]       # values to floats
            temp.extend(alist)
            temp_sim.append(temp)
        gwhyd_sim.append(np.array(temp_sim))

    return gwhyd_sim

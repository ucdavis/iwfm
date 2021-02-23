# read_sim_hyds.py
# Read simulated hydrographs from IWFM hydrograph.out file
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


def read_sim_hyds(nhyds, gwhyd_files):
    """ read_sim_hyds() - Reads simulated values from multiple IWFM output 
        hydrograph files

    Parameters:
      nhyds           (int):   Number of simulated hydrograph files
      gwhyd_files     (list):  List of input file names

    Returns:
      gwhyd_sim       (list):  List with one item of hydrograph values for
                                 each input hydrograph file

    """
    gwhyd_sim = []

    for k in range(0, nhyds):
        gwhyd_lines = (
            open(gwhyd_files[k]).read().splitlines()
        )  # open and read input file
        gwhyd_lines = [word.replace('_24:00', ' ') for word in gwhyd_lines]

        temp = []
        for j in range(9, len(gwhyd_lines)):
            line = gwhyd_lines[j].split()
            for i in range(1, len(line)):
                line[i] = float(line[i])
            temp.append(line)
        gwhyd_sim.append(temp)
    return gwhyd_sim

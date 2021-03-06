# grid_read.py
# Reads an ASCII Grid file
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


def grid_read(infile):
    """grid_read() reads an ASCII Grid file"""
    import numpy as np

    skiprows = 6
    header = ''
    with open(infile, 'r') as f:
        for i in range(0, skiprows):
            header += f.readline()
    myArray = np.loadtxt(infile, skiprows=skiprows)
    return header, myArray

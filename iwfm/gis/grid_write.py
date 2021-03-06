# grid_write.py
# Writes an ASCII Grid file
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


def grid_write(outfile, array, xllcorner=277750.0, yllcorner=6122250.0, 
    cellsize=1.0, nodata=-9999):
    """grid_write() writes an ASCII Grid file"""
    import numpy as np

    header = 'ncols {}\n'.format(array.shape[1])
    header += 'nrows {}\n'.format(array.shape[0])
    header += 'xllcorner {}\n'.format(round(xllcorner, 1))
    header += 'yllcorner {}\n'.format(round(yllcorner, 1))
    header += 'cellsize {}\n'.format(round(cellsize, 1))
    header += 'NODATA_value {}\n'.format(nodata)
    with open(outfile, 'w') as f:
        f.write(header)
        np.savetxt(f, array, fmt='%1.2f')
    return

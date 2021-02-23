# histogram_array.py
# Determines the histogram function for multi-dimensional array
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


def histogram_array(arr, bins=list(range(0, 256))):
    """histogram_array() determines the histogram function for multi-dimensional array <a>.
    bins = range of numbers to match"""
    from osgeo import gdal_array as gdal_array

    fa = arr.flat
    n = gdal_array.numpy.searchsorted(gdal_array.numpy.sort(fa), bins)
    n = gdal_array.numpy.concatenate([n, [len(fa)]])
    hist = n[1:] - n[:-1]
    return hist

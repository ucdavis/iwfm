# img_stretch.py
# Stretches the color bands of an image
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


def img_stretch(infile, outfile):
    '''img_stretch() - Stretch the color bands of an image

    Parameters
    ----------
    infile : str
        image file name

    outfile : str
        modified image output file name

    Returns
    -------
    nothing
    
    '''
    from osgeo import gdal_array as gdal_array
    from stretch import stretch

    arr = gdal_array.LoadFile(infile)
    stretched = stretch(arr)
    output = gdal_array.SaveArray(arr, outfile, format='GTiff', prototype=infile)
    output = None

    return
    
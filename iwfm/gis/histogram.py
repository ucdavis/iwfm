# histogram.py
# Generates and displays the color histogram of an image
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


def histogram(infile, scl=True):
    '''histogram() - Generate and display the color histogram of an image
    
    Parameters
    ----------
    infile : str
        input image file

    scl : bool, default=True
        True = scaling on

    Returns
    -------
    nothing

    '''
    from osgeo import gdal_array as gdal_array
    import iwfm as iwfm

    t = None
    arr = gdal_array.LoadFile(infile)
    histograms = [hist(b) for b in arr]
    t = iwfm.gis.histogram_draw(histograms, scale=scl)
    t.pen(shown=False)
    t.done()
    return

# shp_bounds_fiona.py
# Return shapefile bounds with fiona
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


def shp_bounds_fiona(filename, verbose=False):
    ''' shp_bounds_fiona() - Return the bounds for shapefile opened with Fiona
    
    Parameters
    ----------
    filename : str
        input shapefile name

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    b : str
        shapefile bounding box

    '''
    import fiona

    with fiona.open(filename) as f:
        b = f.bounds
    if verbose:
        print(f' Shapefile {filename} bounds: {b}')
    return b

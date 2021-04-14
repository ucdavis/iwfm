# shp_len_fiona.py
# Return number of records in shapefile with fiona
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


def shp_len_fiona(filename):
    '''  shp_len_fiona() - Return the number of records in a shapefile
         opened with Fiona

    Parameters
    ----------
    filename : str
        shapefile name

    Returns
    -------
    l : int
        number of records
    
    '''
    import fiona

    f = fiona.open(filename)
    l = len(f)
    f = None
    return l

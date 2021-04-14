# shp_getrow.py
# Returns one row or record for a PyShp shapefile
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


def shp_getrow(inshape, rec):
    ''' shp_getrow() - Return one row or record for a shapefile opened
        with PyShp

    Parameters
    ----------
    inshape : PyShp shapefile object
    
    rec : int
        record number

    Returns
    -------
    one row record
    
    '''
    import iwfm as iwfm

    return iwfm.gis.shp_getrec(inshape, rec)

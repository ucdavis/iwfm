# geocode_json.py
# Return the lat-lon of a street address
# Copyright (C) 2020-2025 University of California
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

import geocoder

def geocode_json(address, verbose=False):
    ''' geocode_json() - Return the lat-lon of a street address
    
    Parameters
    ----------
    address : str
        street and city address

    verbose : bool, default=False
        True = command line output on
    
    Returns
    -------
    geocode of address : geojson format
    
    '''

    g = geocoder.osm(address)
    if verbose:
        print(f'  Geocode of {address} in geojson: {g.geojson}')
    return g.geojson

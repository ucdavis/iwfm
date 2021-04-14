# geocode_ex.py
# Example - finds the lat-lon of a street address and then
#     reverses to use the lat-lon to get the address information
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


def geocode_ex(address, verbose=False):
    ''' geocode_ex() - example: finds the lat-lon of a street address and then
        reverses to use the lat-lon to get the address information
    
    Parameters
    ----------
    adddress : str
        address
    
    verbose : bool, default=False
        True = command line update on

    Returns
    -------
    rev : str
        reversed address
    
    location.raw : str
        geocode of address

    '''
    from geopy.geocoders import Nominatim

    g = Nominatim()
    location = g.geocode(address)
    rev = g.reverse(f'{location.latitude},{location.longitude}')
    if verbose: 
        print(f'    Reversed address:  {rev}')
        print(f'    Geocode: {location.raw}')
    return rev, location.raw

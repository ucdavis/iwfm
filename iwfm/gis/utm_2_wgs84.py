# utm_2_wgs84.py
# Reproject from UTM to geographic coordinates
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


def utm_2_wgs84(zone, easting, northing):
    ''' utm_2_wgs84() - Reproject from UTM to geographic coordinates

    Parameters
    ----------
    zone : int or str
        UTM Zone

    easting : float
        Easting in UTM

    northing : float
        Northing in UTM

    Return
    ------
    (lon, lat, altitude) : tuple
        Longitude, Latitude, and altitude (0)

    '''
    import utm

    # Ensure zone is an integer
    zone = int(zone)

    # Determine hemisphere from northing value
    band = 'N' if northing >= 0 else 'M'

    # Convert UTM to lat/lon (returns lat, lon)
    lat, lon = utm.to_latlon(northing, easting, zone, band)

    # Return in original format: (lon, lat, altitude)
    return (lon, lat, 0)

# wgs84_2_utm.py
# Reproject from geographic coordinates to UTM
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


def wgs84_2_utm(lon, lat):
    """ wgs84_2_utm() - Reprojects a WGS84 shapefile to UTM

    Parameters:
      lat             (float): Latitude
      lon             (float): Longitude

    Returns:
      [easting, northing, altitude]
    
    """
    import osr as osr

    utm_coord_sys = osr.SpatialReference()
    
    # Set geographic coordinate system to handle lat/lon
    utm_coord_sys.SetWellKnownGeogCS('WGS84') 
    utm_coord_sys.SetUTM(get_utm_zone(lon), is_northern(lat))
    
    # Clone ONLY the geographic coordinate system
    wgs84_coord_sys = (utm_coord_sys.CloneGeogCS())  
    
    # create transform component
    wgs84_to_utm_transform = osr.CoordinateTransformation(
        wgs84_coord_sys, utm_coord_sys)  # (<from>, <to>)

    # returns easting, northing, altitude
    return wgs84_to_utm_transform.TransformPoint(lon, lat, 0)  

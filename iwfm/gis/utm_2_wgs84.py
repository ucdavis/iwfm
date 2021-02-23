# utm_2_wgs84.py
# Reproject from UTM to geographic coordinates
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


def utm_2_wgs84(zone, easting, northing):
    """Reproject from UTM to geographic coordinates"""
    import osr as osr

    utm_coordinate_system = osr.SpatialReference()
    utm_coordinate_system.SetWellKnownGeogCS(
        "WGS84"
    )  # Set geographic coordinate system to handle lat/lon
    is_northern = northing > 0
    utm_coordinate_system.SetUTM(zone, is_northern)
    wgs84_coordinate_system = (
        utm_coordinate_system.CloneGeogCS()
    )  # Clone ONLY the geographic coordinate system
    # create transform component
    utm_to_wgs84_transform = osr.CoordinateTransformation(
        utm_coordinate_system, wgs84_coordinate_system
    )  # (<from>, <to>)
    return utm_to_wgs84_transform.TransformPoint(
        easting, northing, 0
    )  # returns lon, lat, altitude

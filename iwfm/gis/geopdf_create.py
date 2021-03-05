# geopdf_create.py
# Create a geopdf canvas
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


def geopdf_create(filename):
    """ geopdf_create() - Create a geopdf canvas that can be drawn on

    Parameters:
      filename        (str):  File name to import

    Returns:
      canvas          (obj):  geopdf object
    """
    from geopdf import GeoCanvas

    canvas = GeoCanvas(filename)
    return canvas

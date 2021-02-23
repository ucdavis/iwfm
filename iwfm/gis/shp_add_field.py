# shp_add_field.py
# Add a field to a shapefile with PyShp
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


def shp_add_field(shapefilename, name="TEST", type="F", length=8, prec=5):
    """Add a field to a shapefile with PyShp"""
    import shapefile  # PyShp

    r = shapefile.Reader(shapefilename)
    with shapefile.Writer(name, r.shapeType) as w:
        w.fields = list(r.fields)
        w.field(name, type, length, prec)
    return 0

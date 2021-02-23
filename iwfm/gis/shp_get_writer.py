# shp_get_writer.py
# Get a writer for a shapefile of the same type as the input shapefile
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


def shp_get_writer(outfile, type, debug=0):
    """Get a writer for a shapefile of the same type as the input shapefile"""
    import shapefile  # PyShp

    if debug:
        print("      shp_get_writer()")
    w = shapefile.Writer(outfile, shapeType=type)  # get Writer
    if debug:
        print("      - shp_type(in):  {}".format(type))
        print("      - shp_type(out): {}".format(shp_type(w)))
        print("      - leaving shp_get_writer()")
    return w

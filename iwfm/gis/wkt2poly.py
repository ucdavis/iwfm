# wkt2poly.py
# Convert WKT-format text string into polygon
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


def wkt2poly(intxt):
    """ wkt2poly(): turn WKT text description into object"""
    import wkt

    wktPoly = intxt  # intxt example: "POLYGON((0 0,4 0,4 4,0 4,0 0))"
    poly = wkt.loads(wktPoly)

    return poly

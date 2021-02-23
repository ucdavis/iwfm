# world2screen.py
# Convert geospatial coordinates to screen pixels for display
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


def world2screen(bbox, w, h, x, y):
    """ world2screen() - Converts geospatial coordinates to screen pixels


    Parameters:
      bbox            (list):  Bounding box [minx, miny, maxx, maxy]
      w               (int):   Screen width in pixels
      h               (int):   Screen height in pixels
      x               (float): X-coordinate to be transformed
      y               (float): Y-coordinate to be transformed

    Returns:
      px, py          (int):   Coordinates in pixels
    """
    minx, miny, maxx, maxy = bbox
    xdist = maxx - minx
    ydist = maxy - miny
    xratio = w / xdist
    yratio = h / ydist
    px = int(w - ((maxx - x) * xratio))
    py = int((maxy - y) * yratio)
    return (px, py)

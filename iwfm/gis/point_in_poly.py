# point_in_poly.py
# Is the point inside the polygon?
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


def point_in_poly(x, y, poly):
    """ point_in_poly() - Is the point inside the polygon?

    Parameters:
      x               (float): Easting 
      y               (float): Northing
      ppoly           (obj):   A polygon object

    Returns:
      TRUE if point <x,y> is inside or on an edge
      FALSE otherwise
    """
    if (x, y) in poly:  # check if point is a vertex
        return True
    for i in range(len(poly)):  # check if point is on a boundary
        p1 = None
        p2 = None
        if i == 0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i - 1]
            p2 = poly[i]
        if (
            p1[1] == p2[1]
            and p1[1] == y
            and x > min(p1[0], p2[0])
            and x < max(p1[0], p2[0])
        ):
            return True
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside  # reverse each time it crosses a line
        p1x, p1y = p2x, p2y
    if inside:
        return True
    return False

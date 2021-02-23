# nearest_node.py
# Return nearest IWFM node to an (x,y) location
# the nearest node to each (x,y) point
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


def nearest_node(point, node_set):
    """ nearest_node() - Find the nearest node to a point from the node array

    Parameters:
      point           (tuple): (x,y) point
      node_set        (list):  List of node numbers with x and y of each

    Returns:
      nearest         (int):  Number of nearest node
    """
    import iwfm as iwfm

    dist = 9.9e30
    nearest = -1
    for j in range(0, len(node_set)):
        line = node_set[j]
        pt = [line[1], line[2]]
        new_dist = iwfm.distance(
            point, pt
        )  # Computes distance between each pair of the two collections of inputs.
        if dist > new_dist:
            dist = new_dist
            nearest = line[0]
    return nearest

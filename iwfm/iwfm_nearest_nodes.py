# iwfm_nearest_nodes.py
# Read a file with (x,y) locations and an IWFM node file, and write a file with
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


def iwfm_nearest_nodes(filename, node_set):
    """ iwfm_nearest_nodes() - Read a point file, calculate the nearest node 
        and distance for each point, and write the results to the output file

    Parameters:
      filename        (str):  File containing x,y points
      node_set        (list): Node IDs and x,y locations

    Returns:
      number of points processed
    """
    import iwfm as iwfm

    output_filename = filename[0 : filename.find('.')] + '_nodes.out'
    with open(output_filename, 'w') as output_file:
        with open(filename, 'r') as input_file:
            lines = input_file.read().splitlines()  # open and read input file
            output_file.write('{}\tNdNear\tNdDist\n'.format(lines[0]))
            for line_index in range(1, len(lines)):  # skip header line
                temp = lines[line_index].split()
                nearest = iwfm.nearest_node(
                    [float(temp[1]), float(temp[2])], node_set, debug
                )  # ID of nearest node
                dist = iwfm.distance(
                    [float(temp[1]), float(temp[2])],
                    [node_set[nearest][1], node_set[nearest][2]],
                )  # calculate distance to node
                # write out
                output_file.write(
                    '{}\t{}\t{}\n'.format(lines[line_index], nearest, dist)
                )
    return len(lines) - 1

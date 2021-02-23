# iwfm_read_streams.py
# read IWFM preprocessor streams file
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


def iwfm_read_streams(stream_file):
    """ iwfm_read_streams() - Read an IWFM Stream Geometry file and return
        a list of stream reaches, a dictionary of stream nodes, and the 
        number of stream nodes.

    Parameters:
      stream_file      (str):  Name of IWFM Streams file (v4.2)

    Returns:
      reach_list       (list): Information for each stream reach
      stnodes_dict     (dict): Dictionary of stream node info
      len(snodes_list) (int):  Number of stream nodes
      rating_dict      (dict): Dictionary of rating table info
    """
    import iwfm as iwfm

    comments = 'Cc*#'
    stream_lines = open(stream_file).read().splitlines()  # open and read input file
    stream_index = 0  # start at the top
    stream_index = iwfm.skip_ahead(stream_index, stream_lines, 0)  # skip comments
    nreach = int(stream_lines[stream_index].split()[0])

    stream_index += 1
    rating = int(stream_lines[stream_index].split()[0])

    reach_list = []
    snodes_list = []
    nsnodes = 0
    for i in range(0, nreach):  # cycle through stream reaches
        # read reach information
        stream_index = iwfm.skip_ahead(
            stream_index + 1, stream_lines, 0
        )  # skip comments
        l = stream_lines[stream_index].split()
        # streams package version 4.2
        reach = int(l.pop(0))
        snodes = int(l.pop(0))
        # streams package version 5
        # upper = int(l.pop(0))
        # lower = int(l.pop(0))
        # snodes = lower - upper + 1
        oflow = int(l.pop(0))

        # read stream node information
        for j in range(0, snodes):
            stream_index = iwfm.skip_ahead(
                stream_index, stream_lines, 1
            )  # skip comments
            l = stream_lines[stream_index].split()
            t = [int(l[0]), int(l[1]), reach]  #  snode, GW Node
            snodes_list.append(t)
            if j == 0:
                upper = int(l[0])
            else:
                lower = int(l[0])
        reach_list.append([reach, upper, lower, oflow])

    stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 3)  # skip comments
    rating_dict = {}
    selev = []
    for i in range(
        0, len(snodes_list)
    ):  # cycle through stream nodes in rating table section
        l = stream_lines[stream_index].split()
        snd = l[0]
        selev.append(float(l[1]))
        # read the rating table values for this stream node
        temp = [[l[2], l[3]]]
        stream_index += 1
        for t in range(0, rating - 1):
            if any(
                (c in comments) for c in stream_lines[stream_index][0]
            ):  # skip lines that begin with 'C', 'c' or '*'
                stream_index += 1
            temp.append(stream_lines[stream_index].split())
            stream_index += 1
        rating_dict[snd] = temp
        # stream_index = stream_index + rating

        if i < len(snodes_list) - 1:  # stop at end
            stream_index = iwfm.skip_ahead(
                stream_index, stream_lines, 0
            )  # skip comments

    # put stream node info into a dictionary
    stnodes_dict = {}
    for i in range(
        0, len(snodes_list)
    ):  # cycle through stream nodes in order 1 - nsnodes
        j = 0
        while snodes_list[j][0] != i + 1:  # find info for i in snodes list
            j += 1
        key, values = i + 1, [
            snodes_list[j][1],
            snodes_list[j][2],
            selev[i],
        ]  # key = snode, values = GW Node, Reach, Bottom
        stnodes_dict[key] = values

    return reach_list, stnodes_dict, len(snodes_list), rating_dict

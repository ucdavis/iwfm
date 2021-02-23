# igsm_read_streams.py
# Read an IGSM pre-processor streams file
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


def igsm_read_streams(stream_file, debug=0):
    """Function igsm_read_streams(stream_file,debug = 0) reads an IGSM Stream Geometry
    file and returns (a) a list of stream reaches and (b) a dictionary of stream nodes,
    and (c) the number of stream nodes."""
    import iwfm as iwfm

    stream_lines = open(stream_file).read().splitlines()  # open and read input file
    stream_index = 0  # start at the top
    stream_index = iwfm.skip_ahead(stream_index, stream_lines, 0)  # skip comments
    nreach = int(stream_lines[stream_index].split()[0])
    stream_index += 1
    rating = stream_lines[stream_index].split()[0]
    reach_list = []
    snodes_list = []
    nsnodes = 0

    for i in range(0, nreach):  # cycle through stream reaches
        # read reach information
        stream_index = iwfm.skip_ahead(
            stream_index + 1, stream_lines, 0
        )  # skip comments
        l = stream_lines[stream_index].split()
        reach = int(l.pop(0))
        upper = int(l.pop(0))
        lower = int(l.pop(0))
        oflow = int(l.pop(0))
        reach_list.append([reach, upper, lower, oflow])
        # read stream node information
        snodes = lower - upper + 1
        for j in range(0, snodes):
            stream_index = iwfm.skip_ahead(
                stream_index, stream_lines, 1
            )  # skip comments
            l = stream_lines[stream_index].split()
            t = [
                int(l[0]),
                int(l[1]),
                int(l[2]),
                reach,
            ]  #  snode, GW Node, Subregion, Reach
            snodes_list.append(t)
    stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 0)  # skip comments
    selev = []

    for i in range(
        0, len(snodes_list)
    ):  # cycle through stream nodes in rating table section
        l = stream_lines[stream_index].split()
        selev.append(int(l[1]))
        if i < len(snodes_list) - 1:  # stop at end
            stream_index = iwfm.skip_ahead(
                stream_index + 1, stream_lines, 4
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
            snodes_list[j][3],
            selev[i],
        ]  # key = snode, values = GW Node, Subregion, Reach, Bottom
        stnodes_dict[key] = values

    return reach_list, stnodes_dict, len(snodes_list)

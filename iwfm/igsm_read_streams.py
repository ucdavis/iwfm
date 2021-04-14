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


def igsm_read_streams(stream_file):
    ''' igsm_read_streams() - Reads an IGSM Stream Geometry file and returns 
        (a) a list of stream reaches and (b) a dictionary of stream nodes, and 
        (c) the number of stream nodes

    Parameters
    ----------
    stream_file : str
        Name of existing IWFM stream file

    Returns
    -------
    reach_list : list
        Stream reach information

    stnodes_dict : dict
        Stream nodes dictionary

    len(snodes_list) : int
        Number of stream nodes

    '''
    import iwfm as iwfm

    stream_lines = open(stream_file).read().splitlines() 
    stream_index = 0  # start at the top
    stream_index = iwfm.skip_ahead(stream_index, stream_lines, 0)  
    nreach = int(stream_lines[stream_index].split()[0])
    stream_index += 1
    rating = stream_lines[stream_index].split()[0]
    reach_list = []
    snodes_list = []
    nsnodes = 0

    for i in range(0, nreach):  
        # read reach information
        stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 0)  
        l = stream_lines[stream_index].split()
        reach = int(l.pop(0))
        upper = int(l.pop(0))
        lower = int(l.pop(0))
        oflow = int(l.pop(0))
        reach_list.append([reach, upper, lower, oflow])
        # read stream node information
        snodes = lower - upper + 1
        for j in range(0, snodes):
            stream_index = iwfm.skip_ahead(stream_index, stream_lines, 1) 
            l = stream_lines[stream_index].split()
            t = [int(l[0]),int(l[1]),int(l[2]),reach] 
            snodes_list.append(t)
    stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 0)  
    selev = []

    # cycle through stream nodes in rating table section
    for i in range(0, len(snodes_list)):  
        l = stream_lines[stream_index].split()
        selev.append(int(l[1]))
        if i < len(snodes_list) - 1:  
            stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 4)

    # put stream node info into a dictionary
    stnodes_dict = {}
    for i in range(0, len(snodes_list)):  
        j = 0
        while snodes_list[j][0] != i + 1: 
            j += 1
        # key = snode, values = GW Node, Subregion, Reach, Bottom
        key, values = i + 1, [snodes_list[j][1],snodes_list[j][2],
            snodes_list[j][3],selev[i]]  
        stnodes_dict[key] = values

    return reach_list, stnodes_dict, len(snodes_list)

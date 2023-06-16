# iwfm_read_streams.py
# read IWFM preprocessor streams file
# Copyright (C) 2020-2023 University of California
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
    ''' iwfm_read_streams() - Read an IWFM Stream Geometry file and return
        a list of stream reaches, a dictionary of stream nodes, and the 
        number of stream nodes

    Parameters
    ----------
    stream_file : str
        IWFM Streams file name

    Returns
    -------
    reach_list : list
        information for each stream reach
    
    stnodes_dict : dictionary
        key = stream node ID, value = groundwater node
    
    len(snodes_list) : int
        number of stream nodes
    
    rating_dict : dictionary
        key = stream node ID, values = rating table
    
    '''
    import iwfm as iwfm

    iwfm.file_test(stream_file)
    comments = 'Cc*#'

    stream_lines = open(stream_file).read().splitlines()  
    stream_type = stream_lines[0][1:]
    stream_index = iwfm.skip_ahead(1, stream_lines, 0)  

    nreach = int(stream_lines[stream_index].split()[0])
    stream_index += 1
    rating = int(stream_lines[stream_index].split()[0])

    # read in stream reaches
    reach_list, snodes_list, nsnodes = [], [], 0
    for i in range(0, nreach):  
        stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 0)
        l = stream_lines[stream_index].split()

        reach = int(l.pop(0))

        # ***** TODO ************************************
        # Handle multiple types of stream packages (stream_type)
        # ***** TODO ************************************

        # streams package versions 4.0, 4.1, 4.2
        if stream_type == '4.0'or stream_type == '4.1' or stream_type == '4.2':
            snodes = int(l.pop(0))

        # streams package version 5
        elif stream_type == '5':
            up_node = int(l.pop(0))
            dn_node = int(l.pop(0))
            snodes = dn_node - up_node + 1

        # old streams package versions...?
        else: 
            up_node = int(l.pop(0))
            dn_node = int(l.pop(0))
            snodes = dn_node - up_node + 1

        oflow = int(l.pop(0))

        # read stream node information
        for j in range(0, snodes):
            stream_index = iwfm.skip_ahead(stream_index, stream_lines, 1)
            l = stream_lines[stream_index].split()
            t = [int(l[0]), int(l[1]), reach]  
            snodes_list.append(t)
            if j == 0:
                upper = int(l[0])
            else:
                lower = int(l[0])
        reach_list.append([reach, upper, lower, oflow])

    stream_index = iwfm.skip_ahead(stream_index + 1, stream_lines, 3) 
    rating_dict = {}
    selev = []
    for i in range(0, len(snodes_list)):
        l = stream_lines[stream_index].split()
        snd = l[0]
        selev.append(float(l[1]))
        # read the rating table values for this stream node
        temp = [[l[2], l[3]]]
        stream_index += 1
        for t in range(0, rating - 1):
            if any((c in comments) for c in stream_lines[stream_index][0]):
                stream_index += 1
            temp.append(stream_lines[stream_index].split())
            stream_index += 1
        rating_dict[snd] = temp

        if i < len(snodes_list) - 1:  # stop at end
            stream_index = iwfm.skip_ahead(stream_index, stream_lines, 0)

    # put stream node info into a dictionary
    stnodes_dict = {}
    for i in range(0, len(snodes_list)):
        j = 0
        while snodes_list[j][0] != i + 1:  # find info for i in snodes list
            j += 1
        key, values = i + 1, [snodes_list[j][1],snodes_list[j][2],selev[i]]
        stnodes_dict[key] = values

    return reach_list, snodes_list, stnodes_dict, len(snodes_list), rating_dict

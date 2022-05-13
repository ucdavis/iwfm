# get_stream_list_42.py
# Reads part of the stream specification file for file type 4.2
# and returns stream reach and rating table info
# Copyright (C) 2020-2021 University of California
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


def get_stream_list_42(stream_lines, line_index, nreach, nrate):
    ''' get_stream_list_42() - Reads part of the stream specification file
        for file type 4.2 and returns stream reach and rating table info

    Parameters
    ----------
    stream_lines : list of strings
        contents of stream specification file
    
    line_index : int
        current item in stream_lines
    
    nreach : int
        number of stream reaches
    
    nrate : int
        number of points in each stream node rating table

    Returns
    -------
    snode_ids : list
        list of model stream nodes
    
    snode_dict : dictionary
        keys = stream node IDs, values = associated groundwater nodes
    
    reach_info : list
        reach info lines for reaches in model
    
    rattab_dict : dictionary
        keys = stream node IDs, values = rating tables
    
    rating_header : str
        header info for rating tables including factors
    
    stream_aq : str
        stream-aquifer section of stream preprocessor file

    '''
    import iwfm as iwfm

    comments = ['Cc*#']
    reach_ids, reach_nodes, reach_outflows, reach_names = [], [], [], []
    reach_info, snode_ids, rating_header, stream_aq = [], [], [], []

    # -- first section, reaches
    snode_dict = {}
    for reach in range(0, nreach):
        line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0) 
        info = stream_lines[line_index].split()  # -- get reach information

        snodes_temp, gwnodes_temp = [], []

        for sn in range(0, int(info[1])):
            line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0) 
            temp = stream_lines[line_index].split()
            snodes_temp.append(int(temp[0]))  
            gwnodes_temp.append(int(temp[1])) 
            snode_ids.append(int(temp[0])) 
            snode_dict[int(temp[0])] = int(temp[1])

        reach_info.append(
            [
                int(info[0]),
                int(info[1]),
                int(info[2]),
                ' '.join(info[3:]),
                snodes_temp,
                gwnodes_temp,
            ]
        )

    # -- second section, rating table factors
    line_index += 1
    while stream_lines[line_index][0] in comments:
        rating_header.append(stream_lines[line_index])
        line_index += 1

    for i in range(0, 3):
        rating_header.append(stream_lines[line_index])
        line_index += 1

    while stream_lines[line_index][0] in comments:
        rating_header.append(stream_lines[line_index])
        line_index += 1

    # -- read in the rating tables for each stream node
    rattab_dict = {}
    line_index -= 1  # back up one before starting
    for sn in snode_ids:
        rt_temp = []
        for t in range(0, nrate):  # nrate lines, already read first one
            line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0)
            rt_temp.append(stream_lines[line_index])
        rattab_dict[sn] = rt_temp

    # -- copy the last section, partial stream-aquifer interaction, to a list
    line_index += 1
    while line_index < len(stream_lines):
        stream_aq.append(stream_lines[line_index])
        line_index += 1

    return snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq

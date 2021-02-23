# sub_pp_streams.py
# Reads the stream specification file and returns stream reach and
# rating table info
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


def sub_pp_streams(stream_file, node_list):
    """sub_pp_streams() reads the stream specification file and returns
        stream reach and rating table info for the submodel

    Parameters:
      stream_file     (str):   Existing model preprocessor stream file name
      node_list       (list):  List of existing model nodes in submodel

    Returns:
      sub_reach_info  (list):  Reach info line for reaches in submodel
      snode_dict      (dict):  Dictionary of existing model stream nodes in submodel
      sub_rattab_dict (dict):  Rating tables for stream nodes in submodel
      rating_header   (str):   Header info for rating tables including factors
      stream_aq       (str):   Stream-aquifer section of stream preprocessor file

    """
    import iwfm as iwfm

    nodes = []
    for n in node_list:
        nodes.append(int(n))

    # -- read the stream specification file into array elem_lines
    stream_lines = open(stream_file).read().splitlines()  # open and read input file

    # -- determine stream specification version
    stream_type = stream_lines[0][1:]

    ## -- skip to number of stream reaches
    line_index = iwfm.skip_ahead(0, stream_lines, 0)  # skip comments
    nreach = int(stream_lines[line_index].split()[0])

    # -- skip to number of rating table points
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0)  # skip comments
    nrate = int(stream_lines[line_index].split()[0])

    # -- get stream reach information
    if stream_type == '4.0':
        # placeholder for iwfm.get_stream_list_40()
        # snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = iwfm.get_stream_list_40(stream_lines,line_index,nreach,nrate)
        exit_now(stream_type)
    elif stream_type == '4.1':
        # placeholder for iwfm.get_stream_list_41()
        # snode_ids, snode_dict, reach_info, rattab_dict, rating_header, stream_aq = iwfm.get_stream_list_41(stream_lines,line_index,nreach,nrate)
        exit_now(stream_type)
    elif stream_type == '4.2':
        (
            snode_ids,
            snode_dict,
            reach_info,
            rattab_dict,
            rating_header,
            stream_aq,
        ) = iwfm.get_stream_list_42(stream_lines, line_index, nreach, nrate)
    else:
        exit_now(stream_type)

    # -- list of stream nodes in submodel
    sub_snodes = []
    for sn in snode_ids:
        if snode_dict[sn] in nodes:
            sub_snodes.append(sn)

    # -- cycle through stream reaches, determine if all in, part in, or out of submodel
    sub_reach_info = []
    for i in range(0, len(reach_info)):
        reach_snodes = []
        for j in range(0, len(reach_info[i][4])):
            if reach_info[i][4][j] in sub_snodes:
                reach_snodes.append(reach_info[i][4][j])
        if len(reach_snodes) > 0:
            temp = reach_info[i][0:4]
            temp.append(reach_snodes)
            sub_reach_info.append(temp)

    # -- cycle through rating tables, keeping those in submodel
    rattab_sns = [*rattab_dict]
    sub_rattab_dict = {}
    for sn in rattab_sns:
        if sn in sub_snodes:
            sub_rattab_dict[sn] = rattab_dict[sn]

    return sub_reach_info, snode_dict, sub_rattab_dict, rating_header, stream_aq


def exit_now(stream_type):
    print(f'  ** Error.')
    print(f'  ** No method to read stream specification type {stream_type}')
    print(f'  ** Exiting...\n')
    import sys

    sys.exit()

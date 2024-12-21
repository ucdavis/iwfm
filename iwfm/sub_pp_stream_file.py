# sub_pp_stream_file.py
# Copies the old stream file and replaces the contents with those of the new
# submodel, and writes out the new file
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


def sub_pp_stream_file(stream_file, new_stream_file, snode_dict, reach_info,
    rattab_dict, rating_header, stream_aq):
    ''' sub_pp_stream_file() - Copy the original stream specification file 
        and replace the contents with those of the new model, and write
        out the new file

    Parameters
    ----------
    stream_file : str
        name of existing preprocessor node file
    
    new_stream_file : str
        name of submodel preprocessor node file
    
    snode_dict : ints
        dictionary of existing model stream nodes in submodel
    
    reach_info : str
        reach info line for reaches in submodel
    
    rattab_dict : dict
        rating tables for stream nodes in submodel
    
    rating_header : str
        header info for rating tables including factors
    
    stream_aq : str
        stream-aquifer section of stream preprocessor file

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    stream_lines = open(stream_file).read().splitlines()

    stream_type = stream_lines[0][1:]

    line_index = iwfm.skip_ahead(0, stream_lines, 0)  # skip comments
    sub_stream_lines = stream_lines[:line_index]

    # -- number of stream reaches
    sub_stream_lines.append(
        iwfm.pad_both(str(len(reach_info)), f=4, b=35)
        + ' '.join(stream_lines[line_index].split()[1:])
    )

    # -- number of points in each rating table
    rattab_sns = [*rattab_dict]
    sub_stream_lines.append(
        iwfm.pad_both(str(len(rattab_dict[rattab_sns[0]])), f=4, b=35)
        + ' '.join(stream_lines[line_index].split()[1:])
    )

    # -- write stream reach and rating table information
    if stream_type == '4.0':
        # TODO - add add_streams_40()
         # placeholder for add_streams_40()
        # sub_stream_lines = add_streams_40(sub_stream_lines, reach_info, snode_dict, rattab_dict, rating_header, stream_aq)
        exit_now(stream_type)
    elif stream_type == '4.1':
        # TODO - add add_streams_41()
        # placeholder for add_streams_41()
        # sub_stream_lines = add_streams_41(sub_stream_lines, reach_info, snode_dict, rattab_dict, rating_header, stream_aq)
        exit_now(stream_type)
    elif stream_type == '4.2':
        sub_stream_lines = add_streams_42( sub_stream_lines, reach_info, snode_dict, rattab_dict,
            rating_header, stream_aq)
    else:
        exit_now(stream_type)

    sub_stream_lines.append('')
    # -- write new stream specification file
    with open(new_stream_file, 'w') as outfile:
        outfile.write('\n'.join(sub_stream_lines))

    return


def add_streams_42(sub_stream_lines, reach_info, snode_dict, rattab_dict, rating_header, stream_aq):
    ''' add_streams_42()  - adds the reach and rating table info in the format of
        stream file type 4.2
    
    Parameters
    ----------
    sub_stream_lines : list
        sumbodel stream file being assembled
    
    reach_info : list
        ** TODO description **
    
    snode_dict : dictionary
        key = stream node ID, values = groundwater node
    
    rattab_dict : dictionary
        key = stream node ID, values = rating table contents
    
    rating_header : list of strings
        rating table comments and flags/constants from original streams file
    
    stream_aq : list of strings
        stream-aquifer section of original streams file
    
    Returns
    -------
    sub_stream_lines : list
        ** TODO description **

    '''

    # -- write stream reaches
    for s in reaches_header_42:
        sub_stream_lines.append(s)

    for r in reach_info:
        sub_stream_lines.append('C     REACH   ' + str(r[0]))
        for s in reach_header_42:
            sub_stream_lines.append(s)
        # write reach information
        sub_stream_lines.append(
            '\t' + str(r[0]) + '\t' + str(r[1]) + '\t' + str(r[2]) + '\t' + r[3]
        )
        for s in snodes_header_42:
            sub_stream_lines.append(s)
        # write reach stream nodes
        for sn in r[4]:
            sub_stream_lines.append('\t' + str(sn) + '\t' + str(snode_dict[sn]))
        sub_stream_lines.append(
            'C-------------------------------------------------------------------------------'
        )

    # -- write rating tables
    for s in rating_header:
        sub_stream_lines.append(s)

    rattab_sns = [*rattab_dict]
    for sn in rattab_sns:
        for s in rattab_dict[sn]:
            sub_stream_lines.append(s)

    # -- write stream-aquifer section
    for s in stream_aq:
        sub_stream_lines.append(s)

    return sub_stream_lines


reaches_header_42 = [
    'C*******************************************************************************',
    'C                      Description of Stream Reaches',
    'C',
    'C   The following lists the stream nodes and corresponding groundwater',
    'C   nodes for each stream reach modeled in IWFM.',
    'C',
    'C   ID;    Reach number',
    'C   IBUR;  First upstream stream node of the reach',
    'C   IBDR;  Last downstream node of the reach',
    'C   IDWN;  Stream node into which the reach flows into',
    'C              0: If stream flow leaves the modeled area',
    'C           -nlk: If stream flows into lake number nlk',
    'C   NAME;  Name of the reach (maximum 20 characters)',
    'C',
    'C   In addition, for each stream node within the reach the corresponding',
    'C   groundwater nodes is listed.',
    'C',
    'C   IRV;   Stream node',
    'C   IGW;   Corresponding groundwater node(s) (can be more than one for wide streams)',
    'C           * Note: For wide streams with more than one corresponding groundwater nodes,',
    'C                    the groundwater node that is closest to the middle of the channel',
    'C                    cross-section must be listed first.',
    'C',
    'C-------------------------------------------------------------------------------',
]

reach_header_42 = [
    'C	Reach	Number	Outflow	Reach',
    'C	Node	Nodes	Node	Name',
    'C	ID	NRD	IDWN	NAME',
    'C-------------------------------------------------------------------------------',
]

snodes_header_42 = [
    'C-------------------------------------------------------------------------------',
    'C	Stream	Groundwater',
    'C    node  node',
    'C	IRV	IGW',
    'C-------------------------------------------------------------------------------',
]


def exit_now(stream_type):
    print(f'  ** Error.')
    print(f'  ** No method to wrwite stream specification type {stream_type}')
    print(f'  ** Exiting...\n')
    import sys

    sys.exit()

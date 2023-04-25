# sub_streams_file.py
# Copies the old Simulation streams main file and replaces the contents with 
# those of the new submodel, and writes out the new file, then calls methods 
# to modify the other Simulation stream component files
# Copyright (C) 2020-2022 University of California
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


def sub_streams_file(sim_dict, sim_dict_new, elem_list, sub_snodes, verbose=False):
    '''sub_streams_file() - Read the original Simulation streams main file, 
        determine which elements are in the submodel, and writes out a new file, 
        then modifies the other Simulation stream component files

    Parameters
    ----------
    sim_dict : dictionary
        existing model file names

    sim_dict_new : str
        new subnmodel file names

    elem_list : list of ints
        list of existing model elements in submodel

    sub_snodes : list of ints
        submodel stream nodes

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    comments = ['C','c','*','#']

    stream_lines = open(sim_dict['stream_file']).read().splitlines()  
    stream_lines.append('')

    line_index = iwfm.skip_ahead(1, stream_lines, 0)                # skip initial comments

    st_dict = {}

    # inflow file name
    inflow_file = stream_lines[line_index].split()[0]                   # stream inflow file
    have_inflow = True
    if inflow_file[0] == '/':
        inflow_file = ''
        have_inflow = False
        stream_lines[line_index] = '                                         / INFLOWFL'
    else:
        inflow_file = inflow_file.replace('\\', ' ').split()[1]
        stream_lines[line_index] = '   ' + sim_dict_new['stin_file'] + '.dat		        / INFLOWFL'
    st_dict['stin_file'] = inflow_file

    # diversion specification file name
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0) 
    divspec_file = stream_lines[line_index].split()[0]                   # tile drain main file
    have_divspec = True
    if divspec_file[0] == '/':
        divspec_file = ''
        have_divspec = False
        stream_lines[line_index] = '                                         / DIVSPECFL'
    else:
        divspec_file = divspec_file.replace('\\', ' ').split()[1]
        stream_lines[line_index] = '   ' + sim_dict_new['divspec_file'] + '.dat		        / DIVSPECFL'
    st_dict['divspec_file'] = divspec_file

    # bypass specification file name
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0) 
    bp_file = stream_lines[line_index].split()[0]                 # bypass specification file
    bp_line = line_index
    have_bp = True
    if bp_file[0] == '/':
        bp_file = ''
        have_bp = False
        stream_lines[line_index] = '                                         / BYPSPECFL'
    else:
        bp_file = bp_file.replace('\\', ' ').split()[1]     
        stream_lines[line_index] = '   ' + sim_dict_new['bp_file'] + '.dat		        / BYPSPECFL'
    st_dict['bp_file'] = bp_file

    # diversion time series file
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0) 
    div_file = stream_lines[line_index].split()[0]           # subsidence main file
    have_div = True
    if div_file[0] == '/':
        div_file = ''
        have_div = False
        stream_lines[line_index] = '                                         / DIVFL'
    else:
        div_file = div_file.replace('\\', ' ').split()[1]
        stream_lines[line_index] = '   ' + sim_dict_new['div_file'] + '.dat		        / DIVFL'
    st_dict['div_file'] = div_file

    # skip comments to hydrograph section
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 2)

    nhyds = int(stream_lines[line_index].split()[0])                # number of hydrographs
    hyds_line = line_index
 
    # --  hydrograph section --
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 6)
 
    # check each hydrographs and remove the hydrographs outside the submodel boundary
    new_hyds = 0 
    for i in range(0, nhyds):
        sn = int(stream_lines[line_index].split()[0])

        if sn not in sub_snodes:
            del stream_lines[line_index]
        else:
            new_hyds += 1
            line_index += 1

    # update the number of hydrographs
    stream_lines[hyds_line] = '     ' + str(new_hyds) + '        / NOUTR'
    
    # --- stream node budgets section --
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 0)

    nbud = int(stream_lines[line_index].split()[0])                # number of stream node budgets
    buds_line = line_index
 
    # check each hydrographs and remove the hydrographs outside the submodel boundary
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 1)
    new_buds = 0 
    for i in range(0, nbud):
        sn = int(stream_lines[line_index].split()[0])

        if sn not in sub_snodes:
            del stream_lines[line_index]
        else:
            new_buds += 1
            line_index += 1

    # update the number of hydrographs
    stream_lines[buds_line] = '     ' + str(new_buds) + '        / NBUDR'
    
    # -- streambed parameters
    line_index = iwfm.skip_ahead(line_index + 1, stream_lines, 3)

    count = 0 
    while len(stream_lines) > line_index and len(stream_lines[line_index]) > 0 and stream_lines[line_index][0] not in comments:
        sn = int(stream_lines[line_index].split()[0])

        if sn not in sub_snodes:
            del stream_lines[line_index]
        else:
            count += 1
            line_index += 1

    # -- inflow file --
    if have_inflow:
        iwfm.sub_st_inflow_file(inflow_file, sim_dict_new['stin_file'], sub_snodes, verbose=verbose)

    # -- diversion specification file file --
    # ** too abstract - needs to be done manually

    # -- bypass specification file --
    if bp_file:
        have_bp = iwfm.sub_st_bp_file(bp_file, sim_dict_new['bp_file'], elem_list, sub_snodes, verbose=verbose)
        if have_bp == 0:
          stream_lines[bp_line] = '                                         / BYPSPECFL'

    # -- don't modify diversion time series file file --

    with open(sim_dict_new['stream_file'], 'w') as outfile:
        outfile.write('\n'.join(stream_lines))
    if verbose:
        print(f'  Wrote stream main file {sim_dict_new["stream_file"]}')

    return

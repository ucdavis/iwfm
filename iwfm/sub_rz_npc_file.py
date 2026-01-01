# sub_rz_npc_file.py
# Copy the rootzone non-ponded crops main file and replace the contents 
# with those of the new submodel, write out the new file, and 
# process the other non-ponded crop files
# Copyright (C) 2020-2026 University of California
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


def sub_rz_npc_file(old_filename, sim_dict_new, elems, verbose=False):
    '''sub_rz_npc_file() - Copy the rootzone non-ponded crops main file 
       and replace the contents with those of the new submodel, write out 
       the new file, and process the other non-ponded crop files

    Parameters
    ----------
    old_filename : str
        name of existing model non-ponded crops main file

    sim_dict_new : str
        new subnmodel file names

    elems : list of ints
        list of existing model elements in submodel

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    comments = ['C','c','*','#']

    with open(old_filename) as f:
        npc_lines = f.read().splitlines()
    npc_lines.append('')

    line_index = iwfm.skip_ahead(0, npc_lines, 0)                # skip initial comments
    ncrop = int(npc_lines[line_index].split()[0])                # number of crop types

    # non-ponded crop area file name
    line_index = iwfm.skip_ahead(line_index, npc_lines, 2 + ncrop)       # skip factors
    nparea_file = npc_lines[line_index].split()[0]               # original crop area file name
    nparea_file = nparea_file.replace('\\', ' ').split()[1]      # remove directory name
    npc_lines[line_index] = '   ' + sim_dict_new['npa_file'] + '.dat		        / LUFLNP'

    # budget section
    line_index = iwfm.skip_ahead(line_index, npc_lines, 1)       # skip comments
    nbud = int(npc_lines[line_index].split()[0])                 # number of crop budgets
    line_index = iwfm.skip_ahead(line_index, npc_lines, 3 + nbud) # skip budget section

    line_index = iwfm.skip_ahead(line_index, npc_lines, 2)       # skip file name and factor
    line_index = iwfm.skip_ahead(line_index, npc_lines, ncrop)   # skip crop root depths

    # get orig_elems value
    orig_elems, l = 0, line_index
    while npc_lines[l][0] not in comments:
        orig_elems += 1
        l += 1

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems)    # curve numbers

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems)    # crop ETc

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems)    # ag water supply requirement

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems)    # irrigation periods

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems, skip=1)    # minimum soil moisture

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems, skip=1)    # target soil moisture

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems)    # return flow fractions

    line_index = iwfm.sub_remove_items(npc_lines, line_index, elems)    # reuse fractions

    # initial conditions - process manually because end of file
    line_index = iwfm.skip_ahead(line_index, npc_lines, 1)       # skip file name and comments
    if int(npc_lines[line_index].split()[0]) > 0:
        for i in range(0, orig_elems):
            if int(npc_lines[line_index].split()[0]) not in elems:
                del npc_lines[line_index]
            else:
                line_index += 1

    npc_lines.append('')

    with open(sim_dict_new['np_file'], 'w') as outfile:
        outfile.write('\n'.join(npc_lines))
    if verbose:
        print(f'      Wrote non-ponded crop file {sim_dict_new["np_file"]}')


    # -- non-ponded crop area file --
    iwfm.sub_lu_file(nparea_file, sim_dict_new['npa_file'], elems, verbose=verbose)


    return


# sub_rz_pc_file.py
# Copy the rootzone ponded crops main file and replace the contents 
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


def sub_rz_pc_file(old_filename, sim_dict_new, elems, verbose=False):
    '''sub_rz_pc_file() - Copy the rootzone ponded crops main file 
       and replace the contents with those of the new submodel, write out 
       the new file, and process the other ponded crop files

    Parameters
    ----------
    old_filename : str
        name of existing model ponded crop main file

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
    ncrop = 5

    with open(old_filename) as f:
        pc_lines = f.read().splitlines()
    pc_lines.append('')

    line_index = iwfm.skip_ahead(0, pc_lines, 0)                # skip initial comments

    # non-ponded crop area file name
    parea_file = pc_lines[line_index].split()[0]               # original crop area file name
    parea_file = parea_file.replace('\\', ' ').split()[1]      # remove directory name
    pc_lines[line_index] = '   ' + sim_dict_new['npa_file'] + '.dat		        / LUFLP'

    # budget section
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)       # skip comments
    nbud = int(pc_lines[line_index].split()[0])                     # number of crop budgets
    line_index = iwfm.skip_ahead(line_index, pc_lines, 3 + nbud)    # skip budget section

    line_index = iwfm.skip_ahead(line_index, pc_lines, 1)           # skip factor
    line_index = iwfm.skip_ahead(line_index, pc_lines, ncrop)       # skip crop root depths

    # get orig_elems value
    orig_elems, l = 0, line_index
    while pc_lines[l][0] not in comments:
        orig_elems += 1
        l += 1

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # curve numbers

    line_index = iwfm.skip_ahead(line_index, pc_lines, 0)              # skip comments

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # crop ETc

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # water supply requirement

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # irrigation periods

    line_index = iwfm.skip_ahead(line_index, pc_lines, 2)              # skip comments and file names

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # ponding depths

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # application depths

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # return flow depths

    line_index = iwfm.sub_remove_items(pc_lines, line_index, elems)    # re-use flow depths

    # initial conditions - process manually because end of file
    line_index = iwfm.skip_ahead(line_index, pc_lines, 0)       # skip file name and comments
    if int(pc_lines[line_index].split()[0]) > 0:
        for i in range(0, orig_elems):
            if int(pc_lines[line_index].split()[0]) not in elems:
                del pc_lines[line_index]
            else:
                line_index += 1

    pc_lines.append('')

    with open(sim_dict_new['pc_file'], 'w') as outfile:
        outfile.write('\n'.join(pc_lines))
    if verbose:
        print(f'      Wrote ponded crop file {sim_dict_new["pc_file"]}')

    # -- ponded crop area file --
    iwfm.sub_lu_file(parea_file, sim_dict_new['pca_file'], elems, verbose=verbose)

    return




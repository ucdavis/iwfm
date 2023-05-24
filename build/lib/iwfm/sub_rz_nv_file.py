# sub_rz_nv_file.py
# Copy the rootzone native and riparian main file and replace the contents 
# with those of the new submodel, write out the new file, and 
# process the other non-ponded crop files
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


def sub_rz_nv_file(old_filename, sim_dict_new, elems, verbose=False):
    '''sub_rz_nv_file() - Copy the rootzone native and riparian main file 
       and replace the contents with those of the new submodel, write out 
       the new file, and process the other non-ponded crop files

    Parameters
    ----------
    old_filename : str
        name of existing model native and riparian main file

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

    nv_lines = open(old_filename).read().splitlines()  
    nv_lines.append('')

    line_index = iwfm.skip_ahead(0, nv_lines, 0)                # skip initial comments

    # native and riparian vegetation area file name
    nvarea_file = nv_lines[line_index].split()[0]               # original crop area file name
    nvarea_file = nvarea_file.replace('\\', ' ').split()[1]      # remove directory name
    nv_lines[line_index] = '   ' + sim_dict_new['nva_file'] + '.dat		        / LUFLNVRV'

    line_index = iwfm.skip_ahead(line_index, nv_lines, 4)       # skip comments and three factors

    # get orig_elems value
    orig_elems, l = 0, line_index
    while nv_lines[l][0] not in comments:
        orig_elems += 1
        l += 1

    line_index = iwfm.sub_remove_items(nv_lines, line_index, elems)    # parameters

    # initial conditions - process manually because end of file
    line_index = iwfm.skip_ahead(line_index, nv_lines, 0)       # skip file name and comments
    if int(nv_lines[line_index].split()[0]) > 0:
        for i in range(0, orig_elems):
            if int(nv_lines[line_index].split()[0]) not in elems:
                del nv_lines[line_index]
            else:
                line_index += 1

    nv_lines.append('')

    with open(sim_dict_new['nv_file'], 'w') as outfile:
        outfile.write('\n'.join(nv_lines))
    if verbose:
        print(f'      Wrote native and riparian file {sim_dict_new["nv_file"]}')


    # -- native and riparian area file --
    iwfm.sub_lu_file(nvarea_file, sim_dict_new['nva_file'], elems, verbose=verbose)


    return


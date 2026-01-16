# sub_gw_bc_cghd_file.py
# Copies the old groundwater constrained general head boundary condition file,
# replaces the contents with those of the new submodel, and writes out the new file
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


def sub_gw_bc_cghd_file(old_filename, new_filename, nodes, verbose=False):
    '''sub_gw_bc_cghd_file() - Read the original groundwater constrained general head 
        boundary conditions file, determine which boundary conditions are in the submodel, 
        and write out a new file

    Parameters
    ----------
    old_filename : str
        name of existing model constrained general head boundary condition file

     new_filename : str
        name of new subnmodel constrained general head boundary condition file

    nodes : list of ints
        list of existing model nodes in submodel

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    new_ngb : int
        number of boundary conditions in new file

    '''
    import iwfm as iwfm

    comments = ['C','c','*','#']

    # Check if constrained head BC file exists using iwfm utility
    iwfm.file_test(old_filename)

    with open(old_filename) as f:
        cg_lines = f.read().splitlines()
    cg_lines.append('')

    line_index = iwfm.skip_ahead(0, cg_lines, 0)                # skip initial comments

    ngb = int(cg_lines[line_index].split()[0])  
    ngb_line = line_index

    line_index = iwfm.skip_ahead(0, cg_lines, 6)                # skip initial comments

    # remove lines for nodes that are not in the submodel
    new_ngb = 0
    for l in range(0,ngb):
        if (int(cg_lines[line_index].split()[0]) not in nodes):
            del cg_lines[line_index]
        else:
            line_index += 1
            new_ngb += 1

    cg_lines[ngb_line] = '     '+ str(new_ngb) +'                         / NGB'

    with open(new_filename, 'w') as outfile:
        outfile.write('\n'.join(cg_lines))
        if verbose:
            print(f'      Wrote constrained general head BC file {new_filename}')

    return new_ngb

# sub_gw_pump_epump_file.py
# Copies the old element pumping file and replaces the contents with those 
# of the new submodel, and writes out the new file
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


def sub_gw_pump_epump_file(old_filename, new_filename, elems, verbose=False):
    '''sub_gw_pump_epump_file() -  Copies the old element pumping file and replaces 
       the contents with those of the new submodel, and writes out the new file

    Parameters
    ----------
    old_filename : str
        name of existing model element ppumping file

    new_filename : str
        name of new subnmodel element pumpgin file

    elems : list of ints
        list of existing model elements in submodel

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    bool : new_nsink > 0
        True if there are any wells

    '''
    import iwfm as iwfm

    comments = ['C','c','*','#']

    with open(old_filename) as f:
        epump_lines = f.read().splitlines()
    epump_lines.append('')

    line_index = iwfm.skip_ahead(0, epump_lines, 0)           # skip factors and comments

    nsink = int(epump_lines[line_index].split()[0])           # number of element pumping specs
 
    new_nsink, nsink_line = 0, line_index

    line_index = iwfm.skip_ahead(line_index, epump_lines, 1)  # skip factors and comments

    for l in range(0, nsink):
        #print(f' ==> l: {l},  epump_lines[{line_index}]: {epump_lines[line_index]}')
        if int(epump_lines[line_index].split()[0]) not in elems:
            del epump_lines[line_index]
        else:
            line_index += 1
            new_nsink += 1

    epump_lines[nsink_line] = '     ' + str(new_nsink) + '                       / NSINK'

    # element groups
    line_index = iwfm.skip_ahead(line_index, epump_lines, 0)  # skip comments
    ngrp = int(epump_lines[line_index].split()[0])           # number of element groups
    new_ngrp, ngrp_line = 0, line_index

    line_index = iwfm.skip_ahead(line_index, epump_lines, 1)  # skip comments

    # cycle through element groups, eliminating those outside the submodel area
    # and reducing those partially inside the submodel area
    for id in range(0, ngrp):
        grp_id, nelem, ielem, *z = [int(e) for e in epump_lines[line_index].split()]
        grp_line, ielems = line_index, []
        ielems.append(ielem)
        line_index += 1
        for j in range(1, nelem):
            if ielem == 0: # get next ielem
                ielem = int(epump_lines[line_index].split()[0])
            # else on first line of this group
            if ielem in elems:  # keep the item
                ielems.append(ielem)
            ielem = 0
            line_index += 1
        # after reading all ielem in group
        if len(ielems) > 0: 
            new_ngrp += 1
            epump_lines[grp_line] = str(id+1) + '\t' + str(len(ielems)) + '\t' + str(ielems[0])
            if len(ielems) > 1:
                for j in range(1,len(ielems)):
                    epump_lines[grp_line + j] = '\t\t' + str(ielems[j])
            if len(ielems) < nelem:
                for j in range(len(ielems), nelem):       
                    del epump_lines[grp_line + len(ielems) + j]
        epump_lines[ngrp_line] = '\t' + str(new_ngrp)

    epump_lines.append('')

    with open(new_filename, 'w') as outfile:
        outfile.write('\n'.join(epump_lines))
        if verbose:
            print(f'      Wrote element pumping file {new_filename}')

    return new_nsink > 0

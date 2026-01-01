# sub_gw_pump_well_file.py
# Copies the old well pumping file and replaces the contents with those 
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


def sub_gw_pump_well_file(old_filename, new_filename, elems, bounding_poly, verbose=False):
    '''sub_gw_pump_well_file() - Copies the old well pumping file and replaces the 
       contents with those of the new submodel, and writes out the new file

    Parameters
    ----------
    old_filename : str
        name of existing model element ppumping file

    new_filename : str
        name of new subnmodel element pumpgin file

    elems : list of ints
        list of existing model elements in submodel

    bounding_poly : shapely Polygon
        submodel area

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    new_nwells > 0 : bool
        True if any wells in submodel, False otherwise

    '''
    import iwfm as iwfm
    from shapely.geometry import Point

    comments = ['C','c','*','#']

    with open(old_filename) as f:
        well_lines = f.read().splitlines()
    well_lines.append('')

    line_index = iwfm.skip_ahead(0, well_lines, 0)           # skip factors and comments

    nwells = int(well_lines[line_index].split()[0])          # number of well pumping specs
    new_nwells, nwells_line = 0, line_index

    line_index = iwfm.skip_ahead(line_index, well_lines, 4)  # skip factors and comments

    keep_wells = []
    for l in range(0, nwells):
        t = well_lines[line_index].split()
        id = int(t[0])
        point = Point(float(t[1]), float(t[2]))
        if not point.within(bounding_poly):
            del well_lines[line_index]
        else:
            keep_wells.append(id)
            line_index += 1

    well_lines[nwells_line] = '         ' + str(new_nwells) + '                       / NWELL'
    line_index = iwfm.skip_ahead(line_index, well_lines, 0)  # skip factors and comments

    for l in range(0, nwells):
        t = well_lines[line_index].split()
        if t[0] not in keep_wells:
            del well_lines[line_index]
        else:
            line_index += 1

    # -- delivery element groups
    line_index = iwfm.skip_ahead(line_index, well_lines, 0)  # skip comments

    ngrp = int(well_lines[line_index].split()[0])           # number of element groups
    new_ngrp, ngrp_line = 0, line_index

    # cycle through element groups, eliminating those outside the submodel area
    # and reducing those partially inside the submodel area
    line_index = iwfm.skip_ahead(line_index, well_lines, 1)  # skip comments
    for id in range(0, ngrp):
        grp_line, ielems = line_index, []
        grp_id, nelem, ielem, *z = [int(e) for e in well_lines[line_index].split()]
        if ielem in elems:  # keep the item
            ielems.append(ielem)
        line_index += 1
        for j in range(1, nelem):
            ielem = int(well_lines[line_index].split()[0])
            if ielem in elems:  # keep the item
                ielems.append(ielem)
            line_index += 1
        # after reading all ielem in group
        if len(ielems) == 0:   # delete the lines for this element group
            for j in range(grp_line, line_index):
                del well_lines[grp_line]
            line_index = grp_line
        elif len(ielems) > 0: 
            new_ngrp += 1
            well_lines[ngrp_line] = '\t' + str(new_ngrp)
            well_lines[grp_line] = str(id+1) + '\t' + str(len(ielems)) + '\t' + str(ielems[0])
            if len(ielems) > 1:
                for j in range(1,len(ielems)):
                    well_lines[grp_line + j] = '\t\t' + str(ielems[j])
            if len(ielems) < nelem:
                for j in range(len(ielems), nelem):       
                    del well_lines[grp_line + len(ielems) + j]

    well_lines[ngrp_line] = '         ' + str(new_ngrp) + '                       / NGRP'
    well_lines.append('')

    # -- write out the submodel wwell specification file
    with open(new_filename, 'w') as outfile:
        outfile.write('\n'.join(well_lines))
        if verbose:
            print(f'      Wrote well specification file {new_filename}')

    return new_nwells > 0


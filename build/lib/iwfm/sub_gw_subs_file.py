# sub_gw_subs_file.py
# Copies the groundwater subsidence file and replace the contents with those of the new
# submodel, and writes out the new file
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


def sub_gw_subs_file(old_filename, new_filename, node_list, bounding_poly, verbose=False):
    '''sub_gw_subs_file() - Read the original groundwater subsidence file, determine 
        which nodes are in the submodel, and write out a new file

    Parameters
    ----------
    old_filename : str
        name of existing model element ppumping file

    new_filename : str
        name of new subnmodel element pumpgin file

    node_list : list of ints
        list of existing model nodes in submodel

    bounding_poly : shapely Polygon
        submodel area

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm
    from shapely.geometry import Point

    comments = ['C','c','*','#']
    nodes = []
    for n in node_list:
        nodes.append(n)

    subs_lines = open(old_filename).read().splitlines()  
    subs_lines.append('')

    line_index = iwfm.skip_ahead(0, subs_lines, 0)                # skip initial comments

    line_index = iwfm.skip_ahead(line_index, subs_lines, 5)       # skip file names and factors

    # -- hydrographs
    nouts = int(subs_lines[line_index].split()[0])                # number of hydrographs

    new_nouts, nouts_line = 0, line_index
    line_index = iwfm.skip_ahead(line_index, subs_lines, 3)       # skip factors

    # remove hydrographs that are not in the submodel
    keep_hyd = []
    for l in range(0, nouts):
        t = subs_lines[line_index].split()
        id = int(t[0])
        point = Point(float(t[3]), float(t[4]))
        if not point.within(bounding_poly):
            del subs_lines[line_index]
        else:
            new_nouts += 1
            keep_hyd.append(id)
            line_index += 1
        line_index = iwfm.skip_ahead(line_index, subs_lines, 0)       # skip comments to next section

    subs_lines[nouts_line] = '         ' + str(new_nouts) + '                       / NOUTS'

    # -- subsidence parameters
    # -- parametric grid for subsidence parameters --
    pgroups = int(subs_lines[line_index].split()[0])              # parametric grid?
    # skip factors
    line_index = iwfm.skip_ahead(line_index + 1, subs_lines, 1)

    # --  TODO:  if pgroups > 0,  skip parametric grid(s)

    # -- parameters for each model node -- 
    # first, determine the number of layers - 1st line has 6 items, others have 5 items
    layers, line = 1, line_index + 1
    while len(subs_lines[line].split()) < 6:
        layers += 1
        line += 1

    # count the number of nodes in the original model file
    line, node_count = line_index, 0 # starting point
    while len(subs_lines[line]) > 0:
        line += 1
        node_count += 1
    node_count = int(node_count / layers)

    # remove parameters for nodes that are not in the submodel
    for l in range(1,node_count + 1):
        t = subs_lines[line_index].split()
        if (int(t[0]) not in nodes):
            for i in range(0,layers):  # remove <layers> lines
                del subs_lines[line_index]
        else:
            line_index += layers

    subs_lines.append('')

    with open(new_filename, 'w') as outfile:
        outfile.write('\n'.join(subs_lines))
    if verbose:
        print(f'      Wrote subsidence file {new_filename}')

    return

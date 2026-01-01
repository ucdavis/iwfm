# sub_gw_pump_file.py
# Copies the old groundwater pumping main file and replaces the contents 
# with those of the new submodel, and writes out the new file
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


def sub_gw_pump_file(old_filename, sim_dict_new, elems, bounding_poly, verbose=False):
    '''sub_gw_bc_file() - Read the original groundwater main pumping file, 
        determine which boundary conditions are in the submodel, and write out a new 
        file

    Parameters
    ----------
    old_filename : str
        name of existing groundwater pumping main file

     sim_dict_new : str
        new subnmodel file names

    nodes : list of ints
        list of existing model nodes in submodel

    elems : list of ints
        list of existing model elements in submodel

    bounding_poly : shapely.geometry Polygon
        submodel boundary form model nodes

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    comments = ['C','c','*','#']

    with open(old_filename) as f:
        pump_lines = f.read().splitlines()
    pump_lines.append('')

    line_index = iwfm.skip_ahead(1, pump_lines, 0)                # skip initial comments

    # -- file names --

    # well specification file
    well_file = pump_lines[line_index].split()[0]  # well specifications file
    have_well = True
    if well_file[0] == '/':
        have_well = False
    else:
        well_file = well_file.replace('\\', ' ').split()[1]     
        pump_lines[line_index] = '   ' + sim_dict_new['well_file'] + '.dat		        / WELLFL'
    well_index = line_index # in case no wells in submodel, return and set blank file name
    line_index = iwfm.skip_ahead(line_index, pump_lines, 1)                

    # element pumping file
    epump_file = pump_lines[line_index].split()[0]  # specified head conditions file
    have_epump = True
    if epump_file[0] == '/':
        have_epump = False
    else:
        epump_file = epump_file.replace('\\', ' ').split()[1]     
        pump_lines[line_index] = '   ' + sim_dict_new['epump_file'] + '.dat		        / ELEMPUMPFL'
    epump_index = line_index # in case no element pumping in submodel, return and set blank file name
    line_index = iwfm.skip_ahead(line_index, pump_lines, 1)                

    # pumping rates file
    prate_file = pump_lines[line_index].split()[0]  # general head boundary conditions file
    have_rates = True
    if prate_file[0] == '/':
        have_rates = False
    else:
        prate_file = prate_file.replace('\\', ' ').split()[1]     
        pump_lines[line_index] = '   ' + sim_dict_new['prate_file'] + '.dat		        / PUMPFL'


    # -- modify other pumping files for submodel
    if have_well:                                   # process well specification file
        have_well = iwfm.sub_gw_pump_well_file(well_file, sim_dict_new['well_file'], elems, bounding_poly, verbose)
    if have_well == False:
        pump_lines[well_index] = '                                          / WELLFL'


    if have_epump:                                  # process element pumping file
        have_epump = iwfm.sub_gw_pump_epump_file(epump_file, sim_dict_new['epump_file'], elems, verbose)
    if have_epump == False:
        pump_lines[epump_index] = '                                         / ELEMPUMPFL'

    # -- write out the modified pumping file
    with open(sim_dict_new['pump_file'], 'w') as outfile:
        outfile.write('\n'.join(pump_lines))
        if verbose:
            print(f'      Wrote pumping main file {sim_dict_new["pump_file"]}')


    return

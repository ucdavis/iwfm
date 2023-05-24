# sub_sim_file.py
# Copies the old simulation input file, replaces the file names with
# those of the new submodel, and writes out the new file
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


def sub_sim_file(in_sim_file, sim_dict_new, has_lake=False):
    ''' sub_sim_file() - Copy the old simulation input file,
        replacing the file names with those of the new model,
        and write out the new file

    Parameters
    ----------
    in_sim_file : str
        name of existing simprocessor main input file
    
    sim_dict_new : dict
        dictionary of submodel simulation file names
    
    has_lake : bool, default=False
        does the submodel have a lake file?

    Returns:
    nothing

    '''
    import iwfm as iwfm

    # -- read the simprocessor file into array sim_lines
    sim_lines = open(in_sim_file).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, sim_lines, 3)  # skip comments and three header lines

    # -- preprocessor output file
    sim_lines[line_index] = iwfm.pad_both(sim_dict_new['preout'], f=4, b=53) + ' '.join(
        sim_lines[line_index].split()[1:]
    )

    # -- groundwater file
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_lines[line_index] = iwfm.pad_both(
        sim_dict_new['gw_file'], f=4, b=53
    ) + ' '.join(sim_lines[line_index].split()[1:])

    # -- stream file
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_lines[line_index] = iwfm.pad_both(
        sim_dict_new['stream_file'], f=4, b=53
    ) + ' '.join(sim_lines[line_index].split()[1:])

    # -- lake file
    if has_lake:
        line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
        sim_lines[line_index] = iwfm.pad_both(
            sim_dict_new['lake_file'], f=4, b=53
        ) + ' '.join(sim_lines[line_index].split()[1:])
    else:
        line_index += 1

    # -- rootzone file
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_lines[line_index] = iwfm.pad_both(
        sim_dict_new['root_file'], f=4, b=53
    ) + ' '.join(sim_lines[line_index].split()[1:])

    # -- small watersheds file
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_lines[line_index] = iwfm.pad_both(
        sim_dict_new['swshed_file'], f=4, b=53
    ) + ' '.join(sim_lines[line_index].split()[1:])

    # -- unsaturated file
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0) 
    sim_lines[line_index] = iwfm.pad_both(
        sim_dict_new['unsat_file'], f=4, b=53
    ) + ' '.join(sim_lines[line_index].split()[1:])

    sim_lines.append('')

    # -- write new simulation input file
    with open(sim_dict_new['sim_name'], 'w') as outfile:
        outfile.write('\n'.join(sim_lines))

    return

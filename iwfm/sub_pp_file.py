# sub_pp_file.py
# Copies the old preprocessor input file, replaces the file names with
# those of the new submodel, and writes out the new file
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


def sub_pp_file(in_pp_file, pre_dict, pre_dict_new, has_lake=False):
    ''' sub_pp_file() - Copy the old preprocessor input file,
        replacing the file names with those of the new model,
        and write out the new file

    Parameters
    ----------
    in_pp_file : str
        name of existing preprocessor main input file
    
    pre_dict : dict
        dictionary of existing model preprocessor file names
    
    pre_dict_new : dict
        dictionary of submodel preprocessor file names
    
    has_lake : bool, default=False
        does the submodel have a lake file?

    Returns:
    nothing

    '''
    import iwfm as iwfm

    # -- read the preprocessor file into array pre_lines
    with open(in_pp_file) as f:
        pre_lines = f.read().splitlines()  # open and read input file

    # -- preproc output file
    line_index = iwfm.skip_ahead(0, pre_lines, 3)  # skip comments
    pre_lines[line_index] = iwfm.pad_both(pre_dict_new['preout'], f=4, b=53) + ' '.join(
        pre_lines[line_index].split()[1:]
    )

    # -- element file
    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0) 
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['elem_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    # -- node file
    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0) 
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['node_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    # -- stratigraphy file
    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0) 
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['strat_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    # -- stream file
    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0) 
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['stream_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    # -- lake file
    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0) 
    if len(pre_dict['lake_file']) > 1 and has_lake:
        pre_lines[line_index] = iwfm.pad_both(
            pre_dict_new['lake_file'], f=4, b=53
        ) + ' '.join(pre_lines[line_index].split()[1:])
    else:
        pre_lines[line_index] = (
            iwfm.pad_both(' ', f=4, b=53)
            + '/ '
            + ' '.join(pre_lines[line_index].split()[1:])
        )

    pre_lines.append('')
    # -- write new preprocessor input file
    with open(pre_dict_new['prename'], 'w') as outfile:
        outfile.write('\n'.join(pre_lines))

    return

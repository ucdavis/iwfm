# iwfm_read_preproc.py
# read IWFM preprocessor main file and return dictionary of file names
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


def iwfm_read_preproc(pre_file):
    ''' iwfm_read_preproc() - Read an IWFM Preprocessor main input file,
        and return a dictionary with file names and some settings

    Parameters
    ----------
    pre_file : str
        name of existing preprocessor main input file

    Returns
    -------
    pre_dict : dictionary
        dictionary of preprocessor file names (resolved to absolute paths)

    have_lake : bool
        True = the existing model has a lake file

    '''
    import iwfm
    from pathlib import Path
    from iwfm.file_utils import read_next_line_value

    # Use iwfm utility for file validation
    iwfm.file_test(pre_file)
    with open(pre_file) as f:
        pre_lines = f.read().splitlines()  # open and read input file

    # Get base path for resolving relative file paths
    pre_base_path = Path(pre_file).resolve().parent

    pre_dict = {}

    preout, line_index = read_next_line_value(pre_lines, -1, skip_lines=3)  # preproc output file
    pre_dict['preout'] = str(pre_base_path / preout.replace('\\', '/'))

    elem_file, line_index = read_next_line_value(pre_lines, line_index)     # element file
    pre_dict['elem_file'] = str(pre_base_path / elem_file.replace('\\', '/'))

    node_file, line_index = read_next_line_value(pre_lines, line_index)     # node file
    pre_dict['node_file'] = str(pre_base_path / node_file.replace('\\', '/'))

    strat_file, line_index = read_next_line_value(pre_lines, line_index)    # stratigraphy file
    pre_dict['strat_file'] = str(pre_base_path / strat_file.replace('\\', '/'))

    stream_file, line_index = read_next_line_value(pre_lines, line_index)   # stream file
    pre_dict['stream_file'] = str(pre_base_path / stream_file.replace('\\', '/'))

    lake_file, line_index = read_next_line_value(pre_lines, line_index)     # lake file
    # -- is there a lake file?
    have_lake = True
    if lake_file[0] == '/':
        lake_file = ''
        have_lake = False
    else:
        lake_file = str(pre_base_path / lake_file.replace('\\', '/'))
    pre_dict['lake_file'] = lake_file

    return pre_dict, have_lake

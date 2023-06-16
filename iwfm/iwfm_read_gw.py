# iwfm_read_gw.py
# read IWFM simulation groundwater file for file names
# Copyright (C) 2020-2023 University of California
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

def get_name(s):
    import iwfm as iwfm
    temp = s.split()[0]
    if temp[0] == '/':   # check for presence of file name
        name = 'none'
    else:
        name = temp
    return name


def iwfm_read_gw(gw_file):
    ''' iwfm_read_gw() - Read an IWFM Simulation Groundwater file and return
        a dictionary of sub-process file names

    Parameters
    ----------
    gw_file : str
        IWFM Simulation Groundwater file name

    Returns
    -------
    gw_files : dictionary
        Groundwater sub-process file names
        
    '''
    import iwfm as iwfm

    iwfm.file_test(gw_file)
    comments, gw_dict = 'Cc*#', {}

    file_lines = open(gw_file).read().splitlines()  

    line_index = iwfm.skip_ahead(1, file_lines, 0) 
    gw_dict['bc'] = get_name(file_lines[line_index]) 

    line_index += 1
    gw_dict['tiledrain'] = get_name(file_lines[line_index]) 

    line_index += 1
    gw_dict['pumping'] = get_name(file_lines[line_index]) 

    line_index += 1
    gw_dict['subsidence'] = get_name(file_lines[line_index]) 

    line_index = iwfm.skip_ahead(10, file_lines, 0) 
    gw_dict['headall'] = get_name(file_lines[line_index]) 

    line_index = iwfm.skip_ahead(9, file_lines, 0) 
    gw_dict['gwhyd'] = get_name(file_lines[line_index]) 

    return gw_dict

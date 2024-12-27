# iwfm_read_div_areas.py
# Read diversion areas from an IWFM Diversion Specification File
# Copyright (C) 2020-2024 University of California
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


def iwfm_read_div_areas(divspec_file_name):
    ''' iwfm_read_div_areas() - read diversion areas from IWFM divirsion specification file
    
    Parameters
    ----------
    divspec_file_name : str
        IWFM Diversion Specification file name
    
    Return
    ------
    div_ids : list
        IWFM diversion numbers

    div_areas : list of lists
        List of elements in each IWFM diversion area
    
    '''
    import iwfm as iwfm

    # read diversion specification file
    with open(divspec_file_name, 'r') as f:
        div_file_lines = f.readlines()
    line_index = iwfm.skip_ahead(0, div_file_lines, skip=0)

    ndivs = int(div_file_lines[line_index].split()[0])

    # skip ndiv lines and comment ines to get to the first delivery area
    line_index = iwfm.skip_ahead(line_index+1, div_file_lines, skip=ndivs)
    n_delivs = int(div_file_lines[line_index].split()[0])

    deliv_area_ids, deliv_areas = [], []
    # read the element groups for each delivery
    for i in range(n_delivs):
        # the first line of a group has 3 items: deliv_area_id, number of elements, and first element number
        line_index = iwfm.skip_ahead(line_index+1, div_file_lines, skip=0)
        deliv_area_id = int(div_file_lines[line_index].split()[0])
        deliv_area_ids.append(deliv_area_id)
        n_elems = int(div_file_lines[line_index].split()[1])

        elems = []
        elems.append(int(div_file_lines[line_index].split()[2]))
        # read each element in the rest of the diversion area
        for j in range(n_elems-1):
            line_index = iwfm.skip_ahead(line_index+1, div_file_lines, skip=0)
            elem = int(div_file_lines[line_index].split()[0])
            elems.append(elem)

        deliv_areas.append(elems)

    div_ids, rchg_areas = [], []
    # read the element groups for each diversion recharge aree
    for i in range(n_delivs):
        # the first line of a group has 4 items: diversion id, number of elements, element number and factor
        line_index = iwfm.skip_ahead(line_index+1, div_file_lines, skip=0)
        div_id = int(div_file_lines[line_index].split()[0])
        div_ids.append(div_id)
        n_elems = int(div_file_lines[line_index].split()[1])

        elems = []
        elems.append(int(div_file_lines[line_index].split()[2]))
        # read each element in the rest of the diversion area
        for j in range(n_elems-1):
            line_index = iwfm.skip_ahead(line_index+1, div_file_lines, skip=0)
            elem = int(div_file_lines[line_index].split()[0])
            elems.append(elem)

        rchg_areas.append(elems)

    return deliv_area_ids, deliv_areas, div_ids, rchg_areas


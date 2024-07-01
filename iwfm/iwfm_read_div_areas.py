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
        divs = f.readlines()
    line_index = iwfm.skip_ahead(0, divs, skip=0)
    ndivs = int(divs[line_index].split()[0])

    # skip ndiv lines to get to the first diversion area
    line_index = iwfm.skip_ahead(line_index+1, divs, skip=ndivs)
    ngroup = int(divs[line_index].split()[0])

    div_ids, div_areas = [], []
    # read the element groups for each diversion and add a field to the shapefile
    for i in range(ngroup):
        # the first line of a group has 3 items: group number, number of elements, and diversion number
        line_index = iwfm.skip_ahead(line_index+1, divs, skip=0)
        div = int(divs[line_index].split()[0])
        div_ids.append(div)
        n_elems = int(divs[line_index].split()[1])

        elems = []
        elems.append(int(divs[line_index].split()[2]))
        # read each element in the rest of the diversion area
        for j in range(n_elems-1):
            line_index = iwfm.skip_ahead(line_index+1, divs, skip=0)
            elem = int(divs[line_index].split()[0])
            elems.append(elem)

        div_areas.append(elems)

    return div_ids, div_areas


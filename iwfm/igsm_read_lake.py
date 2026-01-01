# igsm_read_lake.py
# Read an IGSM pre-processor lakes file
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


def igsm_read_lake(lake_file):
    ''' igsm_read_lake() - Read an IGSM Lake file and returns (a) a list of
        elements and (b) a list of properties for each lake
        
    Parameters
    ----------
    lake_file : str
        name of IGSM lake file

    Returns
    -------
    lake_elems : list
        all lake elements
    
    lakes : list
        [lake_id, max_elev, next, nelem] for each lake

    '''
    import iwfm as iwfm

    with open(lake_file) as f:
        lake_lines = f.read().splitlines()  # open and read input file
    lake_index = 0  # start at the top
    lake_index = iwfm.skip_ahead(lake_index, lake_lines, 0)  # skip comments
    nlakes = int(lake_lines[lake_index].split()[0])
    lake_index = iwfm.skip_ahead(lake_index + 1, lake_lines, 0)  # skip comments
    lakes = []
    lake_elems = []
    l = lake_lines[lake_index].split()  # read first line of lake description
    for i in range(0, nlakes):
        lake_id = int(l.pop(0))
        max_elev = float(l.pop(0))
        next = int(l.pop(0))
        nelem = int(l.pop(0))
        lakes.append([lake_id, max_elev, next, nelem])
        j = 0
        while j < nelem:
            e = []
            e.append(lake_id)  # lake number
            e.append(int(l.pop(0)))  # element number
            e.append(float(l.pop(0)))  # area
            lake_elems.append(e)
            j += 1
            l = lake_lines[lake_index + i + j].split()  # get next line
        i += j
    return lake_elems, lakes

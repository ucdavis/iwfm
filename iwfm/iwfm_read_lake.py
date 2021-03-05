# iwfm_read_lake.py
# read IWFM preprocessor lakes file
# Copyright (C) 2020-2021 Hydrolytics LLC
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


def iwfm_read_lake(lake_file):
    """ iwfm_read_lake() - Read an IWFM Lake file and returns 
        (a) a list of elements and (b) a list of properties for each lake

    Parameters:
      lake_file      (str):   Name of IWFM Preprocessor Lake file

    Returns:
      lake_elems     (list):  Element numbers comprising each lake
      lakes          (list):  Configuration info for each lake

    """
    import iwfm as iwfm

    iwfm.file_test(lake_file)
    lake_lines = open(lake_file).read().splitlines()  

    lake_index = iwfm.skip_ahead(0, lake_lines, 0)  
    nlakes = int(lake_lines[lake_index].split()[0])

    lakes, lake_elems = [], []
    for i in range(0, nlakes):
        lake_index = iwfm.skip_ahead(lake_index + 1, lake_lines, 0)  
        l = lake_lines[lake_index].split() 
        lake_id = int(l.pop(0))
        max_elev = float(l.pop(0))
        dest = int(l.pop(0))
        nelem = int(l.pop(0))
        lakes.append([lake_id, max_elev, dest, nelem])
        for j in range(0, nelem):
            e = []
            if j > 0:  
                lake_index = iwfm.skip_ahead(lake_index + 1, lake_lines, 0)  
                l = lake_lines[lake_index].split()  
            e.append(lake_id)  
            e.append(int(l[0])) 
            lake_elems.append(e)
    return lake_elems, lakes

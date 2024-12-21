# map_divs2shp.py
# Read a shapefile of IWFM model elements and an IWFM diversion specification
# file and add a field to the shapefile for each diversion, setting element value
# to 1 if served by the diversion else 0
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


def map_divs2shp(div_ids, div_areas, elem_shp_name, out_shp_name, verbose=False):
    ''' map_divs2shp() - Add diversion areas to shapefile of IWFM model elements
    
    Parameters
    ----------
    div_ids : list
        IWFM diversion numbers

    div_areas : list of lists
        List of elements in each IWFM diversion area
    
    elem_shp_name : shapefile name
        IWFM Elements shapefile

    out_shp_name : shapefile name
        IWFM diversion areas shapefile name

    verbose : bool, default = False
        Print status messages    

    Return
    ------
    nothing
    
    '''
    import geopandas as gpd
    import os

    gdf = gpd.read_file(elem_shp_name)                                      # read elements shapefile into geopandas dataframe

    gdf.columns = gdf.columns.str.lower()                                   # convert column names to lower case

    elem_ids = gdf['elem_id'].tolist()                                      # copy geopandas dataframe field ELEM_ID to a list
    count = 0

    for div_id, div_area in zip(div_ids, div_areas):
        field_name = f'DelAr_{div_id}'                                        # add a field to the shapefile's dbf for the diversion area

        div_elems = [1 if elem in div_area else 0 for elem in elem_ids]     # create a list of 1's and 0's for the diversion area

        gdf[field_name] = div_elems                                         # add a field to the geopandas dataframe for the diversion area

        # to avoid fragmentation, make a deep copy every 50 fields
        count += 1
        if count >= 50:
            gdf = gdf.copy()
            count = 0

    # create a diversion specification shapefile name
    divspec_shp_base = os.path.basename(out_shp_name).split('.')[0]

    divspec_shp_name = divspec_shp_base+'.shp'

    # write the geopandas dataframe to a shapefile
    gdf.to_file(divspec_shp_name)

    if verbose: print(f'  Created diversion specification shapefile {divspec_shp_name}')

    return 


if __name__ == "__main__":
    ''' Run map_divs() from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        divspec_file_name  = sys.argv[1]
        elem_shp_name      = sys.argv[2]
        out_shp_name       = sys.argv[3]
    else:  # ask for file names from terminal
        divspec_file_name  = input('IWFM Diversion Specification file name: ')
        elem_shp_name      = input('IWFM Elements shapefile name: ')
        out_shp_name       = input('Output shapefile name: ')

    iwfm.file_test(divspec_file_name)
    iwfm.file_test(elem_shp_name)

    idb.exe_time()                                              # initialize timer

    div_ids, div_areas = iwfm.iwfm_read_div_areas(divspec_file_name)           # Read diversion specification file

    map_divs2shp(div_ids, div_areas, elem_shp_name, out_shp_name, verbose=True)   # Add diversion areas to shapefile of IWFM model elements

    idb.exe_time()                                          # print elapsed time

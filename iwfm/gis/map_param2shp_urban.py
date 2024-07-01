# map_param2shp_urban.py
# Read a shapefile of IWFM model elements and map IWFM Rootzone Urban parameters to the elements
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


def map_param2shp_urban(param_types, param_vals, elem_shp_name, out_shp_name='elem_parameters', verbose=False):
    ''' map_param2shp_urban() - Read a shapefile of IWFM model elements and map IWFM 
                    Rootzone Urban parameters to the elements
    
    Parameters
    ----------
    param_types : list
        names of parameters

    param_vals : list of lists
        lists of parameter values

    elem_shp_name : shapefile name
        IWFM Elements shapefile name

    out_shp_name : shapefile name, default = 'elem_parameters'
        IWFM output shapefile name

    verbose : bool, default = False
        Print status messages    

    Return
    ------
    nothing
    
    '''
    import geopandas as gpd
    import os

    param_types = [t.upper() for t in param_types]                      # convert parameter names to upper case

    ic = param_vals[1]

    param_vals = param_vals[0]

    gdf = gpd.read_file(elem_shp_name)                                  # read elements shapefile into geopandas dataframe

    out_shp_base = os.path.basename(out_shp_name).split('.')[0]         # create a parameter shapefile name

    gdf_new = gdf.copy()                                                # make a copy of the geopandas dataframe

    for j in range(len(param_types)):
        field_name = f'{param_types[j]}'                                # create the field name
    
        if verbose: 
            print(f'  Mapping parameter {param_types[j]} to elements')

        data = param_vals[:,j]                                          # compile data for the field

        gdf_new[field_name] = data                                      # add a field to the geopandas dataframe

    out_shp_name = out_shp_base+'.shp'

    gdf_new.to_file(out_shp_name)                                       # write the geopandas dataframe to a shapefile

    if verbose: print(f'  Created IWFM parameter shapefile {out_shp_name}')


    # write IC to a separate shapefile
    gdf_ic = gdf.copy()                                                 # make a copy of the geopandas dataframe

    gdf_ic['FSOILMP'] = ic[:,0]                                         # add a field to the geopandas dataframe

    gdf_ic['SOILM'] = ic[:,1]                                           # add a field to the geopandas dataframe

    out_shp_name = out_shp_base+'_IC.shp'

    gdf_ic.to_file(out_shp_name)                                        # write the geopandas dataframe to a shapefile

    if verbose: print(f'  Created IWFM parameter shapefile {out_shp_name}')

    return 


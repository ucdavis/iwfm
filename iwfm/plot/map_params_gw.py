# map_params_gw.py
# Create PNG images of groundwater parameters from an IWFM simulation
# Copyright (C) 2023-2024 University of California
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

def plot_one(param_name, plot_data, bounding_poly, layer, basename, units='', point_width=100, format='tiff', verbose=False ):
    ''' plot_one() - Draw and save one plot

    Parameters
    ----------
    param_name : string
        name of parameter
    
    plot_data : list
        numpy array containing x, y, and value

    bounding_poly : shapely Polygon
        Model boundary polygon

    layer : int
        layer number

    basename : string
        base name of image file

    units : string, default=''
        units of parameter

    point_width : int, default = 100
        The width of the polygon or diameter of the circle to be drawn around each data point.

    format : string, default = 'tiff'
        output file format: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp

    verbose : bool, default = False
        If True, print status messages.
    
    Returns
    -------
    nothing
    '''
    import iwfm.plot as iplot
    count = 0

    #  Produce point map
    image_name = f'{basename}_{param_name}{layer+1}_nodes.'+format               #  Set image file name
    iplot.map_to_nodes(plot_data, bounding_poly, image_name, title=f'{param_name} layer {layer+1}', 
                       label=f'{param_name}', units=units, format=format )
    count += 1

    # if all plot_data values are equal then they can't be contoured
    if len(set([i[2] for i in plot_data])) == 1:
        print(f'  Skipping {param_name} contour plots for layer {layer+1}, all values are the same')
    else:
        #  Produce contour lines map
        image_name = f'{basename}_{param_name}{layer+1}_contour.'+format       #  Set image file name
        iplot.map_to_nodes_contour(plot_data, bounding_poly, image_name, title=f'{param_name} layer {layer+1}', 
                               label=f'{param_name}', units=units, format=format )
        count += 1

        #  Produce filled contour map
        image_name = f'{basename}_{param_name}{layer+1}_contourf.'+format      #  Set image file name
        iplot.map_to_nodes_contour(plot_data, bounding_poly, image_name, title=f'{param_name} layer {layer+1}', 
                               label=f'{param_name}', units=units, format=format, contour='filled' )
        count += 1

    return count





def map_params_gw(param_type, param_values, node_coords, layers, bounding_poly, strat, format='tiff', basename='gw_param_map',
                   point_width=100, verbose=False):
    ''' map_params_gw() - Create PNG images of groundwater parameters from an IWFM simulation

    Parameters
    ----------
    param_type : string
        name of parameter

    param_values : numpy array
        groundwater parameter values

    node_coords: numpy array
        nodal coordinates

    layers: int
        number of model layers

    bounding_poly : numpy array
        Model boundary polygon for masking

    strat : list
        thicknesses of model layers
        strat[][2] == Aquiclude 1, strat[][3] == Layer 1, etc
    
    format : string, default = 'tiff'
        output file format: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp

    basename : string
        base name of image file, default = gw_param_map

    point_width : int, default = 100
        The width of the polygon or diameter of the circle to be drawn around each data point.


    Returns
    -------
    count : int
        number of parameter maps created
    '''
    import numpy as np

    count = 0
    for layer in range(layers):
        thickness = strat[:,layer*2 + 3]

        if param_type in ['Kh', 'Kv']:                                          # plot Kh or Kv for layer 
            units, do_it ='(ft/day)', 1
        elif param_type == 'Kq':                                                # plot Kq for layer
            if (np.max(strat,axis=0)[layer*2 + 2]) > 0:                         # if aquiclude thickness > 0
                units, do_it ='(ft/day)', 1
                thickness = strat[:,layer*2 + 2]                                # aquiclude thickness
            else:
                do_it = 0
                #print(f'  Skipping Kq, layer {layer+1}')
        elif param_type == 'Sy' and layer == 0:                                 # plot Sy for layer 1
            units, do_it ='', 1
        elif param_type == 'Ss' and layer >= 1:                                 # plot Ss for layers > 0
            units, do_it ='', 1
        else:
            do_it = 0
            #print(f'  Skipping {param_type}, layer {layer+1}')

        if do_it == 1:                                                          # compile plot data and produce plots
            plot_data = []
            for i in range(len(node_coords)):
                if thickness[i] > 0:
                    plot_data.append([node_coords[i][1], node_coords[i][2], param_values[i][layer]]) 
                else:
                    plot_data.append([node_coords[i][1], node_coords[i][2], 0 ]) 

            result = plot_one(param_type, plot_data, bounding_poly, layer, basename, units, point_width=point_width, format=format)

            if verbose and result > 0: print(f'  Mapped {param_type} for layer {layer+1} ')

            count += result

    return count


if __name__ == "__main__":
    import sys
    import numpy as np
    import iwfm as iwfm
    import iwfm.gis as igis
    import iwfm.debug as idb

    point_width_default = 100
    point_width = point_width_default

    verbose = True

    args = sys.argv

# TODO: Change to get Simulation file name, and get Groundwater.dat file name from Simulation file

    if len(args) > 1:  # arguments are listed on the command line
        gw_file   = args[1]         # groundwate.dat file
        pre_file  = args[2]         # preprocessor.in file
        basename  = args[3]         # output file base name
        format    = args[4].lower() # output file format: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp

        if(len(args) > 4): 
            point_width = int(args[5])  # point width
        if point_width < 1: 
            point_width = point_width_default  # default point width

    else:  # get everything form the command line
        gw_file   = input('IWFM Groundwater.dat file name: ')
        pre_file  = input('IWFM Preprocessor file name: ')
        basename  = input('Output file base name: ')
        format    = input('Output file format (pdf, png, tiff): ').lower()

    iwfm.file_test(gw_file)
    iwfm.file_test(pre_file)

    idb.exe_time()  # initialize timer

# TODO: Put path into pre_dict, sim_dict and add to Preprocessor and Simulation file names when calling read functions

    pre_dict, have_lake = iwfm.iwfm_read_preproc(pre_file)

    node_coords, node_list, factor = iwfm.iwfm_read_nodes(pre_dict['node_file'])

    elem_ids, elem_nodes, elem_sub = iwfm.iwfm_read_elements(pre_dict['elem_file'])

    strat, nlayers = iwfm.iwfm_read_strat(pre_dict['strat_file'], node_coords)

    bounding_poly = igis.get_boundary_coords(elem_nodes, node_coords)

    layers, Kh, Ss, Sy, Kq, Kv = iwfm.get_gw_params(gw_file)

    strat = np.array([np.array(i) for i in strat])          # stratigraphy to numpy array


    count = map_params_gw('Kh', Kh, node_coords, layers, bounding_poly, strat, format=format, 
                          basename=basename, point_width=point_width, verbose=verbose)

    count += map_params_gw('Kv', Kv, node_coords, layers, bounding_poly, strat, format=format, 
                          basename=basename, point_width=point_width, verbose=verbose)

    count += map_params_gw('Kq', Kq, node_coords, layers, bounding_poly, strat, format=format, 
                          basename=basename, point_width=point_width, verbose=verbose)

    count += map_params_gw('Sy', Sy, node_coords, layers, bounding_poly, strat, format=format, 
                          basename=basename, point_width=point_width, verbose=verbose)

    count += map_params_gw('Ss', Ss, node_coords, layers, bounding_poly, strat, format=format, 
                          basename=basename, point_width=point_width, verbose=verbose)


    print(f'  Created {count:,} groundwater parameter maps')  # update cli

    idb.exe_time()  # print elapsed time

    
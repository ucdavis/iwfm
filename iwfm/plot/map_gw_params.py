# map_gw_params.py
# Create PNG images of groundwater parameters from an IWFM simulation
# Copyright (C) 2023 University of California
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


def plot_one(plot_data, bounding_poly, param_name, layer, basename, units='', point_width=100, png=False, verbose=False ):
    ''' plot_one() - Draw and save one plot

    Parameters
    ----------
    plot_data : list
        numpy array containing x, y, and value

    bounding_poly : shapely Polygon
        Model boundary polygon

    param_name : string
        name of parameter
    
    layer : int
        layer number

    basename : string
        base name of image file

    units : string, default=''
        units of parameter

    point_width : int, default = 100
        The width of the polygon or diameter of the circle to be drawn around each data point.

    png : bool, default = False
        If True, create a png image file.
    
    Returns
    -------
    nothing
    '''
    import iwfm.plot as iplot
    count = 0

    #  Produce tiff point map
    image_name = f'{basename}_{param_name}{layer+1}_nodes.tiff'               #  Set image file name
    iplot.map_to_nodes(plot_data, bounding_poly, image_name, title=f'{param_name} layer {layer+1}', 
                       label=f'{param_name}', units=units )
    count += 1

    #  Produce tiff contour lines map
    image_name = f'{basename}_{param_name}{layer+1}_contour.tiff'       #  Set image file name
    iplot.map_to_nodes_contour(plot_data, bounding_poly, image_name, title=f'{param_name} layer {layer+1}', 
                               label=f'{param_name}', units=units )
    count += 1

    #  Produce tiff filled contour map
    image_name = f'{basename}_{param_name}{layer+1}_contourf.tiff'      #  Set image file name
    iplot.map_to_nodes_contour(plot_data, bounding_poly, image_name, title=f'{param_name} layer {layer+1}', 
                               label=f'{param_name}', units=units, contour='filled' )
    count += 1

    if png:
        #  Produce png map
        image_name = f'{basename}_{param_name}{layer+1}.png'            #  Set png image file name
        iplot.map_to_nodes_png(plot_data, image_name, point_type='circle', point_width=point_width )
        count += 1

    return count





def map_gw_params(node_coords, layers, Kh, Ss, Sy, Kq, Kv, bounding_poly, strat, basename='gw_param_map',
                   point_width=100, verbose=False):
    ''' map_gw_params() - Create PNG images of groundwater parameters 
            from an IWFM simulation

    Parameters
    ----------
    node_coords: numpy array
        nodal coordinates

    layers: int
        number of model layers

    Kh, Ss, Sy, Kq, Kv: numpy arrays
        groundwater parameters

    bounding_poly : numpy array
        Model boundary polygon for masking

    strat : list
        thicknesses of model layers
        strat[][2] == Aquiclude 1, strat[][3] == Layer 1, etc
    
    basename : string
        base name of image file, default = gw_param_map

    point_width : int, default = 100
        The width of the polygon or diameter of the circle to be drawn around each data point.

    Returns
    -------
    count : int
        number of parameter maps created
    '''

    # plot all layers for each parameter
    count = 0
    for layer in range(layers):
        thickness = strat[:,layer*2 + 3]

        # plot Kh for layer 
        plot_data = []
        for i in range(len(node_coords)):
            if thickness[i] > 0:
                plot_data.append([node_coords[i][1], node_coords[i][2], Kh[i][layer]]) 
            else:
                plot_data.append([node_coords[i][1], node_coords[i][2], 0 ]) 
        count += plot_one(plot_data, bounding_poly, 'Kh', layer, basename, '(ft/day)', point_width=point_width)

        # plot Ss for layers > 0
        if layer >= 1:
            plot_data = []
            for i in range(len(node_coords)):
                if thickness[i] > 0:
                    plot_data.append([node_coords[i][1], node_coords[i][2], Ss[i][layer]]) 
                else:
                    plot_data.append([node_coords[i][1], node_coords[i][2], 0 ]) 
            count += plot_one(plot_data, bounding_poly, 'Ss', layer, basename, '', point_width=point_width)

        # plot Sy for layer 1
        if layer < 1:
            plot_data = []
            for i in range(len(node_coords)):
                if thickness[i] > 0:
                    plot_data.append([node_coords[i][1], node_coords[i][2], Sy[i][layer]]) 
                else:
                    plot_data.append([node_coords[i][1], node_coords[i][2], 0 ]) 
            count += plot_one(plot_data, bounding_poly, 'Sy', layer, basename, '', point_width=point_width)
 
        # plot Kq for layer if any thicknesses are greater than 0.0
        if (np.max(strat,axis=0)[layer*2 + 2]) > 0:
            q_thick = strat[:,layer*2 + 2]
            plot_data = []
            for i in range(len(node_coords)):
                if q_thick[i] > 0:
                    plot_data.append([node_coords[i][1], node_coords[i][2], Kq[i][layer]]) 
                else:
                    plot_data.append([node_coords[i][1], node_coords[i][2], 0 ]) 
            count += plot_one(plot_data, bounding_poly, 'Kq', layer, basename, '(ft/day)', point_width=point_width)
 
        # plot Kv for layer 
        plot_data = []
        for i in range(len(node_coords)):
            if thickness[i] > 0:
                plot_data.append([node_coords[i][1], node_coords[i][2], Kv[i][layer]]) 
            else:
                plot_data.append([node_coords[i][1], node_coords[i][2], 0 ]) 
        count += plot_one(plot_data, bounding_poly, 'Kv', layer, basename, '(ft/day)', point_width=point_width)
        if verbose: print(f'  Finished layer {layer+1}\n')

    return count


if __name__ == "__main__":
    import sys
    import numpy as np
    import iwfm as iwfm
    import iwfm.debug as idb

    if len(sys.argv) > 1:  # arguments are listed on the command line
        gw_file   = sys.argv[1]      # groundwate.dat file
        pre_file  = sys.argv[2]      # preprocessor.in file
        bnds_file = sys.argv[3]      # boundary.csv file file
        basename  = sys.argv[4]      # output file base name

        if(len(sys.argv) > 4): point_width = int(sys.argv[5])  # point width
        if point_width == 0: point_width = 100  #default point width


    else:  # get everything form the command line
        gw_file   = input('IWFM Groundwater.dat file name: ')
        pre_file  = input('IWFM Preprocessor file name: ')
        bnds_file = input('Model boundary CSV file name: ')
        basename  = input('Output file base name: ')

    iwfm.file_test(gw_file)
    iwfm.file_test(pre_file)
    iwfm.file_test(bnds_file)

    idb.exe_time()  # initialize timer

    pre_dict, have_lake = iwfm.iwfm_read_preproc(pre_file)

    node_coords, node_list = iwfm.iwfm_read_nodes(pre_dict['node_file'])

    elem_ids, elem_nodes, elem_sub = iwfm.iwfm_read_elements(pre_dict['elem_file'])

    strat, nlayers = iwfm.iwfm_read_strat(pre_dict['strat_file'], node_coords)

    strat = np.array([np.array(i) for i in strat])    # strat to numpy array

    layers, Kh, Ss, Sy, Kq, Kv = iwfm.get_gw_params(gw_file)

    bnds_d = iwfm.file2dict_int(bnds_file)

    bounding_poly = iwfm.bnds2mask(bnds_d, node_coords)

    count = map_gw_params(node_coords, layers, Kh, Ss, Sy, Kq, Kv, bounding_poly, strat, basename, point_width=point_width)

    print(f'  Created {count} groundwater parameter maps')  # update cli

    idb.exe_time()  # print elapsed time

    
# iwfm_map_params.py
# Create a contour map representing nodal values such as groundwater data.
# Copyright (C) 2024 University of California
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

def get_params(data_filename, param_type, param_values, verbose=False):
    ''' get_params() - Get the parameter values from the data file 
    
    Parameters
    ----------
    data_filename : str
        The name of the file containing the parameter values.
        
    param_type : str
        The parameter type to be mapped

    param_values : list
        [parameter type, simulation file, description ]

    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------
    data : list of lists
        Parameter values.

    format : str
        'nodes' or 'elements'
        
        '''
    
    import numpy as np
    import pandas as pd
    import iwfm as iwfm

    if verbose: 
        print(f"Reading parameter values from {data_filename}")
        print(f"Parameter type: {param_type}")

    if param_values[0] == 'Groundwater':
        data = iwfm.iwfm_read_gw_params(data_filename)
        param_types = {'kh': 0, 'ss': 1, 'sy': 2, 'kq': 3, 'kv': 4, 'gwic': 5}
        data = data[param_types[param_type]]
        format = 'nodes'
    elif param_values[0] == 'Rootzone':
        data = iwfm.iwfm_read_rz_params(data_filename)
        param_types = {'wp':0, 'fc':1, 'tn':2, 'lambda':3, 'rzk':4, 'rhc':5, 'cp':6, 'irne':7, 'frne':8, 'imsrc':9, 'tp':10, 'dest':11, 'pk':12}
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'Non-ponded':
        data = iwfm.iwfm_read_rz_npc_params(data_filename)
        param_types = {'npcn': 0, 'npet': 1, 'npwsp': 2, 'npip': 3, 'npms': 4, 'npts': 5, 'nprf': 6, 'npru': 7, 'npic': 8}
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'Ponded':
        data = iwfm.iwfm_read_rz_pc_params(data_filename)
        param_types = {'pcn': 0, 'pet': 1, 'pwsp': 2, 'pip': 3, 'pd': 4, 'pad': 5, 'prf': 6, 'pru': 7, 'pic': 8}
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'Urban':
        data = iwfm.iwfm_read_rz_urban_params(data_filename)
        param_types = {'perv': 0, 'ucn': 1, 'pop': 2, 'wtr': 3, 'ufr': 4, 'uet': 5, 'urt': 6, 'uru': 7, 'uri': 8, 'uic': 9}
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'Native':
        data = iwfm.iwfm_read_rz_nr_params(data_filename)
        param_types = {'ncn': 0, 'rcn': 1, 'net': 2, 'ret': 3, 'rst': 4, 'nvic': 5, 'rvic': 6}
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'Unsaturated':
        data = iwfm.iwfm_read_uz_params(data_filename)
        param_types = {'uzthk': 0, 'uzn': 1, 'uzi': 2, 'uzk': 3, 'urhc': 4, 'uzic': 5}  
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'ET':
        data = iwfm.iwfm_read_et_vals(data_filename)
        param_types = {'et': 0}
        data = data[param_types[param_type]]
        format = 'elements'
    elif param_values[0] == 'Precip':
        data = iwfm.iwfm_read_precip_vals(data_filename)
        param_types = {'pr': 0}
        data = data[param_types[param_type]]
        format = 'elements'

    else:
        print(f"Parameter type {param_type} not found in input_dict")
        sys.exit()
        
    if verbose: print(f"Read parameter values")

    return data, format




def iwfm_map_params(dataset, bounding_poly, image_basename, cmap='rainbow', title="Parameter values", label='Z values', 
                    units='', no_levels=20, contour='line', verbose=False):
    """iwfm_map_params() - Create a contour map representing nodal values such as groundwater data.

    Parameters
    ----------
    dataset : list of lists [[x, y, value], [x, y, value], ...
        A list containing lists of three values (x, y, value), representing the x and y coordinates of each
        data point along with their corresponding values.

    image_basename : str
        The desired name of the image file to be saved.

    cmap : str, default = 'rainbow'
        The colormap to be used for the scatter plot.  See https://matplotlib.org/stable/tutorials/colors/colormaps.html

    title : str, default = "Parameter values"
        Title for the plot.

    label : str, default = 'Z values'
        Label for the colorbar.

    units : str, default = ''
        Units for the colorbar.

    no_levels : int, default = 20
        Number of contour levels.

    contour : str, default = 'line'
        Type of contour to be plotted.  Options are 'line' or 'filled'.

    verbose : bool, default = False
        If True, print status messages.  

    Returns
    -------
    nothing
    """
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    from scipy.interpolate import griddata
    import numpy as np
    import iwfm.plot as iplot



    X, Y, Z = iplot.get_XYvalues(dataset)  # list of lists to numpy arrays

    # Define the contour levels
    levels = iplot.contour_levels(Z, no_levels=no_levels, verbose=verbose)

    # create a regular grid for interpolation
    ratio = (X.max() - X.min()) / (Y.max() - Y.min())
    xi = np.linspace(X.min(), X.max(), int(len(X) * ratio * 0.5 ))
    yi = np.linspace(Y.min(), Y.max(), int(len(Y) / ratio * 0.5 ))
    Xi, Yi = np.meshgrid(xi, yi)

    # interpolate the irregular data onto the regular grid
    Zi = griddata((X, Y), Z, (Xi, Yi), method='linear')

    # Set figure size, width and height in inches
    fig, ax = plt.subplots(figsize=(10, 8))

    # create path from boundary polygon
    print(f"Bounding polygon file: {bounding_poly}")
    path = Path(bounding_poly)

    # create a mask from the path
    mask = path.contains_points(np.column_stack((Xi.ravel(),Yi.ravel()))).reshape(Xi.shape)

    # apply the mask to the data
    Zi = np.ma.masked_array(Zi, mask=~mask) 

    # plot the masked data
    if contour == 'filled':
        plt.contourf(Xi, Yi, Zi, levels=levels, cmap=cmap)    # filled contours
    else:
        plt.contour(Xi, Yi, Zi, levels=levels, cmap=cmap)     # contour lines

    # Add colorbar to show the Z values
    plt.colorbar(label=f'{label} {units}', shrink=.5, fraction=0.046, pad=0.04)   

    # display boundary polygon
    patch = PathPatch(path, facecolor='none')
    ax.add_patch(patch)

    ax.set_title(title)             # Add a title   

    plt.axis('off')                 # Hide X axis and Y axis labels

    plt.savefig(image_name)         # Save the plot to an image file

    #plt.show()                     # Show the plot

    plt.close('all')                # close the plot to free up memory

    if verbose: print(f"Image saved to {image_name}")

    return


if __name__ == "__main__":
    ''' Run iwfm_map_params() from command line '''
    import sys, os
    from pathlib import Path
    import iwfm.debug as idb
    import iwfm as iwfm
    import iwfm.plot as iplot

    args = sys.argv

    if len(args) > 1:  # arguments are listed on the command line
        sim_filename    = args[1]
        pre_filename    = args[2]
        bounding_poly   = args[3]
        param_type      = args[4]
        image_basename  = args[5]
    else:  # ask for file names from terminal
        sim_filename    = input('IWFM Simulation file name: ')
        pre_filename    = input('IWFM Preprocessor file name: ')
        bounding_poly   = input('Boundary polygon file name: ')
        param_type      = input('Parameter keyword: ')
        image_basename  = input('Output image basename: ')

    iwfm.file_test(sim_filename)
    iwfm.file_test(pre_filename)
    iwfm.file_test(bounding_poly)

    input_dict = { 
         'kh'     : [ 'Groundwater', 'Horizontal hydraulic conductivity' ],
         'ss'     : [ 'Groundwater', 'Specific storage' ],
         'sy'     : [ 'Groundwater', 'Specific yield' ],
         'kv'     : [ 'Groundwater', 'Vertical hydraulic conductivity' ],
         'kq'     : [ 'Groundwater', 'Aquiclude hydraulic conductivity' ],
         'gwic'   : [ 'Groundwater', 'Initial groundwater head' ],
         'uzn'    : [ 'Unsaturated', 'Unsaturated zone porosity' ],
         'uzi'    : [ 'Unsaturated', 'Unsaturated zone pore-size distribution index' ],
         'uzk'    : [ 'Unsaturated', 'Unsaturated zone hydraulic conductivity' ],
         'urhc'   : [ 'Unsaturated', 'Method to represent hydraulic conductivity vs. moisture content curve' ],
         'uzic'   : [ 'Unsaturated', 'Initial unsaturated zone moisture content' ],
         'wp'     : [ 'Rootzone',    'Wilting point' ],
         'fc'     : [ 'Rootzone',    'Field capacity' ],
         'tn'     : [ 'Rootzone',    'Porosity' ],
         'lambda' : [ 'Rootzone',    'Pore-size distribution index' ],
         'rzk'    : [ 'Rootzone',    'Rootzone hydraulic conductivity' ],
         'rhc'    : [ 'Rootzone',    'Method to represent hydraulic conductivity vs. moisture content curve' ],
         'cp'     : [ 'Rootzone',    'Capillary rise' ],
         'irne'   : [ 'Rootzone',    'Precipitation column' ],
         'frne'   : [ 'Rootzone',    'Precipitation multiplier' ],
         'imsrc'  : [ 'Rootzone',    'Irrigation source column' ],
         'tp'     : [ 'Rootzone',    'Runoff and return flow destination type' ],
         'dest'   : [ 'Rootzone',    'Runoff and return flow destination value' ],
         'pk'     : [ 'Rootzone',    'Ponded hydraulic conductivity' ],
         'npcn'   : [ 'Non-ponded',  'Curve Number value' ],
         'npet'   : [ 'Non-ponded',  'ET column' ],
         'npip'   : [ 'Non-ponded',  'Irrigation Period column' ],
         'npts'   : [ 'Non-ponded',  'Target soil moisture column' ],
         'nprf'   : [ 'Non-ponded',  'Irrigation water return flow fraction column' ],
         'npic'   : [ 'Non-ponded',  'Initial soil moisture condition' ],
         'pcn'    : [ 'Ponded',      'Curve Number value' ],
         'pet'    : [ 'Ponded',      'ET column' ],
         'pip'    : [ 'Ponded',      'Irrigation Period column' ],
         'pic'    : [ 'Ponded',      'Initial soil moisture condition' ],
         'perv'   : [ 'Urban',       'Percent pervious' ],
         'ucn'    : [ 'Urban',       'Curve Number value' ],
         'pop'    : [ 'Urban',       'Population column' ],
         'wtr'    : [ 'Urban',       'Water use column' ],
         'ufr'    : [ 'Urban',       'Urban demand population fraction' ],
         'uet'    : [ 'Urban',       'ET column' ],
         'urt'    : [ 'Urban',       'Urban fraction to runoff column' ],
         'uru'    : [ 'Urban',       'Urban fraction reused column' ],
         'uri'    : [ 'Urban',       'Urban fraction used indoors column' ],
         'uic'    : [ 'Urban',       'Initial urban moisture content' ],
         'ncn'    : [ 'Native',      'Native Vegetation Curve Number value' ],
         'rcn'    : [ 'Native',      'Riparian Vegetation Curve Number value' ],
         'net'    : [ 'Native',      'Native Vegetation ET column' ],
         'ret'    : [ 'Native',      'Riparian Vegetation ET column' ],
         'rst'    : [ 'Native',      'Riparian Vegetation source stream node' ],
         'nvic'   : [ 'Native',      'Initial native vegetation moisture content' ],
         'rvic'   : [ 'Native',      'Initial riparian vegetation moisture content' ],
         'et'     : [ 'ET',          'ET values' ],
         'pr'     : [ 'Precip',      'Precipitation values' ],
        }   

    print(f" ==> {sim_filename=}")
    print(f" ==> {pre_filename=}")
    print(f" ==> {bounding_poly=}")
    print(f" ==> {param_type=}")
#    print(f"{image_basename=}\n")

    if param_type in input_dict:
        param_values = input_dict[param_type]
#        print(f"Parameter type {param_type}: {param_values} found in input_dict")
#        print(f'param_values[0]: {param_values[0]}\n')
    else:
        print(f" ** Parameter type {param_type} is invalid **")
        print(f"Valid parameter types are:")
        print(input_dict.keys())                        # TODO: develop a better way to print the valid parameter types
        print(f'Exiting...')
        sys.exit()
#    print(f"{param_values=}\n")

    idb.exe_time()                                          # initialize timer

    # determine the file containing the data
    if param_values[0] == 'Groundwater':
        data_filetype = 'gw_file'
    elif param_values[0] == 'Unsaturated':
        data_filetype = 'unsat_file'
    elif param_values[0] == 'Rootzone':
        data_filetype = 'root_file'
    elif param_values[0] == 'Non-ponded':
        data_filetype = 'root_file'
    elif param_values[0] == 'Ponded':
        data_filetype = 'root_file'
    elif param_values[0] == 'Urban':
        data_filetype = 'root_file'
    elif param_values[0] == 'Native':
        data_filetype = 'root_file'
    elif param_values[0] == 'ET':
        data_filetype = 'et_file'
    elif param_values[0] == 'Precip':
        data_filetype = 'precip_file'
    else:
        print(f"Parameter type {param_type} not found in input_dict")
        sys.exit()

#    print(f"data_filetype: {data_filetype}\n")

    # get file names from preprocessor file
    pre_dict, have_lake = iwfm.iwfm_read_preproc(pre_filename)

    # get file names from the simulation file
    sim_dict, have_lake = iwfm.iwfm_read_sim_file(sim_filename)

    # get path to preprocessor main file
    pre_file = Path(pre_filename)
    print(f' ==> Path of {pre_file.name} is {pre_file.parent}')




    if data_filetype == 'root_file':        # get rootzone file names
        rz_filename = Path(sim_filename).parent / sim_dict[data_filetype].replace('\\', '/')
        rz_dict = iwfm.iwfm_read_rz(rz_filename)

        if param_values[0] == 'Non-ponded':
            data_filename = rz_dict['np_file'].replace('\\', '/')
        elif param_values[0] == 'Ponded':
            data_filename = rz_dict['p_file'].replace('\\', '/')
        elif param_values[0] == 'Urban':
            data_filename = rz_dict['ur_file'].replace('\\', '/')
        elif param_values[0] == 'Native':
            data_filename = rz_dict['nr_file'].replace('\\', '/')
        else:
            data_filename = sim_dict[data_filetype].replace('\\', '/')
    else:
        data_filename = sim_dict[data_filetype].replace('\\', '/')

    data_filename = Path(sim_filename).parent / data_filename
#    print(f'data file name: {data_filename}\n')
    iwfm.file_test(data_filename)

    data, format = get_params(data_filename, param_type, param_values)    # Get the parameter values from the data file

    # Read nodal X,Y coordinates from node file
    node_filename = Path(pre_filename).parent / pre_dict['node_file'].replace('\\', '/')
    node_coord, node_list, factor = iwfm.iwfm_read_nodes(node_filename)

    # Read elements from elements file
    elem_filename = Path(pre_filename).parent / pre_dict['elem_file'].replace('\\', '/')

    # calculate element centroids
    elem_centroids = iwfm.elem_centroids(node_filename, elem_filename)

    if format == 'nodes':
        print(' ==> nodal data')
        dataset = []
        for i in range(len(node_list)):
            dataset.append([node_coord[i][1], node_coord[i][2], data[i]])

        # create boundary polygon
        X_min = min([x[1] for x in node_coord])
        X_max = max([x[1] for x in node_coord])
        Y_min = min([x[2] for x in node_coord])
        Y_max = max([x[2] for x in node_coord])

        point_list = [(X_min, Y_min), (X_max, Y_min), (X_max, Y_max), (X_min, Y_max), (X_min, Y_min)]
        from shapely import geometry

        bounding_poly = geometry.Polygon([(p[0], p[1]) for p in point_list])

        iplot.map_to_nodes_contour(dataset, image_basename + '_' + param_type, verbose=True)    # Create a contour map representing nodal values such as groundwater data.

    elif format == 'elements':
        print(' ==> element data')
        dataset = []
        for i in range(len(elem_centroids)):
            dataset.append([elem_centroids[i][1], elem_centroids[i][2], data[i]])


    iwfm_map_params(dataset, bounding_poly, image_basename + '_' + param_type, verbose=True)    # Create a contour map representing nodal values such as groundwater data.

    idb.exe_time()                                          # print elapsed time


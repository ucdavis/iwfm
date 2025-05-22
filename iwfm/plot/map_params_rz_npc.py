# map_rz_params_npc.py
# Create colored maps  representing non-ponded-crop rootzone parameters
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


def get_rz_params_npc(node_file_name, elem_file_name, rz_npc_file_name, verbose=False):
    ''' map_rz_params_npc() - Get non-ponded-crop rootzone parameters and node and element information

    Parameters
    ----------
    node_file_name : str
        IWFM Node.dat file name

    elem_file_name : str
        IWFM Element.dat file name

    rz_npc_file_name : str
        non-ponded crop rootzone file name

    verbose : bool, default = False
        Print status messages

    Return
    ------
    nothing

    '''                
    import iwfm as iwfm
    import iwfm.gis as igis

    # Get info from read nodal file 
    node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file_name)

    # Get info from element file 
    elem_ids, elem_nodes, elem_sub = iwfm.iwfm_read_elements(elem_file_name)

    # use elem_nodes and node_coords to caclculate the centroid of each element
    elem_centroids = iwfm.get_elem_centroids(elem_ids, elem_nodes, node_coords)

    # Use elem_nodes and node_coords to get the boundary coordinates
    boundary_coords = igis.get_boundary_coords(elem_nodes, node_coords)

    # Get the root zone parameters from the non-ponded crop rootzone file
    crops_np, param_vals_np, _ = iwfm.iwfm_read_rz_npc(rz_npc_file_name)        # Read parameters
    param_types_np = ['cn', 'et', 'wsp', 'ip', 'ms', 'ts', 'rf', 'ru', 'ic']
    if verbose: print(f'  Read root zone parameters from the Non-ponded Crop rootzone file {rz_npc_file_name}')

    return elem_centroids, boundary_coords, crops_np, param_vals_np, param_types_np


def map_params_rz_npc(node_file_name, elem_file_name, out_name, rz_npc_file_name, 
                  format='tiff', point_width=100, verbose=False):
    ''' map_params_rz_npc() -Create a colored image map representing non-ponded-crop rootzone parameters

    Parameters
    ----------
    node_file_name : str
        IWFM Node.dat file name

    elem_file_name : str
        IWFM Element.dat file name

    out_name : str
        Output file base name

    rz_npc_file_name : str
        non-ponded crop rootzone file name

    format : str, default = 'png'
        output file format: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp

    point_width : int, default = 100
        point width

    verbose : bool, default = False
        Print status messages

    Return
    ------
    nothing

    '''                
    import iwfm as iwfm
    import iwfm.gis as igis

    elem_centroids, boundary_coords, crops_np, param_vals_np, param_types_np = get_rz_params_npc(node_file_name, 
                elem_file_name, rz_npc_file_name, verbose=verbose)

#    # Get info from read nodal file 
#    node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file_name)
#
#    # Get info from element file 
#    elem_ids, elem_nodes, elem_sub = iwfm.iwfm_read_elements(elem_file_name)
#
#    # use elem_nodes and node_coords to caclculate the centroid of each element
#    elem_centroids = iwfm.get_elem_centroids(elem_ids, elem_nodes, node_coords)
#
#    # Use elem_nodes and node_coords to get the boundary coordinates
#    boundary_coords = igis.get_boundary_coords(elem_nodes, node_coords)
#
#    # Get the root zone parameters from the non-ponded crop rootzone file
#    crops_np, param_vals_np, _ = iwfm.iwfm_read_rz_npc(rz_npc_file_name)        # Read parameters
#    param_types_np = ['cn', 'et', 'wsp', 'ip', 'ms', 'ts', 'rf', 'ru', 'ic']
#    if verbose: print(f'  Read root zone parameters from the Non-ponded Crop rootzone file {rz_npc_file_name}')

    count = 0
    # Curve Numbers
    label='CN values'
    for i in range(len(crops_np)):
        dataset=[[elem_centroids[j][1], elem_centroids[j][2], param_vals_np[0][:,i][j]] for j in range(len(elem_centroids))]
        image_name = f'{out_name}_CN_{crops_np[i].upper()}.{format}'
        title = f'{crops_np[i].upper()} Curve Number'

        iplot.map_to_nodes(dataset, boundary_coords, image_name, cmap='rainbow', marker_size = 10, title=title, 
                label=label, units='', format=format)    
        count += 1

    # Create images for all ET columns 
    label='ET Column'
    for i in range(len(crops_np)):
        dataset=[[elem_centroids[j][1], elem_centroids[j][2], param_vals_np[1][:,i][j]] for j in range(len(elem_centroids))]
        image_name = f'{out_name}_ETcol_{crops_np[i].upper()}.{format}'
        title = f'{crops_np[i].upper()} Evapotranspiration Column'

        iplot.map_to_nodes(dataset, boundary_coords, image_name, cmap='rainbow', marker_size = 10, title=title, 
                label=label, units='', format=format)    
        count += 1

    # irrigation periods
    for i in range(len(crops_np)):
        dataset=[[elem_centroids[j][1], elem_centroids[j][2], param_vals_np[3][:,i][j]] for j in range(len(elem_centroids))]
        image_name = f'{out_name}_IrrPd_{crops_np[i].upper()}.{format}'
        title = f'{crops_np[i].upper()} Irrigation Period Column'

        iplot.map_to_nodes(dataset, boundary_coords, image_name, cmap='rainbow', marker_size = 10, title=title, 
                label=label, units='', format=format)    
        count += 1

    # target soil moisture
    for i in range(len(crops_np)):
        dataset=[[elem_centroids[j][1], elem_centroids[j][2], param_vals_np[5][:,i][j]] for j in range(len(elem_centroids))]
        image_name = f'{out_name}_TSM_{crops_np[i].upper()}.{format}'
        title = f'{crops_np[i].upper()} Target Soil Moisture Column'

        iplot.map_to_nodes(dataset, boundary_coords, image_name, cmap='rainbow', marker_size = 10, title=title, 
                label=label, units='', format=format)    
        count += 1

    # return flow
    for i in range(len(crops_np)):
        dataset=[[elem_centroids[j][1], elem_centroids[j][2], param_vals_np[6][:,i][j]] for j in range(len(elem_centroids))]
        image_name = f'{out_name}_RF_{crops_np[i].upper()}.{format}'
        title = f'{crops_np[i].upper()} Return Flow Column'

        iplot.map_to_nodes(dataset, boundary_coords, image_name, cmap='rainbow', marker_size = 10, title=title, 
                label=label, units='', format=format)    
        count += 1

    # initial condition
    label='Initial Condition'
    for i in range(len(crops_np)):
        dataset=[[elem_centroids[j][1], elem_centroids[j][2], param_vals_np[8][:,i+1][j]] for j in range(len(elem_centroids))]
        image_name = f'{out_name}_IC_{crops_np[i].upper()}.{format}'
        title = f'{crops_np[i].upper()} Initial Conditions'

        iplot.map_to_nodes(dataset, boundary_coords, image_name, cmap='rainbow', marker_size = 10, title=title, 
                label=label, units='', format=format)    
        count += 1

    return count


    
# Run map_rz_params_npc() from command line
if __name__ == "__main__":
    import sys
    import iwfm as iwfm
    import iwfm.plot as iplot
    import iwfm.debug as idb

    point_width_default = 100
    point_width = point_width_default

    verbose = True

    args = sys.argv

    if len(args) > 1:  # arguments are listed on the command line
        node_file_name      = args[1]
        elem_file_name      = args[2]
        rz_npc_file_name    = args[3]
        out_name            = args[4]

        if(len(args) > 5): 
            format          = args[5].lower() # output file format: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp

        if(len(args) > 6): 
            point_width     = int(args[6])  # point width
        if point_width < 1: 
            point_width = point_width_default  # default point width

    else:  # get everything form the command line
        node_file_name      = input('IWFM Node.dat file name: ')
        elem_file_name      = input('IWFM Element.dat file name: ')
        rz_npc_file_name    = input('IWFM Non-Ponded file name: ')
        out_name            = input('Output file base name: ')
        format              = input('Output file format (pdf, png, tiff): ').lower()

    iwfm.file_test(node_file_name)
    iwfm.file_test(elem_file_name)
    iwfm.file_test(rz_npc_file_name)

    idb.exe_time()  # initialize timer

    verbose = True

    count = map_params_rz_npc(node_file_name, elem_file_name, out_name, rz_npc_file_name, 
                        format=format, point_width=point_width, verbose=verbose)
    
    print(f'  Wrote {count:,} {format.upper()} images')

    idb.exe_time()                                          # print elapsed time

    
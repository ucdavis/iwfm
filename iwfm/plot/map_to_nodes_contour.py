# map_to_nodes_contour.py
# Create a contour map representing nodal values such as groundwater data.
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

def contour_levels(Z, no_levels=20, verbose=False):
    """contour_levels() - Define the contour levels for a contour map.

    Parameters
    ----------
    Z : numpy array
        The values to be contoured.

    step_level : int, default = 25
        Step size for contour levels.

    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------
    levels : numpy array
        The contour levels.
    """

    import numpy as np

    # Define the contour levels
    if Z.max() - Z.min() > 10:
        # set interval for contour levels
        if Z.max() - Z.min() > 500:
            step_level = 50
        elif Z.max() - Z.min() > 200:
            step_level = 20
        elif Z.max() - Z.min() > 100:
            step_level = 10
        else:
            step_level = 5
        min_level = int(Z.min())
        while min_level % step_level != 0:
            min_level -= 1
        max_level = int(Z.max())
        while max_level % step_level != 0:
            max_level += 1
        levels = np.arange(min_level, max_level + step_level, step_level)
    else:
        levels = np.linspace(Z.min(), Z.max(), no_levels)

    return levels

def map_to_nodes_contour(dataset, bounding_poly, image_name, cmap='rainbow', title="Parameter values", 
                 label='Z values', units='', no_levels=20, contour='line', verbose=False):
    """map_to_nodes_contour() - Create a contour map representing nodal values such as groundwater data.

    Parameters
    ----------
    dataset : list of lists [[x, y, value], [x, y, value], ...
        A list containing lists of three values (x, y, value), representing the x and y coordinates of each
        data point along with their corresponding values.

    bounding_poly : shapely Polygon
        Model boundary polygon
    
    image_name : str
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
    levels = contour_levels(Z, no_levels=no_levels, verbose=verbose)

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


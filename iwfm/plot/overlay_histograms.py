# overlay_histograms.py 
# Overlay two histograms to visualize the distribution of two datasets.
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


def overlay_histograms(data1, data2, file_name, label1='Data 1', label2='Data 2', alpha=0.5, bins='auto'):
    """
    Overlay two histograms to visualize the distribution of two datasets.

    Parameters
    ----------
    data1 : list or array-like
        The first dataset.

    data2 : list or array-like
        The second dataset.

    label1 : str, optional
        Label for the first dataset.

    label2 : str, optional
        Label for the second dataset.

    alpha : float, optional
        Transparency level for histograms. Value ranges from 0 (completely transparent) to 1 (fully opaque).

    bins : int or str, optional
        Number of bins for the histograms. Can be an integer specifying the number of bins, or a method like 'auto'
        to automatically determine the number of bins.

    Returns
    -------
    None

    Example
    -------
    overlay_histograms(data1, data2, label1='Dataset 1', label2='Dataset 2', alpha=0.5, bins='auto')
    """
    import numpy as np
    import matplotlib.pyplot as plt

    data1 = np.array(data1)
    data2 = np.array(data2)
    
    plt.hist(data1, bins='auto', color = 'r', alpha=0.5, label='Data 1', log = True)
    plt.hist(data2, bins='auto', color = 'g', alpha=0.5, label='Data 2', log = True)

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Overlayed Histograms')
    plt.legend()

    plt.grid(True)
    plt.savefig(file_name)


if __name__ == "__main__":
    gw_file = "C2VSimCG_Groundwater1974.dat"
    
    params = ["kh", "ss", "sy", "kq", "kv"]
    
    #  Choose parameter(s) and layer(s) to graph
    param1 = 0
    layer1 = 0
    param2 = 0
    layer2 = 1


    #  Set image file name
    image_name = f"histogram_{params[param1]}{layer1}_vs_{params[param2]}{layer2}.png"

    #  Read all relevant values from Groundwater.dat
    values = read_gw(gw_file)

    data1 = values[param1][layer1]
    data2 = values[param2][layer2]

    overlay_histograms(data1, data2, image_name, label1='Data 1', label2='Data 2', alpha=0.5, bins='auto')
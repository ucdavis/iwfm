# gw_hyd_noobs.py
# Create PDF files for simulated data vs time for all hydrographs as lines
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


def gw_hyd_noobs(sim_well_list,gwhyd_sim,sim_hyd_names,sim_well_dict,title_words,
                 yaxis_width=-1,verbose=False):
    ''' gw_hyd_noobs() - Create PDF files for simulated data vs time for 
        all hydrographs as lines

    Parameters
    ----------
    well_list : list
        list of well names
    
    gwhyd_sim : list
        simulated IWFM groundwater hydrographs: [0]==dates, [1 to no_hyds]==datasets
    
    sim_hyd_names : list
        simulated hydrograph names (legend entries)
    
    sim_well_dict : dictionary
        key = well name, values = well data from Groundwater.dat file (if IHYDTYP == 0: [HYDTYP, LAYER, X, Y, NAME])
    
    title_words : str
        plot title words
    
    yaxis_width : int, default=-1
        minimum y-axis width, -1 for automatic

    verbose : bool, default=False
        print extra information
    
    Return
    ------
    count : int
        Number of files produced
    
    '''
    import iwfm.plot as iplot
#    import matplotlib.dates as mdates

    no_sim_hyds = len(gwhyd_sim)  # number of simulation time series to be graphed

    print(f'\n     Processing {len(sim_well_list):,} wells,  {no_sim_hyds} simulation(s)\n')

    # compile simulated hydrographs for each well
    count = 0
    for col, sim_well_name in enumerate(sim_well_list): # move through simulation wells
        if verbose:
            print(f' ==> Processing well {sim_well_name}, {col+1} of {len(sim_well_list)}')

        # get simulation data for this well
        sim_hyd_data = []
        for j in range(0, len(gwhyd_sim)):          # cycle through simulation datasets
            temp = []
            for k in range(0, len(gwhyd_sim[j])):   # loop over rows in gwhyd_sim[j]
                temp.append([gwhyd_sim[j][k][0],gwhyd_sim[j][k][col+1]])
            sim_hyd_data.append(temp)
                
        well_info = sim_well_dict.get(sim_well_name)

        iplot.gw_hyd_noobs_draw(sim_well_name, sim_hyd_data, well_info, sim_hyd_names, title_words, 
                                yaxis_width, verbose=verbose)

        count += 1

    return count

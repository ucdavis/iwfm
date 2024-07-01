# gw_hyd_obs.py
# Create PDF files for simulated data vs time for all hydrographs
#  as lines, with observed values vs time as dots
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


def gw_hyd_obs(sim_well_list,obs,gwhyd_sim,sim_hyd_names,sim_well_dict,title_words,
               yaxis_width=-1,verbose=False):
    ''' gw_hyd_obs() - Create PDF files for simulated data vs time for 
        all hydrographs as lines, with observed values vs time as dots

    Parameters
    ----------
    sim_well_list : list of str
        simulated hydrograph well name, often state well number
    
    obs : list
        list of observed values
    
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
    count           (int):  Number of files produced
    
    '''
    import iwfm.plot as iplot
    import numpy as np
    import matplotlib          
    import matplotlib.dates as mdates
    import datetime

    no_sim_hyds = len(gwhyd_sim)  # number of simulation time series to be graphed

    # extract a list of unique well names from first column of obs (all wells with obs data)
    obs_well_list = []
    for j in range(0, len(obs)):
        if obs[j][0] not in obs_well_list:
            obs_well_list.append(obs[j][0])

    print(f'\n     Processing {len(sim_well_list):,} wells,  {no_sim_hyds} simulation(s),  observation data for {len(obs_well_list):,} wells\n')

    # compile simulated hydrographs for each well
    count = 0
    for col, sim_well_name in enumerate(sim_well_list): # move through simulation wells
        if verbose:
            print(f' ==> Processing well {sim_well_name}, {col+1} of {len(sim_well_list)}')

        # get observed data for this well
        obs_dates = []
        obs_meas = []
        for j in range(0, len(obs)):
            if obs[j][0] == sim_well_name:
                obs_dates.append(obs[j][1])
                obs_meas.append(obs[j][3])
        obs_dates = np.array([datetime.datetime.strptime(obs_dates[i], '%m/%d/%Y') for i in range(0, len(obs_dates))])
        obs_meas = np.array(obs_meas)
        if verbose:
            print(f'     {len(obs_dates):,} observations for well {sim_well_name}')


        # get simulation data for this well
        sim_hyd_data = []
        for j in range(0, len(gwhyd_sim)):          # cycle through simulation datasets
            temp = []
            for k in range(0, len(gwhyd_sim[j])):   # loop over rows in gwhyd_sim[j]
                temp.append([gwhyd_sim[j][k][0],gwhyd_sim[j][k][col+1]])
            sim_hyd_data.append(temp)
                
        well_info = sim_well_dict.get(sim_well_name)

        iplot.gw_hyd_obs_draw(sim_well_name, sim_hyd_data, obs_dates, obs_meas, well_info,
                                  sim_hyd_names, title_words, yaxis_width, verbose=verbose)

        if len(obs_dates) == 0:
            print(f'     No observations for well {sim_well_name}')

        count += 1

    return count

# gw_plot_obs.py
# Create PDF files for simulated data vs time for all hydrographs
#  as lines, with observed values vs time as dots
# Copyright (C) 2020-2021 University of California
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


def gw_plot_obs(well_list,no_hyds,obs,gwhyd_sim,gwhyd_names,well_dict,
    titlewords,yaxis_width=-1):
    ''' gw_plot_obs() - Create PDF files for simulated data vs time for 
        all hydrographs as lines, with observed values vs time as dots

    Parameters
    ----------
    well_list : str
        well name, often state well number
    
    no_hyds : int
        number of simulation time series to be graphed
    
    gwhyd_sim : list
        simulated IWFM groundwater hydrographs 
        [0]==dates, [1 to no_hyds]==datasets
    
    gwhyd_names : list
        hydrograph names from PEST observations file
    
    well_dict : dictionary
        key = well name, values = well data from Groundwater.dat file
    
    title_words : str
        plot title words
    
    yaxis_width : int, default=-1
        minimum y-axis width, -1 for automatic
    
    Return
    ------
    count           (int):  Number of files produced
    
    '''
    import iwfm as iwfm

    # cycle through the list of wells in obs to print plots
    # initialize
    count, date, meas = 0, [], []
    date = []         # initialize
    meas = []         # initialize
    obs_well_name = obs[0][0]        # first well name in observations list
    start_date = gwhyd_sim[0][0][0]  # get starting date

    for j in range(1, len(obs)):                      # move through the observation file
        if obs[j][0] != obs_well_name:                # reached the last observation for this well
            if obs_well_name in well_dict:            # draw and save the current plot
                iwfm.gw_plot_obs_draw(obs_well_name,date,meas,no_hyds,gwhyd_sim,gwhyd_names,well_dict.get(obs_well_name),start_date,titlewords,yaxis_width)
                count += 1
            date, meas, name = [], [], obs[j][0]      # re-initialize for next observation well
            obs_well_name = obs[j][0]
        elif obs[j][0] == obs_well_name:              # this observation is for this well
            date.append(obs[j][1])
            meas.append(obs[j][3])

    # make the last one
    if name in well_dict:
        iwfm.gw_plot_obs_draw(obs_well_name,date,meas,no_hyds,gwhyd_sim,gwhyd_names,well_dict.get(obs_well_name),start_date,titlewords,yaxis_width)
        count += 1
    return count

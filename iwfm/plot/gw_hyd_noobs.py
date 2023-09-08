# gw_hyd_noobs.py
# Create PDF files for simulated data vs time for all hydrographs as lines
# Copyright (C) 2020-2023 University of California
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


def gw_hyd_noobs(well_list,no_hyds,gwhyd_sim,gwhyd_names,well_dict,
    titlewords,yaxis_width=-1):
    ''' gw_hyd_noobs() - Create PDF files for simulated data vs time for 
        all hydrographs as lines

    Parameters
    ----------
    well_list : list
        list of well names
    
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
    count : int
        number of files produced
    
    '''
    import iwfm.plot as iplot

    count, date = 0, []
    date.append(gwhyd_sim[0][0][0])
    name = well_list[0]

    start_date = gwhyd_sim[0][0][0]  
    for j in range(1, len(well_list)):  
        if name in well_dict:  # draw and save the current plot
            iplot.gw_hyd_noobs_draw(name,date,no_hyds,gwhyd_sim,gwhyd_names,
                        well_dict.get(name),start_date,titlewords,yaxis_width)
            count += 1
            # re-initialize for next observation well
            date, name = [], well_list[j]
        elif obs[j][0] == obs_well_name:                    # this observation is for this well
            date.append(obs[j][1])
    # make the last one
    if name in well_dict:
        iplot.gw_hyd_noobs_draw(name,date,no_hyds,gwhyd_sim,gwhyd_names,
                        well_dict.get(name),start_date,titlewords,yaxis_width)
        count += 1
    return count

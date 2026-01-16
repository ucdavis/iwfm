# gw_hyd_obs_draw.py
# Draw one groundwater hydrograph plot and save to a PDF file
# Copyright (C) 2020-2026 University of California
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

import datetime
import iwfm


def gw_hyd_obs_draw(sim_well_name, sim_hyd_data, obs_dates, obs_meas, well_info,
                        sim_hyd_names, title_words, yaxis_width=-1,verbose=False):
    ''' gw_hyd_obs_draw() - Create a PDF file with a graph of the simulated data 
        vs time for all hydrographs as lines, with observed values vs time as 
        dots, saved as the_well_name.pdf

    Parameters
    ----------
    sim_well_name : str
        simulated hydrograph well name, often state well number
    
    sim_hyd_data : numpy array
        simulated IWFM groundwater hydrographs for one well, multiple model runs

    obs_dates : numpy array of datetime objects
        observation dates (paired with meas)
    
    obs_meas : numpy array
        observed values (paired with date)
    
    well_info : list
        well data from Groundwater.dat file
        if IHYDTYP == 0: [HYDTYP, LAYER, X, Y, NAME]
        if IHYDTYP == 1: [HYDTYP, LAYER, NODE #, NAME]
    
    sim_hyd_names : list
        simulated hydrograph names (legend entries)
        
    title_words : str
        plot title words
    
    yaxis_width : int, default=-1
        minimum y-axis width, -1 for automatic

    verbose : bool, default=False
        print extra information
    
    Return
    ------
    nothing
    
    '''
    
    import datetime
    import matplotlib
    import numpy as np
    import iwfm

    # Force matplotlib to not use any Xwindows backend.
#    matplotlib.use('TkAgg')  # Set to TkAgg ...
    matplotlib.use('Agg')  # ... then reset to Agg
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_pdf import PdfPages

    line_colors = ['r-' ,'g-' ,'c-' ,'m-' ,'k-' ,'b-' ,'y-' ,
                   'b--','y--','r--','g--','c--','m--','k--',
                   'b:' ,'y:' ,'r:' ,'g:' ,'c:' ,'m:' ,'k:' ]
    # 'r-' = red line, 'bo' = blue dots, 'r--' = red dashes, 
    # 'r:' = red dotted line, 'bs' = blue squares, 'g^' = green triangles, etc

    no_hyds = len(sim_hyd_names)

    if verbose:
        print(f'     Plotting {sim_well_name} with {no_hyds} simulated hydrograph(s).')

    col = well_info[0]

    # determine ymin and ymax for y-axis
    ymin, ymax = 1e6, 1e-6

    if len(obs_meas) > 0:
        ymin = min(ymin, min(obs_meas))
        ymax = max(ymax, max(obs_meas))

    for j in range(no_hyds):
        sim_vals = [float(sim_hyd_data[j][i][1]) for i in range(len(sim_hyd_data[j]))]
        ymin = min(ymin,  min(sim_vals))
        ymax = max(ymax,  max(sim_vals))

    date_diff = sim_hyd_data[j][-1][0] - sim_hyd_data[j][0][0]
    if date_diff.days < 365*10:
        years = 1
    elif date_diff.days < 365*20:
        years = 2
    elif date_diff.days < 365*70:
        years = 5
    else:
        years = 10

    # plot simulated vs sim_dates as line, and meas vs specific dates as points, on one plot
    with PdfPages(f"{sim_well_name}_{iwfm.pad_front(col, 4, '0')}.pdf") as pdf:
        fig = plt.figure(figsize=(10, 7.5))
        ax = plt.subplot(111)
        ax.xaxis_date()
        plt.grid(linestyle='dashed')
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        ax.xaxis.set_major_locator(mdates.YearLocator(years))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        plt.xlabel('Date')
        plt.ylabel('Head (ft msl)')
        plt.title(f'{title_words}: {sim_well_name.upper()} Layer {str(well_info[3])}')
        if len(obs_meas) > 0:
            plt.plot(obs_dates, obs_meas, 'bo', label='Observed')

        # if minimum y axis width was set by user, check and set if necessary
        if (yaxis_width > 0) and (ymax > ymin) and (ymax - ymin < yaxis_width):  # set minimum and maximum values
            center = (ymax - ymin) / 2 + ymin
            plt.ylim(center - yaxis_width / 2, center + yaxis_width / 2)

        for j in range(no_hyds):
            sim_dates = []
            for i in range(len(sim_hyd_data[j])):
                try:
                    # Check if already a datetime object
                    if isinstance(sim_hyd_data[j][i][0], datetime.datetime):
                        date_dt = sim_hyd_data[j][i][0]
                    else:
                        date_dt = iwfm.safe_parse_date(sim_hyd_data[j][i][0], f'sim_hyd_data[{j}][{i}][0]')
                except ValueError as e:
                    raise ValueError(f"Error parsing date in sim_hyd_data[{j}][{i}]: {str(e)}") from e
                sim_dates.append(date_dt)
            sim_data  = [float(sim_hyd_data[j][i][1]) for i in range(len(sim_hyd_data[j]))]
            plt.plot(sim_dates, sim_data, line_colors[j], label=sim_hyd_names[j])

        leg = ax.legend(frameon=1, facecolor='white')
        pdf.savefig()
        plt.close()


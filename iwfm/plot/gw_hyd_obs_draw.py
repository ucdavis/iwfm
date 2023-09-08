# gw_hyd_obs_draw.py
# Draw one groundwater hydrograph plot and save to a PDF file
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


def gw_hyd_obs_draw(well_name,date,meas,no_hyds,gwhyd_sim,gwhyd_name,well_info,
    start_date,title_words,yaxis_width=-1):
    ''' gw_hyd_obs_draw() - Create a PDF file with a graph of the simulated data 
        vs time for all hydrographs as lines, with observed values vs time as 
        dots, saved as the_well_name.pdf

    Parameters
    ----------
    well_name : str
        well name, often state well number
    
    date : list
        list of dates (paired with meas)
    
    meas : list
        list of observed values (paired with date)
    
    no_hyds : int
        number of simulation time series to be graphed
    
    gwhyd_sim : list
        simulated IWFM groundwater hydrographs 
        [0]=dates, [1 to no_hyds]=datasets
    
    gwhyd_name : list
        hydrograph names from PEST observations file
    
    well_info : list
        well data from Groundwater.dat file
        if IHYDTYP == 0: [HYDTYP, LAYER, X, Y, NAME]
        if IHYDTYP == 1: [HYDTYP, LAYER, NODE #, NAME]
    
    start_date : str
        first date in simulation hydrograph files
    
    title_words : str
        plot title words
    
    yaxis_width : int, default=-1
        minimum y-axis width, -1 for automatic
    
    Return
    ------
    nothing
    
    '''
    
    import datetime
    import matplotlib
#    import numpy as np
    import iwfm as iwfm

    # Force matplotlib to not use any Xwindows backend.
#    matplotlib.use('TkAgg')  # Set to TkAgg ...
    matplotlib.use('Agg')  # ... then reset to Agg
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_pdf import PdfPages

    line_colors = ['b-' ,'y-' ,'r-' ,'g-' ,'c-' ,'m-' ,'k-' ,
                   'b--','y--','r--','g--','c--','m--','k--',
                   'b:' ,'y:' ,'r:' ,'g:' ,'c:' ,'m:' ,'k:' ]
    # 'r-' = red line, 'bo' = blue dots, 'r--' = red dashes, 
    # 'r:' = red dotted line, 'bs' = blue squares, 'g^' = green triangles, etc

    col = well_info[0]

    # compile sim_heads here to determine ymax and ymin
    sim_heads = [[float(gwhyd_sim[hyd][row][col]) for row in range(len(gwhyd_sim[hyd]))] for hyd in range(no_hyds)]

    ymin = min(1e6, min(meas))
    ymax = max(1e-6, max(meas))
    ymin = min(ymin, min(min(sim_heads[hyd]) for hyd in range(no_hyds)))
    ymax = max(ymax, max(max(sim_heads[hyd]) for hyd in range(no_hyds)))


    meas_dates = [datetime.datetime.strptime(d, '%m/%d/%Y') for d in date]

    years = mdates.YearLocator()

    # plot simulated vs sim_dates as line, and meas vs specific dates as points, on one plot
    with PdfPages(f"{well_name}_{iwfm.pad_front(col, 4, '0')}.pdf") as pdf:
        fig = plt.figure(figsize=(10, 7.5))
        ax = plt.subplot(111)
        ax.xaxis_date()
        plt.grid(linestyle='dashed')
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        ax.xaxis.set_minor_locator(years)
        plt.xlabel('Date')
        plt.ylabel('Head (ft msl)')
        plt.title(f'{title_words}: {well_name.upper()} Layer {str(well_info[3])}')
        plt.plot(meas_dates, meas, 'bo', label='Observed')

        # if minimum y axis width was set by user, check and set if necessary
        if (yaxis_width > 0) and (ymax > ymin) and (ymax - ymin < yaxis_width):  # set minimum and maximum values
            center = (ymax - ymin) / 2 + ymin
            plt.ylim(center - yaxis_width / 2, center + yaxis_width / 2)

        for j in range(no_hyds):
            sim_dates = [datetime.datetime.strptime(gwhyd_sim[j][i][0], '%m/%d/%Y') for i in range(len(gwhyd_sim[j]))]
            plt.plot(sim_dates, sim_heads[j], line_colors[j], label=gwhyd_name[j])

        leg = ax.legend(frameon=1, facecolor='white')
        pdf.savefig()
        plt.close()


# gw_hyd.py
# Assemble groundwater hydrograph info and call fns to draw individual plots
# Copyright (C) 2020-2025 University of California
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


def gw_hyd(gwhyd_info_file, gwhyd_files, sim_hyd_names, yaxis_width, titlewords, obs_file='none'):
    ''' gw_hyd() - Assemble groundwater hydrograph info and call fns to 
        write individual plots to PDF files

    Parameters
    ----------
    gwhyd_info_file : str
        IWFM groundwater.dat file name
    
    gwhyd_files : list
        list of IWFM dimulated hydrograph file names
    
    sim_hyd_names : list
        list of legend entries
    
    yaxis_width : int
        minimum y-axis width, -1 for automatic
    
    title_words : str
        plot title words
    
    obs_file : str, default = 'none'
        name of PEST smp file with observed values 
    
    Return
    ------
    count : int
        number of hydrographs processed
    
    '''
    
    import iwfm as iwfm
    import iwfm.plot as iplot 

    # read gw hydrograph information from IWFM Groundwater.dat file
    well_dict, well_list = iwfm.read_sim_wells(gwhyd_info_file)  

    # read simulated heads from multiple IWFM groundwater hydrograph files
    gwhyd_sim = iwfm.read_sim_hyds(gwhyd_files)

    # no observed value
    if obs_file.lower()[0] == 'n':
        return iplot.gw_hyd_noobs(well_list, gwhyd_sim, sim_hyd_names, well_dict, titlewords, yaxis_width)

    # have observed values (no else necessary)
    obs = iwfm.read_obs_smp(obs_file)

    return iplot.gw_hyd_obs(well_list, obs, gwhyd_sim, sim_hyd_names, well_dict, titlewords, yaxis_width)



if __name__ == '__main__':
    ' Run gw_hyd() from command line '
    import sys
    import iwfm as iwfm
    import iwfm.debug as idb

    args = sys.argv

    # read arguments from command line
    gwhyd_files = []
    gwhyd_names = []

    if len(args) > 1:  # arguments are listed on the command line
        titlewords = args[1]        # graph title
        obs_file = args[2]          # PEST-style smp file with observed values
        gwhyd_info_file = args[3]   # IWFM Groundwater.data file
        yaxis_width = int(args[4])  # y-axis minimum size
        no_hyds = int(args[5])      # No of simulated hydrograpns
        gwhyd_files = [args[6 + i * 2] for i in range(no_hyds)] # IWFM groundwater hydrograph file
        gwhyd_names = [args[6 + i * 2 + 1] for i in range(no_hyds)]  # Legend name for this hydrograph

    else:  # get everything form the command line
        titlewords      = input('Graph title: ')
        obs_file        = input('Observed values file name (smp format) or \'none\'): ')
        gwhyd_info_file = input('IWFM Groundwater.dat file name: ')
        yaxis_width     = int(input('Minimum y-axis scale (-1 to autoscale): '))
        no_hyds         = int(input('Number of hydrographs to plot: '))
        for i in range(no_hyds):
            filename    = input(f'  IWFM Groundwater Hydrograph {i+1} file name: ')
            gwhyd_files.append(filename)
            legendname  = input(f'  Graph legend for {filename}: ')
            gwhyd_names.append(legendname)

    # test that the input files exist
    if obs_file.lower() != 'none':
        iwfm.file_test(obs_file)
    iwfm.file_test(gwhyd_info_file)
    for i in range(no_hyds):
        iwfm.file_test(gwhyd_files[i])

    idb.exe_time()  # initialize timer
    count = gw_hyd(gwhyd_info_file, gwhyd_files, gwhyd_names, yaxis_width, titlewords, obs_file)
    print(f'  Created {count:,} PDF hydrograph files')  # update cli
    idb.exe_time()  # print elapsed time

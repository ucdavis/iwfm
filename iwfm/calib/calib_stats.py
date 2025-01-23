# calib_stats.py
# Read a PEST .smp file, IWFM groundwater hydrograph file, and IWFM groundwater.dat 
# file, and print a text file with the RMSE and bias of each well and of all observations
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

def read_sim_hyd(gwhyd_file):
    ''' read_sim_hyd() - Read simulated values from an IWFM output hydrograph file
            to numpy array

    Parameters
    ----------
    gwhyd_file : string
        input file name

    Returns
    -------
    gwhyd_sim : numpy array
        hydrograph values from the hydrograph file

    '''
    import numpy as np
    import datetime

    gwhyd_lines = (open(gwhyd_file).read().splitlines())
    gwhyd_lines = [word.replace('_24:00', ' ') for word in gwhyd_lines]

    gwhyd_sim = []
    for j in range(9, len(gwhyd_lines)):
        items= gwhyd_lines[j].split()
        temp = [datetime.datetime.strptime(items.pop(0),'%m/%d/%Y')]                   # date
        alist = [float(x) for x in items]       # values to floats
        temp.extend(alist)
        gwhyd_sim.append(temp)

    return np.array(gwhyd_sim)


def calib_stats(pest_smp_file, gwhyd_info_file, gwhyd_file, verbose=False):
    ''' calib_stats() - Read a PEST .smp file, IWFM groundwater hydrograph 
        file, and IWFM groundwater.dat file, and print a text file with the 
        RMSE and bias of each well and of all observations
    
    Parameters
    ----------
    pest_smp_file : str
        PEST .smp file name
    
    gwhyd_info_file : str
        IWFM groundwater hydrograph file name
    
    gwhyd_file : str
        IWFM groundwater.dat file name
    
    verbose : bool, default=False
        True = command line updates on
    
    Returns
    -------
    nothing
    
    '''

    import datetime
    import iwfm as iwfm
    import iwfm.calib as ical

    if verbose:
        print(f'  pest_smp_file:\t{pest_smp_file}')
        print(f'  gwhyd_info_file:\t{gwhyd_info_file}')
        print(f'  gwhyd_file:   \t{gwhyd_file}\n')
    
    # == read pest observation file into array obs
    head_obs = open(pest_smp_file).read().splitlines()
    for i in range(0,len(head_obs)):
        head_obs[i] = head_obs[i].split()
        head_obs[i][0] = head_obs[i][0]
        head_obs[i][1] = datetime.datetime.strptime(head_obs[i][1],'%m/%d/%Y')
        head_obs[i][3] = float(head_obs[i][3])
    if verbose:
        print(f'  Read {len(head_obs):,} observations from {pest_smp_file}')
        print(f'  head_obs[0]: {head_obs[0]}\n')

    # groundwater hydrograph info to dictionary of groundwater hydrograph info
    hyd_dict = iwfm.read_hyd_dict(gwhyd_info_file)
    if verbose:
        print(f'  Read information for {len(hyd_dict):,} observation wells from {gwhyd_info_file}')
        print(f'  Test: hyd_dict[{head_obs[0][0]}] {hyd_dict[head_obs[0][0]]}\n')

    # read simulated values
    simhyd = read_sim_hyd(gwhyd_file)
    if verbose:
        print(f'  Read {len(simhyd):,} simulated values from {gwhyd_file}\n')

    # == cycle through the list of wells in pest_obs to calculate rmse & bias
    # -- initialize
    i = 1
    dates, meas, sim = [], [], []
    well_names, rmse_values, bias_values, sim_all = [], [], [], []
    meas_all, count, dates, meas, dates_all, names_all = [], [], [], [], [], []

    name, date = head_obs[0][0], head_obs[0][1]

    names_all.append(name)
    dates.append(date)
    dates_all.append(date)
    measured = head_obs[0][3]
    meas.append(measured)
    meas_all.append(measured)

    # use hyd_dict to find the column no for this obs well in simhyd_obs
    simhyd_col = int(hyd_dict.get(name)[0])

    # calculate the simulated value for this observation
    sim_head = ical.sim_equiv(simhyd, date, simhyd_col)
    sim.append(sim_head)    
    sim_all.append(sim_head)    
    
    # move through the head observations
    j = 1
    while j < len(head_obs):
        new_name = head_obs[j][0]
        if new_name != name:  # new well name, finalize info for the last well
    
            if verbose:
                print(f'  Calculating RMSE and Bias for {name}')
            # calculate rmse and bias
            well_names.append(name)

            rmse = ical.rmse_calc(sim, meas)
            bias = ical.bias_calc(sim, meas)

            rmse_values.append(rmse)
            bias_values.append(bias)
            count.append(len(meas))

            dates, meas, sim = [], [], [] # re-initialize for next observation well

            # find next well from head_obs that is in hyd_dict
            while new_name not in hyd_dict:
                j += 1
                new_name = head_obs[j][0]
            name = new_name
            simhyd_col = (hyd_dict.get(name)[0])
    
        names_all.append(name)

        date = head_obs[j][1]
        dates.append(date)
        dates_all.append(date)

        measured = head_obs[j][3]
        meas.append(measured)
        meas_all.append(measured)

        sim_head = ical.sim_equiv(simhyd, date, simhyd_col)
        #simulated = simhyd_obs.sim_head(date,simhyd_col)
        sim.append(sim_head)
        sim_all.append(sim_head)

        j += 1

    # calculate final one
    rmse = ical.rmse_calc(sim, meas)
    bias = ical.bias_calc(sim, meas)

    rmse_values.append(rmse)
    bias_values.append(bias)
    well_names.append(name)
    count.append(len(meas))

    # write all simulated and measured values to a file
    out_file = gwhyd_file.replace('.out','_sim_obs.txt')
    with open(out_file,'w') as of:
        of.write('Well Name\tDate\tSimulated\tObserved\n')
        for i in range(0,len(sim_all)):
            of.write(f'{names_all[i]}\t{dates_all[i].strftime("%m/%d/%y")}\t{sim_all[i]}\t{meas_all[i]}\n')
    print(f'\n  Wrote all simulated and observed values to {out_file}')

    # write out results for each well
    out_file = gwhyd_file.replace('.out','_rmse.txt')
    ical.write_rmse_bias(out_file,hyd_dict,well_names,rmse_values,bias_values,count)
    print(f'  Wrote results for each well to {out_file}')


    # write out results for all wells
    out_file = gwhyd_file.replace('.out','_rmse_all.txt')
    with open(out_file,'w') as of:
        of.write(f'Filename\tRMSE\tBIAS\n')
        rmse_all = round(ical.rmse_calc(sim_all,meas_all),2)
        bias_all = round(ical.bias_calc(sim_all,meas_all),2)
        of.write(f'{gwhyd_file}\t{rmse_all}\t{bias_all}\n')
    print(f'  Wrote results for all wells to {out_file}')
    
    return


if __name__ == '__main__':
    ' Run calib_stats() from command line '
    import sys
    import iwfm as iwfm
    import iwfm.debug as idb

    if len(sys.argv) > 1:  # arguments are listed on the command line
        pest_smp_file = sys.argv[1]
        gwhyd_info_file = sys.argv[2]
        gwhyd_file = sys.argv[3]
    else:
        # ask for file names from terminal
        pest_smp_file   = input('  Observation file name: ')
        gwhyd_info_file = input('  IWFM Groundwater.dat file name: ')
        gwhyd_file      = input('  IWFM Groundwater Hydrograph file name: ')

    iwfm.file_test(pest_smp_file)
    iwfm.file_test(gwhyd_info_file)
    iwfm.file_test(gwhyd_file)

    idb.exe_time()  # initialize timer
    calib_stats(pest_smp_file, gwhyd_info_file, gwhyd_file)

    idb.exe_time()  # print elapsed time

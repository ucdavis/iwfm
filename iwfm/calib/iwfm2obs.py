# iwfm2obs.py
# Read IWFM hydrograph output files and corresponding observation smp files,
# interpolate simulated values to the observation times ('simulated equivalents'),
# and save them in an smp file, optionally writing a paired instruction file.
# Copyright (C) 2020-2023 Hydrolytics LLC
# Based on a PEST utility written by Matt Tonkin
#-----------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------
# This file contains python code based on FORTRAN modules and subroutines written
# by John Doherty. John's utility SMP2SMP was ported to python to time-interpolate
# model simulated values to times of observed values. Also added the option to
# write a PEST instruction file.
#-----------------------------------------------------------------------------


def iwfm2obs(verbose=False):
    ''' iwfm2obs() interpolates model output to match the times and
        locations of calibration observations and puts them into a PEST-compatible
        smp-formatted output file.  

    Parameters
    ----------
    nothing
    
    Returns
    -------
    nothing

    '''
    import os,sys
    import iwfm as iwfm
    import iwfm.calib as calib
    import numpy as np
    import pandas as pd
    from math import ceil
    from scipy.interpolate import interp1d
    from itertools import islice

    # == Get main simulation file name via prompt -----------------------------------
    sim_file    = input('IWFM Simulation main file: ')

    # == Read Time Step info from IWFM Simulation Input File ------------------------
    start_date, end_date, time_step = iwfm.sim_info(sim_file)
    if verbose: print(f'\n  Read Simulation Main File {sim_file}')

    start_date = iwfm.str2datetime(start_date[0:10])                         # starting data as datetime
    end_date   = iwfm.str2datetime(end_date[0:10])                           # ending date as datetime
    latest     = iwfm.dts2days(end_date,start_date)                          # number of days between start and end
    time_step  = time_step.lower()

    sim_file_d = iwfm.iwfm_read_sim(sim_file)                                # get package file names from simulation file
    gw_file_d = iwfm.iwfm_read_gw(sim_file_d['gw'])                          # get groundwater file names from groundwater file

    file_dict = {   # 0                              1             2             3             4             5    6     7       8     9
        # name/type     main_file                smp_obs       smp_out       ins_out       pcf_out       proc wrins rthresh colid skips
        'Streams':     [sim_file_d['stream']   ,'st_obs.smp','st_temp.smp','st_temp.ins','st_temp.pcf',True,True, 0,      1,    [ 6,6]],
        'Groundwater': [sim_file_d['gw']       ,'gw_obs.smp','gw_temp.smp','gw_temp.ins','gw_temp.pcf',True,True, 0,      5,    [20,2]],
        'Subsidence':  [gw_file_d['subsidence'],'sb_obs.smp','sb_temp.smp','sb_temp.ins','sb_temp.pcf',True,True, 0,      5,    [ 5,2]],
        'Tile drains': [gw_file_d['tiledrain'] ,'td_obs.smp','td_temp.smp','td_temp.ins','td_temp.pcf',True,True, 0,      2,    [-1,3]]
    }

    # == Get other inputs via prompts -------------------------------------------------------------
    headdiffs, missing_file = False, 'sim_miss.out'
    nametype   = ['Streams', 'Groundwater', 'Subsidence', 'Tile drains']
    for nt in nametype:
        main_file  = file_dict[nt][0]
        if main_file != 'none':
            bprocess, bwriteins, rthresh = False, False, 0
            obs_file, out_file, ins_file, pcf_file = '', '', '', ''
            if main_file != 'none':
                iwfm.file_test(main_file)                                      # stop
                bprocess = True
                obs_file = input(f'{nt} observation smp file: ')
                iwfm.file_test(obs_file)                                       # stop
                rthresh = float(input('Extrapolation threshold (days, float): '))
                if nt == 'Groundwater':
                    head_diff = input('Calculate head differences? [y/n]: ').lower()
                    if head_diff[0] == 'n':
                        headdiffs, hdiffile = False, 'none'
                    else:
                        headdiffs = True
                        hdiffile  = input('Name of well pairs file: ')
                        iwfm.file_test(hdiffile)                               
                out_file = input('SMP output file name: ')
                ins_file = input('PEST instruction file (or \'none\'): ')
                if ins_file.lower()[0] == 'n':
                    bwriteins = False
                    pcf_file = ins_file
                else:
                    bwriteins = True
                    pcf_file = ins_file[0:ins_file.find('.')]+'.pcf'                  # replace 'ins' with '.pcf'
        # replace file_dict place-holders with new info
        old_value = file_dict[nt]
        new_value = [old_value[0],obs_file,out_file,ins_file,pcf_file,bprocess,bwriteins,rthresh,old_value[8],old_value[9]]
        file_dict.update({nt: new_value})
    if verbose: print(' ')
    print(' ') # clean screen

    # == Process hydrographs --------------------------------------------------------
    hyd_info = []
    for nt in nametype:
        if file_dict[nt][0] != 'none'and file_dict[nt][5] == True:
            if verbose: print(f'\n  Reading {nt} Main File {file_dict[nt][0]}')
            hyd_file, hyd_names = calib.get_hyd_info(nt,file_dict)
            if verbose: print(f'    Read {len(hyd_names)} {nt.lower()} hydrograph locations')
            if nt == 'Groundwater' and headdiffs == True:
                hdiff_sites, hdiff_pairs, hdiff_link = calib.headdiff_read(hdiffile)
                if verbose: print(f'    Read {len(hdiff_sites)} vertical well pairs')
        else:
            hyd_file = 'none'
            hyd_names = []
        hyd_info.append([hyd_file, hyd_names])

    hyd_dict = dict(zip(nametype, hyd_info))                                      # put hyd_info into a dictionary for easier access

    # == Is there anything to do? ----------------------------------------------------------
    todo = 0
    for nt in nametype:
        if file_dict[nt][5] == True:
            todo += len(hyd_dict[nt][1])                                          # count number of nametypes with work
    if todo == 0:
        if verbose: print('\n  Nothing to do, exiting')
        sys.exit()
        return 0

    with open(missing_file, 'w') as fmiss:                                        # erase old version
        fmiss.write('')

    # == read simulated hydrographs --------------------------------------------------------
    for nt in nametype:
        if file_dict[nt][0] != 'none'and file_dict[nt][5] == True:
            if verbose: print(f'\n  Processing {nt.lower()} hydrographs')
            sim_sites = hyd_dict[nt][1]
            sim_hyd, sim_dates = calib.get_sim_hyd(nt,hyd_dict[nt][0],start_date) # read simulated hydrograph values into lists

            # set up function to interpolate time step from date
            time_steps = [x+1 for x in list(range(len(sim_dates)))]
            ts = pd.DataFrame({ 'sim_dates': sim_dates, 'time_steps':  np.array(time_steps)}) # time steps to pandas dataframe
            ts.set_index('sim_dates')['time_steps']                               # dataframe index for function
            ts_func = interp1d(ts.sim_dates,ts.time_steps,kind='linear')          # scipy interpolation function uses dataframe

            obs_file = file_dict[nt][1]
            obs_sites, obs_data = calib.get_obshyd(obs_file,start_date)           # get the observation sites and dates

            sim_miss, sim_both = calib.compare(sim_sites,obs_sites)               # how many obs_sites not in sim_sites?
            calib.write_missing(sim_miss,obs_file,fname=missing_file)

            if verbose: print(f'    Read {len(sim_hyd[0])} simulated {nt.lower()} hydrographs')

            # -- interpolate simulated values to observation dates and put into smp- and ins-format strings
            obs_data.sort( key = lambda l: (l[0], l[1]))                          # sort by site then by date
            obs_site, obs_date, obs_dt = islice(zip(*obs_data), 3)                # put each obs_data col into a separate list
            smp_out, ins_out, hdiff_data, old_site = [], [], [], ''
            for i in range(0,len(obs_data)):
                if obs_site[i] in sim_sites:
                    if obs_site[i] != old_site:                                   # set up interpolation function for new site
                        old_site = obs_site[i]
                        col_id = sim_sites.index(obs_site[i])
                        sim = []
                        for j in range(0,len(sim_hyd)):
                            sim.append(sim_hyd[j][col_id])
                        # set up function to interpolate simulated values to obs dates
                        df = pd.DataFrame({ 'dates': sim_dates, 'sim_vals':  np.array(sim)}) # sim values to pandas dataframe
                        df.set_index('dates')['sim_vals']                         # dataframe index for function
                        sim_func = interp1d(df.dates,df.sim_vals,kind='linear')   # scipy interpolation function uses dataframe

                    if obs_date[i] < latest:                                      # should latest be end_date?
                        obs_val = float(sim_func(obs_date[i]))                    # use interpolation function
                        ts = ceil(float(ts_func(obs_date[i])))                    # use interpolation function

                        smp, ins = calib.to_smp_ins(obs_site[i],obs_dt[i],obs_val,ts)   # put into smp and ins strings
                        smp_out.append(smp)                                       # add smp string to smp_out list
                        ins_out.append(ins)                                       # add ins string to ins_out list

                        if nt == 'Groundwater' and headdiffs == True and obs_site[i] in hdiff_sites:
                            hdiff_data.append([obs_site[i],obs_dt[i],obs_val,ts])

            if nt == 'Groundwater' and headdiffs == True and len(hdiff_data) > 0:  # process headdiffs
                smp, ins = calib.headdiff_hyds(hdiff_pairs, hdiff_data, file_dict[nt][5], ts_func, start_date, verbose)
                smp_out.extend(smp)                                                # add smp string list to smp_out list
                ins_out.extend(ins)                                                # add ins string list to ins_out list

            # -- write smp file ----------------------------------------------------------------
            smp_outfile  = file_dict[nt][2]
            with open(smp_outfile, 'w') as f:
                for item in smp_out:
                    f.write("%s\n" % item)
            if verbose: print(f'    Wrote {len(smp_out):,} simulated {nt.lower()} values to {smp_outfile}')

            # -- write ins file ----------------------------------------------------------------
            if file_dict[nt][6] == True:        # iwriteins
                ins_outfile  = file_dict[nt][3]
                with open(ins_outfile, 'w') as f:
                    f.write("pif #\n")
                    for item in ins_out:
                        f.write("%s\n" % item)
                if verbose: print(f'    Wrote instrutions to {ins_outfile}')

                # -- if pcf creation is added to smp2smp, write pcf file -------------------------
                #pcf_file  = file_dict[nt][4]
                #with open(pcf_file, 'w') as fpcf:
                #  for item in pcf_out:
                #    fpcf.write("%s\n" % item)
                #print('    Wrote pcf to {}'.format(pcf_file))


if __name__ == "__main__":
    ''' Run iwfm2obs() from command line '''
    import iwfm.debug as idb

    idb.exe_time()  # initialize timer
    iwfm2obs(verbose=True)

    idb.exe_time()  # print elapsed time



# get_obs_hyd.py
# Extract one column from a VIC file to another file
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


def get_obs_hyd(obs_file,start_date):
    ''' get_obs_hyd - reads an observation sample bore (smp) file, and returns a list 
        of observation sites and a list of observation data as [site_id, days since 
        start, date as datetime object]

    Parameters
    ----------
    obs_file : str
        name of observation file (in SMP format)

    start_date : datetime object
        simulation starting date


    Returns
    -------
    obs_sites : list of str
        observation site names

    obs_data : list
        [site name, days since start, date as datetime object]

    '''

    import iwfm as iwfm
  
    obs_lines = open(obs_file).read().splitlines()                      # obs_lines has observations to match
    obs_data, obs_sites = [], []
    for line in obs_lines:
        item = line.split()
        if item[0] not in obs_sites:
            obs_sites.append(item[0])
        days = iwfm.dts2days(iwfm.str2datetime(item[1]), start_date)                # days since start_date
        obs_data.append([item[0],days,iwfm.str2datetime(item[1])])             # site, days since start, date as datetime object

    obs_data.sort( key = lambda l: (l[0], l[1]))
    obs_sites.sort( key = lambda l: (l[0]))

    #print(f'\n==> {obs_sites=}\n {obs_data=}\n')

    return obs_sites, obs_data 

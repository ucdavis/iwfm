# to_smp_ins.py
# Write smp and ins file lines for one observation
# Copyright (C) 2020-2023 University of California
# Based on a PEST utility written by John Doherty
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


def to_smp_ins(obs_site,obs_dt,obs_val,ts):   # put into smp and ins strings
    ''' to_smp_ins() - Write smp and ins file lines for one observation

    Parameters
    ----------
    obs_site : str
        site name

    obs_dt : datetime object
        date

    obs_val : float
        simulated value

    ts : ind
        time step

    Returns
    -------
    smp : string
        the observation in smp-file format: 
             'obs_site             mm/dd/yyyy  0:00:00                obs_val'

    ins : string
        the observation in ins-file format: 
             'L1  [obs_site_0ts]42:70'

    '''

    import iwfm as iwfm

    smp = str(f'{iwfm.pad_back(obs_site,20)} {obs_dt.strftime("%m/%d/%Y")}  0:00:00 {iwfm.pad_front(round(obs_val,6),22)}')
    ins = str(f'L1  [{obs_site}_{iwfm.pad_front(ts,3,"0")}]42:70')

    return smp, ins
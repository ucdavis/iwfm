# sim_head.py
# Return the simulated head for a given date and column
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


def sim_head(date, col, heads):
    ''' sim_head() - Return the simulated head for a given date and column

    Parameters
    ----------
    date : datetime object
        Date for simulated head value
  
    col : int
        Column number of simulated heads dataframe
  
    heads : pandas dataframe
        Index = dates, cols 1-n = simulated head values
  
    Returns
    -------
    h : float
        Simulated head value

    '''

    print(f' function has not been created ')
    h = 0.0
    return h

#    with open(name + '_obs.out', 'w') as o:
#        o.write(f'# Observations for well {name}\n')
#        o.write('# Date\tObserved\tModeled\n')
#        for i in range(0, len(date)):
#            o.write(f'{date[i]}\t{meas[i]}\t{sim[i]}\n')
#    return i

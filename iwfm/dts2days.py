# dts2days.py
# Calculate number of days since simulation start
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

def dts2days(dates, start_date):
    ''' dts2days() - Converts a series of dates to a series of float values that represent days 
        since start_date.
    
    Parameters
    ----------
    dates : list of datetime objects
        dates during simulation period

    start_date : dtaetime object
        simulation start time

    Returns
    -------
    out : list of floats
        each is a dates item - start_date

    '''
    from datetime import date, datetime

    if isinstance(dates, datetime): # there's only one item, not a list
        out = (dates - start_date).days
    else:
        out = []
        for d in dates:
            out.append((d - start_date).days)
    return out

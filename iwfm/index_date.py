# index_date.py
# Returns no days between two dates
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


def index_date(in_date, start_date='10/01/1984'):
    ''' index_date() - Return the number of days from start_date to in_date

    Parameters
    ----------
    in_date : str
        date after start_date
    
    start_date : str, default='10/01/1984'
        date to count from

    Returns
    -------
    days            (int):   Number of days between two dates
    
    '''
    from datetime import datetime
    
    # Parse dates in MM/DD/YYYY format
    start_month, start_day, start_year = map(int, start_date.split('/'))
    in_month, in_day, in_year = map(int, in_date.split('/'))
    
    # Create datetime objects
    start_dt = datetime(start_year, start_month, start_day)
    in_dt = datetime(in_year, in_month, in_day)
    
    # Calculate difference in days
    diff = in_dt - start_dt
    return diff.days

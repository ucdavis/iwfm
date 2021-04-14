# index_date.py
# Returns no days between two dates
# Copyright (C) 2020-2021 Hydrolytics LLC
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
    import iwfm as iwfm

    ys, ms, ds = iwfm.year(start_date), iwfm.month(start_date), iwfm.day(start_date)
    yi, mi, di = iwfm.year(in_date), iwfm.month(in_date), iwfm.day(in_date)

    # special case: in_date == start_date
    if ys == yi and ms == mi and ds == di:
        return 0

    mdays = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    # days from start_date to end of year
    ds = mdays[ms - 1] - ds  # days to end of month
    if int(ys / 4) > 0 and ms > 1:  # leap year
        ds += 1
    for m in range(ms, 12):
        ds += mdays[m]

    # days from beginning of year to in_date
    if mi > 1:
        for m in range(0, mi - 1):  # omits leap years
            di += mdays[m]  # mi=0 points to Jan, etc.

    years = yi - ys
    if yi >= ys:
        years -= 1

    days = ds + di + years * 365 + int(years / 4)
    return days

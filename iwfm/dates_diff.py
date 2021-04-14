# dates_diff.py
# Days between two dates
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


def dates_diff(date1, date2):
    ''' dates_diff() - Returns the number of days between two
    datetime objects

    Parameters
    ----------
    date1 : datetime object
        a date

    date2 : datetime object
        another date

    Returns
    -------
    diff : int
        number of days between the two input dates

    '''
    return abs(date2 - date1).days


if __name__ == "__main__":
    " Run vic_2_table() from command line "
    import sys
    from dateutil.parser import parse

    if len(sys.argv) > 1:  # arguments are listed on the command line
        date1 = sys.argv[1]
        date2 = sys.argv[2]
    else:  # ask for file names from terminal
        date1 = input('First date: ')
        date2 = input('Second date: ')

    date_1 = parse(date1)
    date_2 = parse(date2)

    diff = dates_diff(date_1, date_2)

    print(f'  {date1} and {date2} are {diff} days apart')

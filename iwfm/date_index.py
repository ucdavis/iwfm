# date_index.py
# Returns date inval dates from start_date
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


def date_index(inval, start_date):
    """ date_index() - Calculate a date inval months from start_date

    Parameters:
      inval           (int):  Number of months from start_date
      start_date      (str):  Date in MM/DD/YYYY format

    Returns:
      nothing
    
    """
    import iwfm as iwfm

    y = iwfm.year(start_date)
    m = iwfm.month(start_date)
    d = iwfm.day(start_date)
    for i in range(1, int(inval)):
        if m == 12:
            y = y + 1
            m = 1
        else:
            m = m + 1
    return iwfm.date2text(d, m, y)


if __name__ == "__main__":
    " Run date_index() from command line "
    import sys
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        inval = sys.argv[1]
        start_date = sys.argv[2]
    else:  # ask for file names from terminal
        start_date = input('Date (MM/DD/YYYY):')
        inval = input('Number of months: ')

    end_date = date_index(inval, start_date)

    print(f'  {end_date} is {inval} months after {start_date}.')

# text_date.py
# Converts M/D/YY to MM/DD/YYYY
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


def text_date(text):
    ''' text_date() - Convert M/D/YY to MM/DD/YYYY

    Parameters
    ----------
    text : str
        date in some format like M/D/YY

    Returns
    -------
    date string in MM/DD/YYYY format
    '''
    import iwfm as iwfm

    m = iwfm.month(text)
    d = iwfm.day(text)
    y = iwfm.year(text)

    if m < 10:
        mo = '0' + str(m)
    else:
        mo = str(m)
    if d < 10:
        dy = '0' + str(d)
    else:
        dy = str(d)
    return mo + '/' + dy + '/' + str(y)

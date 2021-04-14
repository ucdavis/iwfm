# date2text.py
# Returns text MM/DD/YYYY
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


def date2text(d, m, y):
    ''' date2text() - Return text MM/DD/YYYY

    Parameters
    ----------
    d : int
        day of month
    
    m : int
        month
    
    y : int
        year

    Returns
    -------
    Date in MM/DD/YYYY format
    
    '''
    if m < 10:
        mo = '0' + str(m)
    else:
        mo = str(m)
    if d < 10:
        dy = '0' + str(d)
    else:
        dy = str(d)
    if y < 20:
        y = 2000 + y
    elif y < 100:
        y = 1900 + y
    return mo + '/' + dy + '/' + str(y)

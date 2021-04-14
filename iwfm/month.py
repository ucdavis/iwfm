# month.py
# extracts month from MM/DD/YY or MM/DD/YYYY and sonverts to integer
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


def month(text):
    ''' month() - Extract month from MM/DD/YY or MM/DD/YYYY to an integer

    Parameters
    ----------
    text : str
        date as a string in m/d/y format

    Returns
    -------
    month : int
        month as integer (Jan == 1, .., Dec == 12)

    '''
    return int(text[0 : text.find('/')])


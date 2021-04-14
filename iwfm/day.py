# day.py
# Extracts day from MM/DD/YY or MM/DD/YYYY and sonverts to integer
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


def day(text):
    ''' day() - Extract day from MM/DD/YY or MM/DD/YYYY
        to an integer

    Parameters
    ----------
    text : str
        date as string

    Returns
    -------
    day : int
        day of month 

    '''
    new_text = text[text.find("/") + 1 : len(text)]
    return int(new_text[0 : new_text.find("/")])

# year.py
# Extracts year from MM/DD/YY or MM/DD/YYYY and sonverts to integer
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


def year(text):
    ''' year() - Extract year from MM/DD/YY or MM/DD/YYYY to an integer

    Parameters
    ----------
    text : str
        date in MM/DD/YY or MM/DD/YYYY format

    Returns:
    year : int
        year as integer

    '''
    new_text = text[text.find("/") + 1 : len(text)]
    y = int(new_text[new_text.find("/") + 1 : len(new_text)])
    if y < 1000:  # MM/DD/YY format
        if y > 20:
            y = y + 1900
        else:
            y = y + 2000
    return y

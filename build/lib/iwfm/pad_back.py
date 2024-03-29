# pad_back.py
# Convert input value to a string and pad end with specified character
# (or space if none specified)
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


def pad_back(item, n=1, t=' '):
    ''' pad_back() - Convert item to a string and then adds multiple copies
        of text character t after item until the string is at least n 
        characters long

    Parameters
    ----------
    item : any single item
        item to be converted to string
    
    n : int, default=1
        minimum string character length
    
    t : str
        character to add to pad string to desired length

    Returns
    -------
    Padded string
    
    '''
    s = str(item)
    while len(s) < n:
        s = s + t
    return s

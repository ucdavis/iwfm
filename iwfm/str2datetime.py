# str2datetime.py
# Convert a string in %m/%d/%y format to a datetime object
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

def str2datetime(s):
    '''str2datetime() - Convert a string in %m/%d/%y format to a datetime object

    Parameters
    ----------
    s : str
        string in %m/%d/%y format

    Returns
    -------
    d : datetime object
        
    '''
    from datetime import date, datetime
  
    d = s.split('/')
    return datetime(int(d[2]), int(d[0]), int(d[1]))

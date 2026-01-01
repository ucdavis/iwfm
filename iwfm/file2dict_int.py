# file2dict_int.py
# Read file of paired integers into a dictionary
# Copyright (C) 2020-2026 University of California
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


def file2dict_int(infile, key_field=0, val_field=1, skip=0):
    ''' file2dict_int() - Read file with paired integers, return dictionary 

    TODO: merge into file2dict as type=='int' option, also add 'float' etc

    Parameters
    ----------
    infile : str
        name of input file
    
    key_field : int, default=0
        list field to use as key
    
    val_field : int, default=1
        list field to use as value
    
    skip : int, default=0
        Number of header rows to skip

    Returns
    -------
    d : dicttionary
        dictionary from file contents
    
    '''
    import re

    d = {}
    with open(infile) as f:
        info = f.read().splitlines()  # open and read input file
    for i in range(len(info)):
        if i > skip:
            items = re.split(';|,|\*|\n|\t', info[i])
            key, values = int(items[key_field]), int(items[val_field])
            d[key] = values
    return d

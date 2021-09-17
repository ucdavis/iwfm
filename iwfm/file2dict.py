# file2dict.py
# Read file of paired items into a dictionary
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


def file2dict(infile, key_field=0, val_field=1, skip=0):
    ''' file2dict() - Read file with paired items, return dictionary 

    Parameters
    ----------
    infile : str
        Name of file with tabular data
    
    key_field : int, default=0 (first column)
        Field that is the key
    
    val_field : int, default=1 (second column)
        Field that is the value
    
    skip : int, default=0 (no header)
        Number of non-comment lines to skip (header)

    Returns
    -------
    d : dict
        Dictionary from file contents

    '''
    import re

    d = {}
    info = open(infile).read().splitlines()  # open and read input file
    for i in range(0, len(info)):
        if i > skip - 1:  # because of zero indexing
            items = re.split(';|,|\*|\n|\t', info[i])
            key, values = items[key_field], items[val_field]
            d[key] = values
    return d

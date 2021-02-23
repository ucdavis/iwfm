# file2dict_int.py
# Read file of paired integers into a dictionary
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


def file2dict_int(infile, key_field=0, val_field=1, skip=0):
    """ file2dict_int() - Read file with paired integers, return dictionary 

    Parameters:
      infile          (str):  Name of input file
      key_fiels       (int):  List field to use as key
      val_field       (int):  List field to use as value
      skip            (int):  Rop row of table data in file

    Returns:
      d               (dict): Dictionary 
    """
    import re

    d = {}
    info = open(infile).read().splitlines()  # open and read input file
    for i in range(0, len(info)):
        if i > skip:
            items = re.split(';|,|\*|\n|\t', info[i])
            key, values = int(items[key_field]), int(items[val_field])
            d[key] = values
    return d

# list2dict.py
# create a dictionary from a list
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


def list2dict(items):
    """ list2dict() - Create a dictionary from a list

    Parameters:
      items           (list): List of items, unique first column

    Returns:
      d               (dict): Dictionary created from items
    """
    d = {}
    for i in range(0, len(items)):
        key, values = items[i][0], items[i][1:]
        d[key] = values
    return d

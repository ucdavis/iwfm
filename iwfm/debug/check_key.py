# check_key.py
# check if key is in dictionary, for debugging
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


def check_key(d, key):
    """ check_key() - check if key is in dictionary, for debugging

    Parameters:
      d          (dict): Dictionary
      key        (*):    Dictionary key value
    
    Return:
      True       (bool): key is in dictionary
      False      (bool): key is not in dictionary
    """
    if key in d.keys():
        return True
    else:
        return False

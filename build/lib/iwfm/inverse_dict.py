# inverse_dict.py
# create an inverse dictionary (only if all values unique)
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


def inverse_dict(d):
    ''' inverse_dict() - Create an inverse dictionary (only if all
        values unique, single value for each key)

    Parameters
    ----------
    d : dictionary
        dictionary with one value item per key

    Returns
    -------
    inv_dict : dictionary
        dictionary with keys -> values, values -> keys
    
    '''
    inv_dict = []
    inv_dict = {v: k for k, v in d.items()}
    return inv_dict

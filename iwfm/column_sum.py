# column_sum.py
# Sum all numbers in an array column
# Copyright (C) 2020-2023 University of California
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


def column_sum(lst):
    ''' column_sum() - takes one column of an array as input and returns
        the sum of all items
    
    Parameters
    ----------
    lst : list of numbers
        one column of an array

    Returns
    -------
    * : int or float
        sum of all numbers in the column

    '''
    return [sum(i) for i in zip(*lst)]

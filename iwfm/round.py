# round.py
# round a number
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


def round(item, decimals):
    """ round() - Round a number

    Parameters:
      item            (*):    Number ot round off
      decimals        (*):    Number of decimal places

    Returns:
      pdf             (PDF):   PDF object
    """
    decimals = int(decimals)
    if decimals == 0:
        return int(item)
    elif decimals > 0:
        factor = 10.0 ** int(decimals)
        return int(factor * item) / factor
    else:
        print(f" * round({item},{decimals}) - Can't round to value less than 0 *")
        sys.exit()
    return

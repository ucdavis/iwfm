# file_missing.py
# Print message to console and exit
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


def file_missing(filename):
    ''' file_missing() - Exit with a message that the file does not exist

    Parameters
    ----------
    filename : str
        file name
    
    Returns
    -------
        nothing
 
    '''
    import sys

    print('  *****************************************************************')
    print('  * ')
    print(f'  *   File path {filename} does not exist.')
    print('  *   Quitting.')
    print('  * ')
    print('  *****************************************************************')
    sys.exit()
    return

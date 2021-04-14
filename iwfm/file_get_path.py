# file_get_path.py
# Return the path to a file as a string
# Copyright (C) 2018-2021 Hydrolytics LLC
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


def file_get_path(filename):
    ''' file_get_path() - Return the path to a file as a string

    Parameters
    ----------
    filename : str
        file name with path

    Returns
    -------
    path to file
    
    '''
    import re
    from pathlib import Path

    fpath = re.split('\\|/', filename)
    newpath = Path('/'.join(fpath))
    return newpath

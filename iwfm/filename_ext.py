# filename_ext.py
# Return filename extension
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


def filename_ext(filename, ext):
    ''' filename_ext() - Add the specified extension to the filename
        or replace existing extention

    Parameters
    ----------
    filename : str
        file name
    
    ext : str
        file name extension

    Returns
    -------
    filename : str
        file name with extension
    
    '''
    if filename.find('.') == len(filename) - 1:  # if last char is '.'
        filename = filename[:-1]
    if f'.{ext}' not in filename:
        filename = f'{filename}.{ext}'
    return filename

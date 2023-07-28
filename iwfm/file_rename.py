# file_rename.py
# Rename file
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


def file_rename(filename, newname, force=0):
    ''' file_rename() - Rename a file

    Parameters
    ----------
    filename : str
        name of existing file
    
    newname : str
        new name for existing file
    
    force : int, default=0
        0 = don't force overwrite if another file named newname 
                already exists
        1 = force overwrite if another file named newname 
                already exists

    Returns
    -------
    nothing
    
    '''
    import os, sys

    if os.path.isfile(newname):  # if file newname already exists
        if force:  # if force>0 then remove
            os.remove(newname)
        else:
            print(f'  *   Error: Can\'t rename {filename} to {newname}.\n')
            print(f'  *   Destination file already exists.\n')
            print('  *   Quitting.')
            sys.exit()
    os.rename(filename, newname)

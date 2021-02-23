# file_rename.py
# Rename file
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


def file_rename(filename, newname, force=0):
    """ file_rename() - Rename a file

    Parameters:
      filename        (str):  Name of existing file
      newname         (str):  New name for existing file
      force           (int):  Force overwrite if another file named newname 
                                already exists

    Returns:
      nothing
    """
    import os, sys

    if os.path.isfile(newname):  # if file newname already exists
        if force:  # if force>0 then remove
            os.remove(newname)
        else:
            print(
                "  *   Error: Can't rename {} to {}. Destination file already exists.\n".format(
                    filename, newname
                )
            )
            print("  *   Quitting.")
            sys.exit()
    os.rename(filename, newname)
    return

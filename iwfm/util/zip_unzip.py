# zip_unzip.py
# unzip a zip file
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


def zip_unzip(filename, verbose=False):
    """ zip_unzip() - Unzips a zipfile

    Parameters:
      filename        (str):  Zip file
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing
    """
    import zipfile

    zip = open(filename, "rb")
    zipList = zipfile.ZipFile(zip)
    for name in zipList.namelist()[1:]:
        out = open(name, "wb")
        out.write(zipList.read(name))
        out.close()
    if verbose:
        print("=> Unzipped '{}'".format(filename))
    return 0

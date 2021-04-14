# url_fetch.py
# download a file from URL
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


def url_fetch(url, filename, verbose=False):
    ''' url_fetch() - Download file at url to filename

    Parameters
    ----------
    url : str
        web address

    filename : str
        file name to save info from url

    verbose : bool, default=False
        True = command-line output on

    Return
    ------
    nothing

    '''
    import requests

    r = requests.get(url=url, verify=False)
    with open(filename, 'wb') as f:
        f.write(r.content)
    if verbose:
        print(f'  Retrieved \'{filename}\' ')
    return 

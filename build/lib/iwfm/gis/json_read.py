# json_read.py
# Get bounding polygon
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


def json_read(jdata, verbose=False):
    ''' json_read() - Read a json file
    
    Parameters
    ----------
    jdata : str
        JSON file name
    
    verbose : bool, default=False
        True = command line updating on

    Returns
    -------
    j : JSON object
        JSON data
    
    '''
    import json

    j = json.loads(jdata)
    if verbose:
        print('  JSON Data:')
        print(f'    {json.dumps(j, indent=5)}')
    return j

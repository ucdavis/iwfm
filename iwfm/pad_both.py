# pad_both.py
# converts item to a string and then adds f copies of text character t
# before item, then multiple copies of text character t at the end
# until it is b characters long (default t is space)
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


def pad_both(item, f=1, b=1, t=' '):
    ''' pad_both(item, f, b, t) - Convert item to a string and then
        adds f copies of text character t before item , then multiple copies
        of text character t at the end until it is b characters long
        (default t is space)

    Parameters
    ----------
    item: (*)
        single item (string, int, float etc)
    
    f : int, default=1
        number of leading fill characters
    
    b : int, default=1
        total lentgh of final string in characters
    
    t : str, default=' '
        character(s) to padd front and back

    Returns
    -------
    s : str
        padded string b characters long

    '''
    s = str(item)
    for i in range(0, f):
        s = t + s
    while len(s) < b:
        s = s + t
    return s

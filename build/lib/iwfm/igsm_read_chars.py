# igsm_read_chars.py
# Read an IGSM pre-processor element characteristics file
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


def igsm_read_chars(char_file, elem_nodes):
    ''' igsm_read_chars() - Read an IGSM Element Characteristics file and 
        returns a list of characteristics for each element.

    Parameters
    ----------
    char_file : str
        IGSM Element Characteristics file name
    
    elem_nodes : list
        elements and associated nodes

    Returns
    -------
    elem_char : list
        element characteristics
    
    '''
    import iwfm as iwfm

    char_lines = open(char_file).read().splitlines()  # open and read input file
    char_index = iwfm.skip_ahead(0, char_lines, 0)  # skip comments
    elem_char = []
    for i in range(0, len(elem_nodes)):
        l = char_lines[char_index + i].split()
        this_elem = int(l.pop(0))
        chars = []
        chars.append(int(l.pop(0)))    # rain station
        chars.append(float(l.pop(0)))  # rain factor
        chars.append(int(l.pop(0)))    # drainage destination
        chars.append(int(l.pop(0)))    # subregion
        temp = int(l.pop(0))           # don't use
        chars.append(float(l.pop(0)))  # soil type
        elem_char.append(chars)
    return elem_char

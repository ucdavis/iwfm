# file_2_list.py
# Converts a portion of a text file to a list of file lines
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


def file_2_list(filename, slice_end=0, slice_start=0, skip=0):
    ''' file_2_list()  - Reads a text file,  and returns it as a list of 
        file lines. Optionally, it can be a slice of each line.
        Header lines can also be skipped.
        
    Parameters
    ----------
    filemane : str
        name of input file
    
    slice_end : int, default=0
        last character to read on each line, 0=to end
    
    slice_start : int, default=0
        first character to read on each line, 0=beginning
    
    skip : int, default=0
        number of header lines ot skip
    
    Returns
    -------
    outlist : list of strings

        '''
    lines = open(filename).read().splitlines()

    out_list, i = [], skip 
    if slice_end < slice_start:
        slice_end = 0
    while i < len(lines):
        start = slice_start
        end = len(lines[i])
        if slice_end > 0:
            end = min(slice_end, end)
        out_list.append(lines[i][start:end])
        i += 1
    return out_list


if __name__ == '__main__':
    ' Run file_2_list() from command line '
    import sys
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
    else:  # ask for file names from terminal
        input_file = input('Imput file name: ')

    iwfm.file_test(input_file)

    out_list = file_2_list(input_file)

    print(f'  From {input_file} read:\n{out_list}')

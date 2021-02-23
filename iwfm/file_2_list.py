# file_2_list.py
# Converts a portion of a text file to a list of file lines
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


def file_2_list(filename, slice_end=0, slice_start=0, skip=0):
    """Function file_2_list(filemane,slice_end = 0,slice_start = 0,skip=0) reads a
    text file,  and returns it as a list of file lines. Optionally, it can be a
    slice of each line.
    Header lines can also be skipped."""
    with open(filename, "r") as inputfile:
        lines = inputfile.read().splitlines()
    out_list = []  # create an empty list
    i = skip  # counter
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


if __name__ == "__main__":
    " Run vic_2_table() from command line "
    import sys
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
    else:  # ask for file names from terminal
        input_file = input("Imput file name: ")

    iwfm.file_test(input_file)

    out_list = file_2_list(input_file, slice_end=10, slice_start=20)

    print("  {}".format(out_list))  # update cli

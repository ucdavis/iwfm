# iwfm_lu2sub.py
# Read IWFM element file and land use files for a submodel and write out
# new land use files for the submodel
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


def iwfm_lu2sub(
    elem_file, lu_file, out_file, skip=4, verbose=False, per_line=6):
    """ iwfm_IWFM_lu2sub() - Reads an IWFM Preprocessor Element File for a 
        submodel and an IWFM Land Use File for the base model, and writes 
        a new land use file with land use for only the elements in the 
        Elements File.

    Parameters:
      elem_file       (str):  Submodel IWFM Preprocessor Element file
      lu_file         (str):  Base model land use area file
      out_file        (str):  Submodel land use area file (output)
      skip            (int):  Number of non-comment lines to skip in eac file
      per_line        (int):  If verbose==True, number of items to write per 
                                line to the console
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing
    """
    import sys, re, os
    import iwfm as iwfm

    # -- test that the input files exist
    iwfm.file_test(elem_file)
    iwfm.file_test(lu_file)

    # -- read element file
    elem_ids, _ = iwfm.iwfm_read_elements(
        elem_file
    )  # read element info
    elem_ids.sort()

    # -- read land use file
    lu_lines = open(lu_file).read().splitlines()  # open and read input file
    line_index = 0  # start at the top
    line_index = iwfm.skip_ahead(line_index, lu_lines, 4) # skip comments
    header = line_index

    outport = iwfm.Unbuffered(sys.stdout)  # to write unbuffered output to console
    out_lines, print_count = [], 0
    while line_index < len(lu_lines):
        out = []
        this_line = lu_lines[line_index].split()
        if re.search('/', lu_lines[line_index]):  # catch date
            this_date = this_line.pop(0)

            if verbose:  # write progress to console
                if print_count > per_line - 2:
                    outport.write(' ' + this_date[:10])
                    print_count = 0
                else:
                    if print_count == 0:
                        outport.write('\n  ' + this_date[:10])
                    else:
                        outport.write(' ' + this_date[:10])
                    print_count += 1

        # -- build the output line
        if int(this_line[0]) in elem_ids:
            if int(this_line[0]) == elem_ids[0]:  # first element -> add date
                out.append(this_date)
            for j in range(0, len(this_line)):  # add the rest of the line
                out.append('\t' + this_line[j])
            out_lines.append(out)
        line_index += 1
    outport.write('\n')

    with open(out_file, 'w') as f:
        for i in range(0, header):  # copy top of input file to output
            f.write(lu_lines[i])
            f.write('\n')
        for i in range(0, len(out_lines)):
            this_line = out_lines[i]
            for j in range(0, len(this_line)):
                f.write(this_line[j])
            f.write('\n')
    return len(out_lines)


if __name__ == "__main__":
    " Run iwfm_lu2sub() from command line "
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        elem_file = sys.argv[1]
        lu_file = sys.argv[2]
        out_file = sys.argv[3]

    else:  # ask for file names from terminal
        elem_file = input('IEFM Element file name: ')
        lu_file   = input('IWFM land use file name: ')
        out_file  = input('Output file name: ')

    iwfm.file_test(elem_file)
    iwfm.file_test(lu_file)

    idb.exe_time()  # initialize timer
    iwfm_lu2sub(elem_file, lu_file, out_file, verbose=True)

    idb.exe_time()  # print elapsed time

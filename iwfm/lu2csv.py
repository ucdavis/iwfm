# lu2csv.py
# Read IWFM land use file and write to a csv file
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


def lu2csv(inFileName, skip=4, verbose=False):
    ''' lu2csv() - Read an IWFM land use file and write to a csv file

    Parameters
    ----------
    inFileName : str
        base name of output files

    skip : int, default=4
        number of non-comment lines to skip in eac file

    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing
    '''
    import csv, os
    comments = 'Cc*#'

    outFileName = os.path.splitext(inFileName)[0] + '.csv'
    year, month, day = 0, 0, 0

    # -- read land use file ------------------------------------
    with open(inFileName, 'r') as inFile:
        with open(outFileName, 'w', newline='') as outFile:
            outWriter = csv.writer(outFile)
            count = 0
            line = inFile.readline()  # read input file
            while len(line) > 0:
                if line[0] not in comments:  # skip lines that begin with comment char
                    if skip > 0:
                        skip = skip - 1
                    else:
                        items = line.split()
                        if '/' in items[0]:  # contains a date, change dates
                            month = items[0][0:2]
                            day = items[0][3:5]
                            year = items[0][6:10]
                            items.pop(0)
                        # insert date (year, month, day)
                        items.insert(0, day)
                        items.insert(0, month)
                        items.insert(0, year)
                        # write it out
                        outWriter.writerow(items)
                        count = count + 1
                line = inFile.readline()  # read next line from input file

    if verbose:
        print(f'  {count:,} lines from {inFileName} written to {outFileName}')

    return


if __name__ == "__main__":
    " Run lu2csv() from command line "
    import sys
    import os
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
    else:  # ask for file names from terminal
        input_file = input('IWFM land use file name: ')

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    lu2csv(input_file, verbose=True)

    idb.exe_time()  # print elapsed time

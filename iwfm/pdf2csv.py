# pdf2csv.py
# Read a PDF file and write tables to a csv file
# info and gwhyd_sim columns, and returns the dictionary
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


def pdf2csv(input_file, output_file, verbose=False):
    """ pdf2csv() - Beads a PDF file and writes tables to a csv file

    Parameters:
      input_file      (str):  Name of input PDF file
      output_file     (str):  Name of output csv file
      verbose         (bool): Turn command-line output on or off

    Returns:
      nothing
    """
    import tabula

    tabula.convert_into(input_file, output_file, output_format='csv', pages='all')
    if verbose:
        print(f'  Wrote table(s) in {input_file} to {output_file}')
    return


if __name__ == "__main__":
    " Run pdf2csv() from command line "
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
    else:  # ask for file names from terminal
        input_file = input('PDF file name: ')

    iwfm.file_test(input_file)

    output_file = iwfm.filename_base(input_file) + '.csv'

    idb.exe_time()  # initialize timer
    pdf2csv(input_file, output_file, verbose=True)  
    idb.exe_time()  # print elapsed time

# lu2tables.py
# Read IWFM land use file and write to a separate file for each land use type
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


def lu2tables(land_use_file, verbose=False, debug=0):
    '''lu2tables() - Read an IWFM land use file and write contents to a 
       separate file for each land use type

    *** INCOMPLETE - UNDER DEVELOPMENT ***

    Parameters
    ----------
    land_use_file : str
        name of existing model land use file

    verbose : bool, default=False
        turn command-line output on or off

    debug : bool, default=0
        turn additional command-line output on or off

    Returns
    -------
    nothing

    SUGGESTED FUTURE CHANGES:
      - include option for output file type i.e. type='dat' with options
            like 'csv', 'excel', 'dbf', etc

    '''
    import datetime
    import sys
    import iwfm as iwfm

    # find the base name and extension
    land_use_file_base = land_use_file[0 : land_use_file.find('.')]
    land_use_file_ext = land_use_file[
        land_use_file.find('.') + 1 : len(land_use_file) + 1
    ]

    # -- SUGGESTED FUTURE CHANGES TO IMPROVE THIS PROGRAM --
    # -- read a cl value for output file type
    # -- allow multiple items: pop each item from arvg[] and process it
    # -- may need to add varnames i.e. '-ext=xlsx' or '--excel'
    # out_file_ext = 'dat'                 # default output
    # if len(sys.argv) > 2:                # If there is a value...
    #    cl_value = sys.argv[2]            # Read the debug value from command line
    # if cl_value == 'xls'||'xlsx' then call write_2_excel() to write

    if verbose:
        print(f'  Creating land use area tables from {land_use_file}')  

    file_lines = open(land_use_file).read().splitlines()  # open input file

    # determine how many elements are in this model
    # Check lines starting at the bottom, find first line with length > 5
    # If there's a change something else is at the bottom,
    # then change to either skip_back(n) or test for int
    i = len(file_lines) - 1
    while len(file_lines[i]) < 5:
        i -= 1
    # the first item on this line is the largest element number
    max_elem = int(file_lines[i].split()[0])

    ts_index, elem_index = 0, 0  # time step index, element being parsed
    line_index = iwfm.skip_ahead(0, file_lines, 4)  # skip comment lines

    time_steps = int(
        float(len(file_lines) - line_index) / float(max_elem)
    )  # How many time steps of data?
    dates = ['' for x in range(time_steps)]  # empty list
    crops = (
        len(file_lines[line_index + 3].split()) - 1
    )  # number of crops/land use types
    data = [
        [['0' for z in range(time_steps)] for y in range(max_elem)]
        for x in range(crops)
    ]  # empty array

    # fill the data and years arrays
    while ts_index < time_steps:  # iterate through each time step
        ts_line_index = 0
        while ts_line_index < max_elem:  # iterate through each element
            if debug > 0:
                print(f'Line: {file_lines[line_index]}')
            this_line = file_lines[line_index].split()  # line to list
            if (
                ts_line_index == 0
            ):  # first line has an extra item, the date in DSS format
                date = this_line.pop(0)  # Get the date
                hr = int(date[11:13])  # DSS midnight = '24', datetime midnight = 0
                if hr == 24:
                    hr = 0
                dates[ts_index] = datetime.datetime(
                    int(date[6:10]),
                    int(date[0:2]),
                    int(date[3:5]),
                    hr,
                    int(date[14:16]),
                )
                if debug > 0:
                    sys.stdout.write(dates[ts_index])  # update cli
                    if ts_index + 1 < time_steps:
                        sys.stdout.write(', ')  # update cli
            elem = int(this_line.pop(0))  # pop the element number
            if debug > 1:
                print(f'elem: {elem}')
            for i in range(crops):
                data[i][elem - 1][ts_index] = this_line[
                    i
                ]  # assign values to data array
            ts_line_index += 1
            line_index += 1
            # ----- end of (while ts_line_index) loop -----
        ts_index += 1
        # ----- end of (while ts_index) loop -----

    # write to text files
    iwfm.write_2_dat(land_use_file_base, data, crops, max_elem, time_steps, dates)
    if verbose:
        print(f'  Wrote land use area tables to {land_use_file_base}_*.dat')

    # write to excel workbook
    # write_2_excel(land_use_file_base,data,crops,max_elem,time_steps,dates)
    # if verbose:
    #  print('  Wrote land use area tables to {}.xlsx'.format(land_use_file_base))

    return


if __name__ == '__main__':
    ''' Run lu2tables() from command line 

    SUGGESTED FUTURE CHANGES TO IMPROVE THIS PROGRAM
      - allow multiple items: pop each item from arvg[] and process it

    '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
    else:  # ask for file names from terminal
        input_file = input('IWFM Land use file name: ')

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    lu2tables(input_file, verbose=True)

    idb.exe_time()  # print elapsed time

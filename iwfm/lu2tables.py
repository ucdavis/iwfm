# lu2tables.py
# Read IWFM land use file and write to a separate file for each land use type
# Copyright (C) 2020-2026 University of California
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

def lu2tables(land_use_file, output_file_type, verbose=False, debug=1):
    '''lu2tables() - Read an IWFM land use file and write contents to a 
       separate file for each land use type

    *** INCOMPLETE - UNDER DEVELOPMENT ***

    Parameters
    ----------
    land_use_file : str
        name of existing model land use file

    output_file_type : str
        type of output file to create

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
    land_use_file_ext = land_use_file[land_use_file.find('.') + 1 : len(land_use_file) + 1]

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

    with open(land_use_file) as f:
        file_lines = f.read().splitlines()  # open input file

    # determine how many data lines per time step
    # Check lines starting at the bottom, find first line with length > 5
    # If there's a change something else is at the bottom,
    # then change to either skip_back(n) or test for int
    i = len(file_lines) - 1                         # start at the bottom# last line of file
    while len(file_lines[i]) < 5:                   # find last line with data (skip empty lines)
        i -= 1
    # the first item on this line is the largest element number
    last_data_line_no = i

    # move up the file to a line with a date, counting lines
    no_elems = 1          # currently pointing to last data line
    # while file_lines[i].split()[0] does not contain a digit
    while not any(char.isdigit() for char in file_lines[i][0]):
        i -= 1
        no_elems += 1

    # determine number of time steps and crops
    line_index = iwfm.skip_ahead(0, file_lines, 4)  # skip comment lines
    no_time_steps = int((last_data_line_no - line_index)/no_elems + 1)
    no_crops = (len(file_lines[line_index + 3].split()) - 1)  # number of crops/land use types

    dates = ['' for x in range(no_time_steps)]  # empty list

    # get list of element numbers
    elem_list, ts_line_index, l_index = [], 0, line_index
    while ts_line_index < no_elems:  # iterate through each element
        this_line = file_lines[l_index].split()  # line to list
        if (ts_line_index == 0):  # first line has an extra item, the date in DSS format
            date = this_line.pop(0)  # remove the date
        elem = int(this_line.pop(0))  # get the element number
        elem_list.append(elem)
        ts_line_index += 1
        l_index += 1

    # create empty 3D list for data
    data = [[['0' for z in range(no_time_steps)] for y in range(no_elems)] for x in range(no_crops) ]  # empty array

    ts_index = 0
    # fill the data and years arrays
    while ts_index < no_time_steps:  # iterate through each time step
        ts_line_index = 0
        while ts_line_index < no_elems:  # iterate through each element
            this_line = file_lines[line_index].split()  # line to list
            if (ts_line_index == 0):  # first line has an extra item, the date in DSS format
                import iwfm
                date = this_line.pop(0)  # Get the date
                try:
                    month, day, year, hr, minute = iwfm.validate_dss_date_format(date, f'line {line_index+1} date')
                except ValueError as e:
                    raise ValueError(f"Error parsing DSS date at line {line_index+1}: {str(e)}") from e

                # DSS midnight = '24', datetime midnight = 0
                if hr == 24:
                    hr = 0

                dates[ts_index] = datetime.datetime(year, month, day, hr, minute)
            elem = int(this_line.pop(0))  # pop the element number
            for crop in range(0, no_crops):
                data[crop][ts_line_index][ts_index] = this_line[crop]  # assign values to data array
            ts_line_index += 1
            line_index += 1
            # ----- end of (while ts_line_index) loop -----
        ts_index += 1
        # ----- end of (while ts_index) loop -----

    # write to text files
    crops = [x+1 for x in range(no_crops)]  # integer crop numbers

    if output_file_type == 'csv':
        iwfm.write_2_csv(land_use_file_base, data, crops, elem_list, no_time_steps, dates)
        if verbose:
            print(f'  Wrote land use area tables to {land_use_file_base}_*.csv')
    else:   # default to 'dat'
        iwfm.write_2_dat(land_use_file_base, data, crops, elem_list, no_time_steps, dates)
        if verbose:
            print(f'  Wrote land use area tables to {land_use_file_base}_*.dat')

    # Future: write to excel workbook
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

    output_file_type = 'dat'  # default output file type
    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
        if len(sys.argv) > 2:  # output file tupe listed on command line
            output_file_type = sys.argv[2]
    else:  # ask for file names from terminal
        input_file = input('IWFM Land use file name: ')

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    lu2tables(input_file, output_file_type, verbose=True)

    idb.exe_time()  # print elapsed time

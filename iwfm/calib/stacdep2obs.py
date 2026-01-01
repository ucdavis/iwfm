# stacdep2obs.py
# Convert IWFM Stream Reach Budget to the SMP file format for 
# use by PEST.
# Based on STACDEP2OBS.F90 by Matt Tonkin, SSPA with routines by John Doherty
# Copyright (C) 2020-2024 University of California
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

def process_budget(budget_file, cwidth=12):
    """ process_budget() - Read IWFM Stream Reach budget file and process into
        a table of individual stream reach stream-groundwater flows
        
        Parameters
        ----------        
        budget_file: str
            Name of IWFM Stream Nodes budget file

        cwidth : int, default = 12
                Width of column in budget file

        Returns
        -------
        budget_table, list
            Stream-groundwater flows for each reach

        run_stacdep2obs.sh, list
            List of reach names

        dates, list
            List of dates for budget_table
    """
    import numpy as np

    with open(budget_file) as f:
        budget_lines = f.read().splitlines()

    # How many lines per table? ----------------------------------
    table_len, header_lines, dates = 0, [], []
    while budget_lines[table_len][0] != '-': # skip label lines
        table_len += 1
    table_len += 1                           # top of header
    while budget_lines[table_len][0] != '-': # read header lines
        header_lines.append(budget_lines[table_len])
        table_len += 1
    table_len += 1                           # skip line
    header_len = table_len                   # lines to skip when reading each table
    while len(budget_lines[table_len]) > 10:  # read times
        dates.append(budget_lines[table_len].split()[0].replace("_24:00",""))
        table_len += 1
    table_len += 2                           # padding at end of each table

    # Get reach numbers for tables --------------------------------
    reach_line, reach_list = 1, []           # first reach number, accumulator
    while reach_line < len(budget_lines) - 10:
        reach_list.append(int(budget_lines[reach_line].split()[-1][:-1]))
        reach_line += table_len              # skip to next one

    # Find Stream-Groundwater Column Indexes ----------------------
    i, header_indexes = 0, []
    line = budget_lines[header_len + 3]     # get column widths
    while i < len(line):
        while i < len(line) and line[i] != ' ':
            i += 1
        header_indexes.append(i)
        while i < len(line) and line[i] == ' ':
            i += 1
    # find index of each instance of 'Gain from GW' 
    i, loc, hline = 0, [], budget_lines[3] # header line
    while i < len(hline):
        if hline[i:i+cwidth] == 'Gain from GW':
            loc.append(i)
        i += 1
    stac_cols = []
    for item in loc:
        i = 0
        while header_indexes[i] < item:
            i += 1
        stac_cols.append(i)

    # Read budget tables' stream-gw column ---------------------------
    budget_table, table_line = [], 0
    while table_line < len(budget_lines):
        table_line += header_len
        temp = []
        while  len(budget_lines[table_line]) > 1:
            t, t1 = budget_lines[table_line].split(), 0
            for i in stac_cols:
                t1 += float(t[i])    # add inside and outside columns
            temp.append(t1)
            table_line += 1
        temp = np.array(temp)        # convert temp to numpy array
        budget_table.append(temp)
        table_line += 2 # skip empty lines

    return budget_table, reach_list, dates


def read_reaches(reach_file):
    """ read_reaches() - Read list of reaches and stream nodes
        
        Parameters
        ----------        
        reach_file: str
            Name of reach list file

        Returns
        -------
        reaches: list
            Observation names and associates stream reach(es)
    """

    with open(reach_file) as f:
        reach_list = f.read().splitlines()

    reaches = []
    for line in reach_list[3:]: # skip header lines
        if len(line) > 2:
            temp = line.split()
        reaches.append([temp[0],[int(n) for n in temp[2].split(',')]])
    return reaches


def stacdep2obs(budget_table, dates, reaches, nwidth=20):
    ''' sestacdep2obs() - Convert stream-groundwater flows from IWFM Stream Budget 
        to the SMP file format for use by PEST. (Based on STACDEP2OBS.F90 by Matt 
        Tonkin, SSPA with routines by John Doherty.)

    Parameters
    ----------
    budget_table: list
        Numpy arrays of stream-groundwater flows (inside and outside model)for 
        each stream node

    dates: list
        Dates for budget rows
    
    reaches: list
        List of ouput reaches, containing [name, [reach nos]]

    nwidth: int, default = 20
        Width of name column

    Returns
    -------
    stacdep : list 
        Observation values for each reach in smp format

    ins : list 
        Corresponding Pest instructions for smp file

    '''
    import iwfm as iwfm

    # dates to 'MM/DD/YYY'
    smp_dates, ins_dates = [], []
    for date in dates:       # convert date from text m/d/yy to mm/dd/yyyy
        temp = [int(i) for i in date.split('/')]
        smp_dates.append(iwfm.date2text(temp[1],temp[0],temp[2]))
        temp = date.split('/')
        ins_dates.append(f'{temp[0]}{temp[2]}') 

    stacdep, ins = [], []
    for reach in reaches:
        reach_name = iwfm.pad_back(reach[0],nwidth)   # first field
        reach_nums = reach[1]

        # sum the reach values
        budget = budget_table[reach_nums[0]-1]
        if len(reach_nums) > 1:
            for i in range(1, len(reach_nums)):
                budget += budget_table[reach_nums[i]]

        for i in range(len(budget)):
            smp_out = f'{reach_name} {smp_dates[i]}  0:00:00   {budget[i]}' # smp format
            ins_out = f'l1  [{reach[0]}_{ins_dates[i]}]41:56'
            stacdep.append(smp_out)
            ins.append(ins_out)

    return stacdep, ins




if __name__ == "__main__":
    ''' Run stacdep2obs() from command line '''
    verbose=True

    import sys
    import iwfm as iwfm
    import iwfm.debug as idb
  
    if len(sys.argv) > 1:  # arguments are listed on the command line
        budget_file  = sys.argv[1]
        reach_file   = sys.argv[2]
        output_file  = sys.argv[3]
    else:                                                      # ask for file names from terminal
        budget_file   = input("Input Stream Budget file name: ")
        reach_file    = input("Reach list file name.: ")
        output_file   = input("Output SMP file name: ")

    iwfm.file_test(budget_file)
    iwfm.file_test(reach_file)

    idb.exe_time()  # initialize timer

    # read input files
    budget_table, reach_list, dates = process_budget(budget_file)

    reaches = read_reaches(reach_file)

    # process
    stacdep, ins = stacdep2obs(budget_table, dates, reaches)

    # write results to output smp file
    with open(output_file, 'w') as out_file:
        for item in stacdep:
            out_file.write(f'{item}\n')

    # write results to output ins file
    outins_file = output_file.replace('.smp','.ins')
    with open(outins_file, 'w') as out_file:
        out_file.write(f'pif #\n')
        for item in ins:
            out_file.write(f'{item}\n')

    print(f'\n  Read {budget_file} and wrote {output_file} and {outins_file}.')  # update cli

    idb.exe_time()  # print elapsed time

  
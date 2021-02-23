# vic_2_table.py
# Extract one column from a VIC file to another file
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


def vic_2_table(
    factorsFileName, outFileName, col, per_line=12, verbose=True, debug=False
):
    """vic_2_table() extracts one column from a file of VIC gridded climate
    change factors and writes to a table, with one column for each VIC
    grid ID and one row for each date

    Parameters:
      factorsFileName (str):  Name of VIC factors file
      outFileName     (str):  Name of output file
      per_line        (ints): 1 = Precipitation, 2 = Evapotranspiration
      verbose         (bool): Turn command-line output on or off
      debug           (bool): Turn additional command-line output on or off

    Returns:
      nothing

    """
    import sys
    import iwfm as iwfm

    if (col != 0) and (col != 1):
        print(f'   * vic_2_table(): P-ET of {col} is not acceptable. *')
        print(f'   * P-ET value must be \'0\' for \'P\' or \'1\' for \'ET\'  *')
        print(f'   * Exiting...                                      *')
        import sys

        sys.exit()

    factors = open(factorsFileName).read().splitlines()  # get climate thance gactors
    if verbose:
        print('  Read {:,} lines from {}'.format(len(factors), factorsFileName))

    VIC_Step = 0  # determine no lines for each VIC Grid ID
    if debug:
        print(
            '  ==> VIC_Step: {}, factors[{}]: {}'.format(
                VIC_Step, VIC_Step + 1, factors[VIC_Step + 1]
            )
        )
    ID = int(factors[VIC_Step + 1].split(',')[0])
    first = ID
    while ID == first:
        VIC_Step += 1
        ID = int(factors[VIC_Step + 1].split(',')[0])
    VIC_No = int(len(factors) / VIC_Step)
    if verbose:
        print('  {:,} VIC grid cells, {:,} time steps'.format(VIC_No, VIC_Step))

    VIC_dict = {}  # process input file once for VIC Grid IDs
    VIC_Grid_IDs = []
    j = 1
    for i in range(1, len(factors), VIC_Step):
        temp = factors[i].split(',')
        ID = int(temp[0])
        key, values = ID, j
        VIC_dict[key] = values
        VIC_Grid_IDs.append(ID)
        j += 1
    VIC_IDs_sorted = sorted(VIC_Grid_IDs)

    dates = []  # process data for one VIC Grid ID to get dates
    for i in range(0, VIC_Step):
        temp = factors[i + 1].split(',')
        dates.append(temp[1].replace(' 0:00:00', ''))

    # -- process the file
    # this is messy, but it's a one-off so not (yet) worth the time to make it nice
    outport = iwfm.Unbuffered(sys.stdout)  # to write unbuffered output to console
    print_count = 0
    factor_array = []
    line = 1  # current index in factors
    items = factors[line].split(',')  # starting data
    while line < len(factors) and len(factors[line]) > 5:
        # build lists for one VIC Grid No
        temp = []
        VIC_this = int(items[0])

        if verbose > 1:  # write progress to console
            out = iwfm.pad_front(VIC_this, 5, ' ')
            if print_count > per_line - 2:
                outport.write(', ' + out)
                print_count = 0
            else:
                if print_count == 0:
                    outport.write('\n  ' + out)
                else:
                    outport.write(', ' + out)
                print_count += 1

        while int(items[0]) == VIC_this:
            temp.append(items[col].replace('000000000000', ''))  # parse one line
            line += 1  # get data from the next line
            if line < len(factors) and len(factors[line]) > 10:
                items = factors[line].split(',')  # get data from next line
            else:
                items[0] = -1  # force loop exit
        factor_array.append(
            temp
        )  # done with this VIC Grid ID, add info to list factor_array
    if verbose > 1:  # write progress to console
        outport.write('\n')
    factors = []  # clear memory

    with open(outFileName, 'w') as out_file:  # write to output file
        if verbose:
            print(f'  Opened {outFileName} for output')
        header = 'Date'  # build output file header
        for i in range(1, max(VIC_dict, key=int)):
            header = header + ',' + str(i)
        out_file.write('{}\n'.format(header))  # write output file header
        if debug:
            print('\n  ==> header: {}'.format(header))
        for i in range(0, VIC_Step):  # write data to output file by rows
            data = dates[i]
            for j in range(1, max(VIC_dict, key=int)):  # cols
                data = (
                    data + ',' + factor_array[VIC_dict[j] - 1][i]
                )  # .replace('0000000000,',',').replace('000,',',').replace('00,',',').replace('0,',',')
            if debug:
                print('\n  ==> data: {}'.format(data))
            out_file.write('{}\n'.format(data))
        out_file.write('\n')

    if verbose:
        print(f'  Wrote results to {outFileName}\n')
    return


if __name__ == "__main__":
    """ Run vic_2_table() from command line """
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        factorsFileName = sys.argv[1]
        output_file = sys.argv[2]
        item = int(sys.argv[3])
    else:  # ask for file names from terminal
        factorsFileName = input('P-ET factor file name: ')
        output_file    = input('Output file name: ')
        item           = int(input('Input 0 for Precipitation, 1 for Evapotranspiration: '))

    iwfm.file_test(factorsFileName)

    idb.exe_time()  # initialize timer
    vic_2_table(factorsFileName, output_file, item)

    print(f'  Read {factorsFileName} and wrote {output_file}.')  # update cli
    idb.exe_time()  # print elapsed time

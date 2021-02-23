# iwfm_precip_adj.py
# Read IWFM precipitation file, list of VIC cells and VIC adjustment factors
# and write adjusted precipitation file
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


def iwfm_precip_adj(
    precip_filename,
    elem_VIC_filemane,
    factors_filename,
    years_filename,
    out_filename,
    verbose=False,
    per_line=6,
    debug=0,
):
    """iwfm_precip_adj() reads an IWFM precipitation file, list of VIC grid cells for each precipitation column,
    and table of monthly adjustment factors for each VIC grid cell, and writes out an IWFM precipitation file
    with precipitation rates adjusted by the VIC factors

    Parameters:
      precip_filename   (str):  Name of existing IWFM precipitation file
      elem_VIC_filemane (str):  Name of file linking model elements to VIC elements
      factors_filename  (str):  Name of file with VIC factors
      years_filename    (str):  Name of file with replacement years
      out_filename      (str):  Name of output IWFM precipitation file
      verbose           (bool): Turn command-line output on or off
      per_line          (str):  If verbose==True, number of items to write to CLI per line
                                  (read but ignored if verbose==False)
      debug             (bool): Turn additional command-line output on or off

    Returns:
      nothing

    """
    import re, sys
    import numpy as np
    import iwfm as iwfm

    skip = 5  # skip 5 non-comment lines before reaching data lines

    # -- read precip column-VIC grid linkage ------------------------
    vic_precip = (
        open(elem_VIC_filemane).read().splitlines()
    )  # data: precip col -> region, VIC ID
    vic_precip.pop(0)  # remove header lines
    vic_rows = len(vic_precip)

    vic_dict = {}
    for item in vic_precip:
        item = re.split(';|,|\t', item)
        vic_dict[int(item[0])] = [int(item[1]), item[2]]
    if verbose:
        print('  Read VIC grid data for {:,} precipitation columns'.format(vic_rows))

    if debug > 0:  # write out the dictionary
        with open('test_vic_dict.txt', 'w') as tf:
            for i in range(1, max(vic_dict)):
                if i in vic_dict:
                    tf.write('{}\t{}\n'.format(i, vic_dict[i]))
                else:
                    tf.write('{}\t-1\n'.format(i))
        print('  Wrote VIC list to test_vic_dict.txt')

    # -- get the climate factors ------------------------------------
    factors = open(factors_filename).read().splitlines()  # open and read input file

    # create a dictionary for VIC cell -> column from the first line
    vic_list = re.split(';|,|\t', factors[0])  # VIC cell for each column
    vic_list = [int(x) for x in vic_list[1:]]
    index_list = list(range(0, len(vic_list) + 1))
    d_factor_col = dict(zip(vic_list, index_list))  # return VIC grid ID -> column

    d_factors = {}
    vic_years = []
    factors.pop(0)  # remove header row
    fac_len = len(factors)
    i = 0
    while i < len(factors) and len(factors[i]) > 1:  # put factors into a dictionary
        factor = re.split(';|,|\t', factors[i])
        mm, dd, yy = re.split('/', factor[0])
        month = str(yy) + '-' + str(mm)
        if yy not in vic_years:
            vic_years.append(yy)  # list of calendar years with factors
        factor = [float(x) for x in factor[1:]]
        d_factors[month] = factor
        i += 1

    # -- replacement years for years without VIC factors ------------
    rep_years = open(years_filename).read().splitlines()  # open and read input file

    d_repyr_col = {}  # region name -> column
    rep_list = rep_years[0].split(',')
    for i in range(1, len(rep_list)):
        d_repyr_col[rep_list[i]] = i - 1

    # create a dictionary of all years and replacement years for missing VIC years
    rep_years.pop(0)  # remove header line
    d_VICyear = {}
    for year in rep_years:
        item = re.split(';|,|\t', year)
        item = [int(x) for x in item]
        d_VICyear[item[0]] = item[1:]

    # -- read IWFM precipitation file ------------------------------------
    precip = open(precip_filename).read().splitlines()  # open and read input file

    of = open(out_filename, 'w')  # open output file for copy of header info

    # find line with first data set, get month and year
    pline, status = 0, 1  # pline = line being processed, continue until status < 1
    while status > 0:
        if precip[pline][0] == 'C':  # skip lines that begin with 'C', 'c' or '*'
            of.write(precip[pline] + '\n')
            pline += 1
        elif precip[pline][0] != 'C':
            if skip > 0:  # also handle the other header lines
                of.write(precip[pline] + '\n')
                skip -= 1
                pline += 1
            else:
                items = precip[pline].split()
                pmonth = int(items[0][0:2])
                pyear = int(items[0][6:10])
                cols = len(items)
                status = 0
    if verbose:
        print(f'  Precipitation start date: {pmonth}/{pyear}')

    # -- do the work -------------------------------------------------
    if verbose:
        print(
            '  Processing {:,} precipitation dates...'.format(len(precip) - pline - 1)
        )

    if debug > 1:
        verbose = False

    if verbose:  # create outport to write unbuffered output to console
        outport = iwfm.Unbuffered(sys.stdout)

    print_count = 0
    with open(
        'factors.dat', 'w'
    ) as factfile:  # write out the factors to a separate file just in case...
        header = 'Date        '
        for i in range(1, cols):
            header = header + str(i) + '   '
        header += '\n'
        factfile.write(header)

        # process each row of the precipitation file, replacing adjusted values
        while pline < len(precip) and len(precip[pline]) > 10:
            items = precip[pline].split()
            date = items[0].replace('_24:00', '')

            if verbose:  # write progress to console
                if print_count > per_line - 2:
                    outport.write(' ' + date)
                    print_count = 0
                else:
                    if print_count == 0:
                        outport.write('\n  ' + date)
                    else:
                        outport.write(' ' + date)
                    print_count += 1

            p = [
                float(x) for x in items[1 : vic_rows + 1]
            ]  # list of precip values to midify

            mm, dd, yy = re.split('/', date)
            repyr = []
            if yy not in vic_years:  # use replacement years
                y = int(yy)
                if int(mm) > 9:
                    y += 1  # bump up to water year
                repyr = d_VICyear[y]

            f = []
            for e in range(1, vic_rows + 1):  # cycle through precip columns

                vic_id = vic_dict[e][0]  # element -> VIC_ID
                column = d_factor_col[vic_id]  # VIC_ID -> factor column
                if len(repyr) == 0:  # use the input data date
                    month = str(yy) + '-' + str(int(mm))
                else:  # get the substitute date
                    region = vic_dict[e][1]
                    yy = repyr[d_repyr_col[region]]
                    month = str(yy) + '-' + str(int(mm))
                f.append(d_factors[month][column])  # factor of element
            new_p = np.round(np.array(p) * np.array(f), 2)

            out_str = items[0]
            for i in new_p:
                out_str = out_str + '\t' + str(i)
            of.write(out_str + '\n')

            pline += 1
    of.close()

    if verbose:  # write progress to console
        outport.write('\n')
        print(f'\n  Wrote adjusted precipitation rates to {out_filename}\n')
    return


if __name__ == '__main__':
    ' Run iwfm_precip_adj() from command line '
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        precip_filename = sys.argv[1]
        elem_VIC_filemane = sys.argv[2]
        factors_filename = sys.argv[3]
        years_filename = sys.argv[4]
        out_filename = sys.argv[5]

    else:  # ask for file names from terminal
        precip_filename   = input('IWFM Precipitation file name: ')
        elem_VIC_filemane = input('Element-VIC file name: ')
        factors_filename  = input('Factors file name: ')
        years_filename    = input('Years file name: ')
        out_filename      = input('Output file name: ')

    iwfm.file_test(precip_filename)
    iwfm.file_test(elem_VIC_filemane)
    iwfm.file_test(factors_filename)
    iwfm.file_test(years_filename)

    idb.exe_time()  # initialize timer
    iwfm_precip_adj(
        precip_filename,
        elem_VIC_filemane,
        factors_filename,
        years_filename,
        out_filename,
        verbose=True,
        debug=0,
    )  # set debug=1 to debug

    idb.exe_time()  # print elapsed time

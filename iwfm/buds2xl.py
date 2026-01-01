# buds2xl.py
# Read information from an IWFM Budget.in file and write output to 
# an Excel file (perhaps in future also to csv file or other type of file)
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


def buds2xl(bud_file, type='xlsx', verbose=False):
    ''' buds2xl() - Read IWFM Budget.in file and write output to an Excel
        or csv file
    Parameters
    ----------
    bud_file : string
        IWFM Budget.in file name
            
    type : string, default='xlsx'
        Output file style
            
    verbose : bool, default=False
        Turn command-line output on or off
            
    Returns
    -------
    nothing

    '''

    import os
    import iwfm
    import iwfm.hdf5 as hdf5
    import iwfm.xls as xl
        
    budget_list, factors = iwfm.iwfm_read_bud(bud_file, verbose=verbose)  # read budget file
    nbudget, factlou, unutlou, factarou, unitarou, factvolou, unitvolou, bdt, edt = factors

    if verbose: print(f'   {nbudget} budgets found in {bud_file}')

    if type=='xlsx':
        excel = xl.excel_init()     # initialize Excel

    for budget in range(nbudget):
        hdffile, outfile, intprnt, nlprint, lprint = budget_list[budget]
        if verbose: print(f'   Processing {hdffile}')

        budget_data   = hdf5.get_budget_data(hdffile, 
                                area_conversion_factor=factarou, 
                                volume_conversion_factor=factvolou, 
                                length_units=unutlou,
                                area_units=unitarou,
                                volume_units=unitvolou,
                                verbose=verbose) # (loc_names, column_headers, loc_values, titles)

        if type=='xlsx':   # default type is Excel
            workbook = xl.excel_new_workbook(excel)             # create new Excel workbook

            xl.write_budget_to_xl(workbook, budget_data)        # write budget data to Excel workbook

            xlfile = outfile[:outfile.index('.bud')] + '.xlsx'  # Excel file name

            workbook.SaveAs(os.path.abspath(xlfile))            # save workbook
            workbook.Close(True)

        elif type=='csv':     # for future use?
            pass

        else:
            pass


    if type=='xlsx':
        xl.excel_kill(excel)
                         




if __name__ == '__main__':
    ' Run from command line '
    import sys
    import iwfm
    import iwfm.debug as idb
 
    if len(sys.argv) > 1:  # arguments are listed on the command line
        bud_file = sys.argv[1]

    else:  # ask for file names from terminal
        bud_file = input('IWFM Budget file name: ')
        print('')

    idb.exe_time()  # initialize timer

    buds2xl(bud_file, verbose=True)

    idb.exe_time()  # print elapsed time




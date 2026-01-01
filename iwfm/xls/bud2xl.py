# bud2xl.py
# Read IWFM Budget or Z-Budget output file and paste into existing Excel workbook
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


def bud2xl(budget_file, excel_file, verbose=False, row = 6):
    ''' bud2xl() - Read IWFM Budget or Z-Budget output file and paste into 
        existing Excel workbook

    Parameters
    ----------
    budget_file : str
        Name of IWFM Budget output file

    excel_file : str
        Name of existing Excel file

    verbose : bool, default=False
        Turn command-line output on or off

    row : int, default=6
        Rop row of table data in excel spreadsheets

    Returns
    -------
    nothing
    '''
    import os
    import iwfm as iwfm
    import win32com.client as win32  # pywin32

    cwd = os.getcwd()

    # -- read the Budget file into array file_lines
    with open(budget_file) as f:
        file_lines = f.read().splitlines() 
    file_lines = [word.replace('_24:00', ' ') for word in file_lines]

    # -- Get the Budget file header and footer info
    header, footer, table, line = 0, 0, 1, 0
    while not file_lines[line][0].isdigit():  
        line += 1
        header += 1
    line += 1
    while  line < len(file_lines) and file_lines[line][0].isdigit():  
        line += 1
        table += 1
    line += 1

    if line + 5 < len(file_lines):  
        while (
            len(file_lines[line]) == 0 or not file_lines[line][0].isdigit()
        ):  
            line += 1
            footer += 1
    footer += 1
    footer -= header
    tables = round(
        len(file_lines) / (header + table + footer)
    )  
    if verbose:
        print(f'  Read {tables} tables from {budget_file}')

    # -- Open the excel workbook
    excel = win32.gencache.EnsureDispatch('Excel.Application')  
    excel.DisplayAlerts = False  
    wb = excel.Workbooks.Open(cwd + '\\' + excel_file)  
    if verbose:
        print(f'  Opened {excel_file}')

    # -- If there are too few worksheets, add some
    if wb.Sheets.Count < tables + 1:
        print(f'=> {tables} tables for {wb.Sheets.Count} worksheets in {excel_file}')
        print(f'=> Adding {tables - wb.Sheets.Count + 1} worksheets to {excel_file}')
        for i in range(wb.Sheets.Count,tables + 1):
            wb.Worksheets.Add(After=wb.Worksheets(wb.Sheets.Count))
    
    # -- Step through the Budget file, one table at a time
    line = 0  
    for t in range(0, tables):  
        line += header  
        budget_data = []
        for _ in range(table):
            lines = file_lines[line].split()
            budget_data.append(lines)
            line += 1
        line += footer  
        # -- write to excel worksheet
        ss = wb.Worksheets(t + 2)  
        ss.Range(
            ss.Cells(row, 1), ss.Cells(row + len(budget_data) - 1, len(list))
        ).Value = budget_data  
        budget_data.clear()  

    wb.SaveAs(cwd + excel_file) 

    excel.DisplayAlerts = False  # return to defaults
    #excel.Visible = False
    #excel.Application.Quit()  
    #excel = None
    if verbose:
        print(f'  Closed {excel_file}')
    


if __name__ == '__main__':
    ' Run bud2xl() from command line '
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        budget_file = sys.argv[1]
        excel_file = sys.argv[2]

    else:  # ask for file names from terminal
        budget_file = input('IWFM Budget file name: ')
        excel_file  = input('Output Excel file name: ')

    iwfm.file_test(budget_file)
    iwfm.file_test(excel_file)

    idb.exe_time()  # initialize timer
    bud2xl(budget_file, excel_file, verbose=True)

    idb.exe_time()  # print elapsed time

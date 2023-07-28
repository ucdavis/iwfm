# write_budget_to_xl.py
# write IWFM Budget data to an Excel workbook
# Copyright (C) 2020-2023 University of California
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

def write_budget_to_xl(wb, budget_data):
    ''' write_budget_to_xl() - write IWFM Budget data to an Excel workbook

    Parameters
    ----------
    workbook : Excel workbook COM object
        Output Excel file open for writing

    budget_data: list 
        List contains four lists:
            loc_names : list of strings
                Location names (subregion, stream reach, stream node, small watershed etc)
        column_headers : list of lists of strings
            Column headers for each location
        loc_values : list of dataframes
            Each dataframe contains values for one location
        titles : list
            Titles (3 items) for each location
    
    Returns
    -------
    nothing

    '''
    import sys
    loc_names, column_headers, loc_values, titles = budget_data[0], budget_data[1], budget_data[2], budget_data[3]

    loc_type = titles[0][1].split()[0]  # location type: 'GROUNDWATER', 'LAND' etc; future use



    for loc in range(len(loc_names)):

        # add a new worksheet to the workbook after last sheet
        ws = wb.Sheets.Add(Before = None , After = wb.Sheets(wb.Sheets.count))

        ws.Name = loc_names[loc]        # give new worksheet a name

        # location info to top of sheet
        for i in range(len(titles[loc])):
            ws.Cells(i+1,1).Value = titles[loc][i]

        # column headers to row 5
        for i in range(len(column_headers[loc])):
            ws.Cells(5,i+1).Value = column_headers[loc][i]

        # convert time stamp to string and place in column 1, rows 6 to end
        for i in range(loc_values[loc].shape[0]):
            ws.Cells(i+6,1).Value = loc_values[loc].iloc[i,0].strftime('%m/%d/%Y')

        # place values for columns 2 to end and rows 6 to end as array
        col = chr(ord("@")+loc_values[loc].shape[1])    # works because never >25 columns or would need to go to two letters
        row = 5 + loc_values[loc].shape[0]
        ws.Range("B6", f"{col}{row}").Value = loc_values[loc].iloc[:,1:].values

        # format cells
        ws.Range("A6", f"A{row}").NumberFormat = "MM/DD/YYYY"       # format cells, column 1: date MM/DD/YYYY format
        ws.Range("B6", f"{col}{row}").NumberFormat = "#,##0.00"     # column 2 to end: number with 2 decimal places and comma separator
        ws.Range("A1", f"{col}5").Font.Bold = True                  # row 5: bold and center and wrap text
        ws.Range("A5", f"{col}5").HorizontalAlignment = 3           # row 5: center
        ws.Range("A5", f"{col}5").WrapText = True                   # row 5: wrap text
        ws.Range("A5", f"{col}5").VerticalAlignment = 2             # row 5: vertical center

        # set column widths
        for i in range(1,36):
            ws.Columns(i).ColumnWidth = 14

    return


# xl_write_2d.py
# Writes 2D array to excel workbook
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


def xl_write_2d(output, wb, row=1, col=1, sheet=0):
    '''xl_write() - Write a 2D array to an existing excel workbook

    Parameters
    ----------
    output : list
        2D array of data
    
    wb : obj
        Excel workbook object
    
    row : int
        top column of write area
    
    col : int
        left column of write area
    
    sheet : int
        worksheet number to write to

    Returns
    -------
    nothing
    
    '''
    ss = wb.Worksheets(sheet)  # select the worksheet for this table
    # paste in
    ss.Range(ss.Cells(row, 1), ss.Cells(row + len(output) - 1, len(output[0]))
        ).Value = output  
    return

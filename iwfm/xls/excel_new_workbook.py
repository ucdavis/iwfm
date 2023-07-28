# excel_new_workbook.py
# open a new Excel workbook with one sheet
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

def excel_new_workbook(excel):
    ''' excel_new_workbook() - open a new Excel workbook with one sheet
    
    Parameters
    ----------
    excel : COM object
        Excel application object

    Returns
    -------
    workbook : Excel workbook COM object
        Output Excel file open for writing
    
    '''

    workbook = excel.Workbooks.Add()

    return workbook


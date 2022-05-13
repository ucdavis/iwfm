# xl_open.py
# Opens an excel workbook
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


def xl_open(excel_file):
    ''' xl_open() - Open an excel workbook

    Parameters
    ----------
    excel_file : str
        name of existing Excel file

    Returns
    -------
    excel workbook object
    
    '''
    import win32com.client as win32  # pywin32

    # Open the excel workbook
    excel = win32.gencache.EnsureDispatch('Excel.Application')  # create an excel object
    excel.DisplayAlerts = False  # no warning when overwriting a file
    excel.Visible = False
    # open the excel workbook
    wb = excel.Workbooks.Open(os.path.join(os.getcwd(), excel_file))
    return wb

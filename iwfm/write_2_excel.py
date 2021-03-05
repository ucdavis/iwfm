# write_2_excel.py
# Writes a 3D array as 2D tables (row=elements x col=time_steps)
# to an excel workbook with sheets # of worksheets
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


def write_2_excel(file_base_name, data, sheets, elements, time_steps, dates, data_type='Crop'):
    """ write_2_excel() - Write a 3D array as 2D tables (row=elements
    x col=time_steps) to an excel workbook with sheets # of worksheets

    Parameters:
      file_base_name (str):   Base name of output file
      data           (list):  Data to be written
      sheets         (int):   Number of sheets
      elements       (list):  Model element numbers
      time_steps     (int):   Number of time steps
      dates          (list):  Dates corresponding to time steps
      data_type      (str):   Type of information

    Returns:
      nothing

    """
    import xlsxwriter

    # Create an Excel writer using XlsxWriter as the engine.
    wkbkname = ''.join([file_base_name, '.xlsx'])
    workbook = xlsxwriter.Workbook(wkbkname)
    worksheets = ['' for x in range(sheets)]  # empty list
    # write to the workbook
    for i in range(sheets):
        worksheets[i] = workbook.add_worksheet(
            ''.join([data_type, str(i + 1)])
        )  # Create a worksheet and name it
        worksheets[i].write(0, 0, ''.join([data_type, str(i + 1)]))  # header label
        worksheets[i].write(1, 0, 'WYr')  #  write header row
        for k in range(time_steps):  # write dates in first column
            worksheets[i].write(1, k + 1, int(dates[k].year))
        for j in range(elements):  # write data
            worksheets[i].write(j + 2, 0, j + 1)
            for k in range(time_steps):
                worksheets[i].write(j + 2, k + 1, float(data[i][j][k]))
    workbook.close()
    return

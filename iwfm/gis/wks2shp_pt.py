# wks2shp_pt.py
# Reads an Excel workbook and creates a POINT shapefile
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


def wks2shp_pt(inwksheet, outshp, sheet_index=0):
    ''' wks2shp_pt() - Read an Excel workbook and create a POINT shapefile

    Parameters
    ----------
    inwksheet : str
        Excel workbook name
    
    outshp : str
        output shapefile name
    
    sheet_index : int, default=0
        Sheet number in workbook

    Returns
    -------
    nothing

    '''
    import xlrd
    import iwfm as iwfm

    xls = xlrd.open_workbook(inwksheet)  # open Excel workbook
    sheet = xls.sheet_by_index(sheet_index)  # select worksheet

    w = iwfm.gis.shp_get_writer(outshp, POINT)  # open shapefile writer

    for i in range(sheet.ncols):  # move data to shapefile table
        w.field(str(sheet.cell(0, i).value), "C", 40)  # read the header row

    for i in range(1, sheet.nrows):
        values = [sheet.cell(i, j).value for j in range(sheet.ncols)]
        w.record(*values)

        # get lat, lon from last two columns
        w.point(float(values[-2]), float(values[-1]))
    w.close
    return

# budget_info.py
# Get the Budget file header and footer length and number of tables 
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


def budget_info(budget_lines):
    ''' budget_info() - Get the Budget file header and footer length and number of tables 

    Parameters
    ----------
    budget_lines : list of str
        contents of IWFM Budget file


    Returns
    -------
    tables : int
        number of tables in the busget file

    header : int
        number of header lines in each table

    footer : int
        number of footer lines in each table

    '''

    header, footer, table, line = 0, 0, 1, 0
    while not budget_lines[line][0].isdigit() :                   # reads to end of header
        header += 1                                               # to get header length
        line   += 1
    line += 1

    width, i = 0, 16                                              # get field width, width of DSS date
    while budget_lines[line][i+width].isspace():                  # count spaces
        width += 1
    while not budget_lines[line][i+width].isspace():              # count digits, decimal etc
        width += 1

    while budget_lines[line][0].isdigit():                        # reads to end of dates
        table += 1                                                # to get table length
        line  += 1
        lines += 1
    line += 1

    if line + 5 < len(budget_lines):                              # budget file contains more than one table
        while len(budget_lines[line])==0 or not budget_lines[line][0].isdigit():     # reads to end of next header
            footer += 1
            line   += 1
    footer = footer + 1 - header                                  # to get footer length
    tables = round(len(budget_lines)/(header + table + footer))   # number of tables in budget file

    return tables, header, footer

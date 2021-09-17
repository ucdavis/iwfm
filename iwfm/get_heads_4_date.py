# get_heads_4_date.py
# Read headall.out file and return heads for a specific date
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


def get_heads_4_date(heads_file, out_date, start=5):
    ''' get_heads_4_date() - Read headall.out file and return heads for a
        specific date 

    Parameters
    ----------
    heads_file : str
        name of IWFM headall.out file
    
    out_date : str
        date in MM/DD/YYYY format
    
    start : int, default=5
        number of header lines to skip

    Returns
    -------
    nothing
    
    '''
    import iwfm as iwfm

    out_mon = iwfm.month(out_date)
    out_day = iwfm.day(out_date)
    out_year = iwfm.year(out_date)

    file_lines = open(heads_file).read().splitlines()  # open and read input file

    line_index = start
    nodes = file_lines[line_index].split()  # read line w/node nos
    nodes.pop(0)  # remove text
    nodes.pop(0)  # remove text

    data = []

    line_index += 1
    item = file_lines[line_index].split()  # read line w/date
    data.append(item)
    end_date = item.pop(0)  # remove the date

    while line_index < len(file_lines) - 1:
        line_index += 1
        layer = 1
        header = []
        header.append('Node')
        header.append('Layer ' + str(layer))
        while file_lines[line_index][0].isspace():  # get all the lines for this time step
            item = file_lines[line_index].split()
            data.append(item)
            layer += 1
            header.append('Layer ' + str(layer))
            line_index += 1
        # now check the date
        m = iwfm.month(end_date[0:10])
        d = iwfm.day(end_date[0:10])
        y = iwfm.year(end_date[0:10])
        if m == out_mon and d == out_day and y == out_year:
            out_table = np.asarray(data)
            return out_table, nodes, header
        else:
            data = []
            data.append(nodes)
            item = file_lines[line_index].split()  # read line w/date
            data.append(item)
            end_date = item.pop(0)  # remove the date

    return

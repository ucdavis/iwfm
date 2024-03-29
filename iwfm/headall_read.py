# headall_read.py
# Read headall.out file and return as lists
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


def headall_read(input_file, skip=5):
    ''' headall_read() - Reads an IWFM HeadAll.out file and returns
        the data as floats, with lists of dates and model nodes and
        the number of model layers

    Parameters
    ----------
    input_file : str
        IWFM HeadAll.out file name
    
    skip : int, default=5
        number of header lines

    Returns
    -------
    data : list
        heads from headall file
    
    layers : int
        number of model layers
    
    dates : list
        simulation time step dates corresponding to data rows
    
    nodes : list
        model nodes corresponding to data columns

    '''
    
    file_lines = open(input_file).read().splitlines() 

    line = skip
    nodes = file_lines[line].split()  
    nodes.pop(0)  
    nodes.pop(0)  

    line += 1
    layers = 1
    while file_lines[line + layers][0] == ' ':
        layers += 1

    data, dates = [], []

    layer = 0
    while line < len(file_lines):
        in_list = file_lines[line].split()  
        if layer == 0:
            date = in_list.pop(0)
            dates.append(date[:10])
        data.append([float(item) for item in in_list])
        line += 1
        layer += 1
        if layer == layers:
            layer = 0
    return data, layers, dates, nodes

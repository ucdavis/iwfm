# iwfm_read_gw.py
# read IWFM simulation groundwater file for file names
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

def get_name(s):
    ''' get_name() - Read an IWFM Simulation Groundwater file and return
        a dictionary of sub-process file names, and arrays of parameters

    Parameters
    ----------
    s : str
        line from IWFM Simulation Groundwater file

    Returns
    -------
    name : string
        if file name: Groundwater sub-process file name
        if blank, 'none'
    '''

    temp = s.split()[0]
    if temp[0] == '/':   # check for presence of file name
        name = 'none'
    else:
        name = temp
    return name


def iwfm_read_gw(gw_file, verbose=False):
    ''' iwfm_read_gw() - Read an IWFM Simulation Groundwater file and return
        a dictionary of sub-process file names, and arrays of parameters

    Parameters
    ----------
    gw_file : str
        IWFM Simulation Groundwater file name

    Returns
    -------
    gw_files : dictionary
        Groundwater sub-process file names

    node_id : list
        node numbers

    layers : int
        number of layers

    Kh : list
        hydraulic conductivity

    Ss : list
        specific storage

    Sy : list
        specific yield

    Kq : list
        horizontal anisotropy ratio

    Kv : list
        vertical anisotropy ratio

    init_cond : list
        initial groundwater heads

    units : list
        time units for Kh, Kv, and Ss

    hydrographs : list
        hydrograph file names

    factxy : float
        (X,Y) scale factor for hydrographs
                
    '''
    import iwfm as iwfm
    import numpy as np
    import re

    iwfm.file_test(gw_file)

    comments, gw_dict = 'Cc*#', {}

    file_lines = open(gw_file).read().splitlines()  

    # get sub-process file names (or 'none' if not present)
    line_index = iwfm.skip_ahead(1, file_lines, 0) 
    gw_dict['bc'] = get_name(file_lines[line_index]) 

    line_index += 1
    gw_dict['tiledrain'] = get_name(file_lines[line_index]) 

    line_index += 1
    gw_dict['pumping'] = get_name(file_lines[line_index]) 

    line_index += 1
    gw_dict['subsidence'] = get_name(file_lines[line_index]) 

    line_index += 10
    gw_dict['headall'] = get_name(file_lines[line_index]) 

    line_index = iwfm.skip_ahead(line_index, file_lines, 7) 
    nouth = int(file_lines[line_index].split()[0])             # number of lines to skip
    factxy = float(file_lines[line_index+1].split()[0])        # (X,Y) scale factor

    line_index = iwfm.skip_ahead(line_index, file_lines, 2)
    gw_dict['gwhyd'] = get_name(file_lines[line_index]) 

    # hydrographs
    line_index = iwfm.skip_ahead(line_index, file_lines, 1)
    hydrographs = []
    for i in range(nouth):
        if re.search(file_lines[line_index].split()[0], comments):
            line_index += 1   # if line starts with comment character, skip it
        hydrographs.append(file_lines[line_index].split()[0])
        line_index += 1
    if verbose: print(f' ==> {gw_file} has {nouth} hydrograph(s)')

    # element face flow - skip
    line_index = iwfm.skip_ahead(line_index, file_lines, 0)             # skip to Element Face Flows
    noutf = int(file_lines[line_index].split()[0])                      # Element Face Flow lines
    if verbose: print(f' ==> {gw_file} has {noutf} face flow line(s)')
    line_index = iwfm.skip_ahead(line_index, file_lines, noutf + 2)     # skip Element Face Flow file name and data

    if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')
    ngroup = int(file_lines[line_index].split()[0])                      # skip to Parameter Groups
    
    if verbose: print(f' ==> {gw_file} has {ngroup} parameter group(s)')

    line_index = iwfm.skip_ahead(line_index, file_lines, 2)             # skip FACTOR lines
    if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')

    # units
    tunitkh = file_lines[line_index].split()[0]                         # time unit for aquifer Kh
    line_index += 1
    if verbose: print(f' ==> {tunitkh=}')
    tunitv = file_lines[line_index].split()[0]                          # time unit for aquitard Kv
    line_index += 1
    if verbose: print(f' ==> {tunitv=}')
    tunitl = file_lines[line_index].split()[0]                          # time unit for aquifer Kv
    units=[tunitkh, tunitv, tunitl]
    if verbose: print(f' ==> {tunitl=}')

    line_index = iwfm.skip_ahead(line_index, file_lines, 1)             # skip to parameter section
    if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')

    if ngroup > 0:                                                      # read parameter grid
        line_index = iwfm.skip_ahead(line_index, file_lines, 1)         # skip model node numbers
        if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')

        nodes = int(file_lines[line_index].split()[0])                  # number of parametric grid nodes
        line_index = iwfm.skip_ahead(line_index, file_lines, 1)         # skip model node numbers
        nep = int(file_lines[line_index].split()[0])                    # number of parametric grid elements
        if verbose: print(f' ==> {nodes=}')
        if verbose: print(f' ==> {nep=}')

        line_index = iwfm.skip_ahead(line_index, file_lines, nep+1)         # skip parametric grid element description
        if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')

        # how many layers?
        layers = 1
        len1 = len(file_lines[line_index].split())                          # includes node number
        len2 = len(file_lines[line_index+1].split())                        # does not include node number unless one layer
        if len2 == len1:
            layers = 1
        else: 
            while len(file_lines[line_index+layers].split()) < len1:
                layers += 1

        if verbose: print(f' ==> {layers=}')
        if verbose: print(f' ==> {nodes=}')

        # initialize parameter arrays
        node_id = [0 for row in range(nodes)]
        x = [0 for row in range(nodes)]
        y = [0 for row in range(nodes)]
        Kh = [[0 for col in range(layers)] for row in range(nodes)]
        Ss = [[0 for col in range(layers)] for row in range(nodes)]
        Sy = [[0 for col in range(layers)] for row in range(nodes)]
        Kq = [[0 for col in range(layers)] for row in range(nodes)]
        Kv = [[0 for col in range(layers)] for row in range(nodes)]

        # read parameter values
        for node in range(nodes):
            for layer in range(layers):
                values = file_lines[line_index].split()
                if layer == 0:
                    node_id[node] = int(values.pop(0))
                    x[node] = int(values.pop(0))
                    y[node] = int(values.pop(0))
                Kh[node][layer] = float(values[0])
                Ss[node][layer] = float(values[1])
                Sy[node][layer] = float(values[2])
                Kq[node][layer] = np.float32(values[3])
                Kv[node][layer] = float(values[4])
                line_index += 1

    else:                                                               # read parameter values
        # how many layers?
        layers = 1
        len1 = len(file_lines[line_index].split())                      # includes node number
        len2 = len(file_lines[line_index+1].split())                    # does not include node number unless one layer
        if len2 == len1:
            layers = 1
        else: 
            while len(file_lines[line_index+layers].split()) < len1:
                layers += 1

        # how many nodes?
        nodes = 0
        while file_lines[line_index+(nodes*layers)].split()[0] != 'C':
            nodes += 1
        nodes -= 1

        # initialize parameter arrays
        node_id = [0 for row in range(nodes)]
        Kh = [[0 for col in range(layers)] for row in range(nodes)]
        Ss = [[0 for col in range(layers)] for row in range(nodes)]
        Sy = [[0 for col in range(layers)] for row in range(nodes)]
        Kq = [[0 for col in range(layers)] for row in range(nodes)]
        Kv = [[0 for col in range(layers)] for row in range(nodes)]

        # read parameter values
        for node in range(nodes):
            for layer in range(layers):
                values = file_lines[line_index].split()
                if layer == 0:
                    node_id[node] = int(values.pop(0))
                Kh[node][layer] = float(values[0])
                Ss[node][layer] = float(values[1])
                Sy[node][layer] = float(values[2])
                Kq[node][layer] = np.float32(values[3])
                Kv[node][layer] = float(values[4])
                line_index += 1

    line_index = iwfm.skip_ahead(line_index, file_lines, 0)       # skip anomaly section
    if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')
    nebk = int(file_lines[line_index].split()[0])                 # anomaly lines
    if verbose: print(f' ==> {nebk=}')
    line_index = iwfm.skip_ahead(line_index, file_lines, nebk+4)  # skip anomaly section and FACTHP

    if verbose: print(f' ==> file_lines[{line_index}] = {file_lines[line_index]}')

    # initial condition
    init_cond = []
    for node in range(nodes):
        temp, items = [], file_lines[line_index].split()
        temp.append(int(items[0]))
        for l in range(layers):
            temp.append(float(items[l+1]))
        init_cond.append(temp)
        line_index += 1
    if verbose: print(' ==> leaving iwfm_read_gw.py <==')

    return gw_dict, node_id, layers, Kh, Ss, Sy, Kq, Kv, init_cond, units, hydrographs, factxy

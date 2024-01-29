# params2gw.py
# Read parameter values for model from an IWFM overwrite file
# and write them to an IWFM Groundwater file
# Copyright (C) 2020-2023 University of California
# Based on a PEST utility written by Matt Tonkin
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


def print_dict(d):
    ''' print_dict() - Print contents of a dictionary, for debugging

    Parameters
    ----------
    d : dict
        Dictionary
    
    Return
    ------
    nothing

    '''

    print('   key\t\tvalue\n')
    for k, v in d.items():
        print(k, v)
    return


def skip_ahead(line_index, all_lines, skip=0):
    ''' skip_ahead() - Increment line_index by skipping (a) every line that 
        begins with 'C', 'c' '*' or '#' and (b) 'skip' additional lines.
        Stop if last line (all_lines) is reached

    Parameters
    ----------
    line_index : int
        current line number
    
    all_lines : list
        each item is one line from a file
    
    skip : int
        number of non-comment lines to skip

    Returns
    -------
    line_index : int
        new current line or -1 if end reached
    
    '''
    skip_lines = skip
    comments = 'Cc*#'
    while skip_lines > 0:
        if line_index >= len(all_lines):
            return -1
        if all_lines[line_index][0] not in comments:  # skip 
            skip_lines -= 1
        line_index += 1
    while all_lines[line_index][0] in comments:  # skip
        line_index += 1
        if line_index > len(all_lines):
            return -1
    return line_index

def pad_front(item, n=1, t=' '):
    ''' pad_front() - Convert item to a string and then add multiple copies
        of text character t before item until the string is n characters long

    Parameters
    ----------
    item : any single item (int, float, string)
        item to be converted to string
    
    n : int
        minimum character length
    
    t : str, default=' '
        character to add to pad string to length

    Returns
    -------
    padded string

    '''
    s = str(item)
    while len(s) < n:
        s = t + s
    return s

def exe_time():
    ''' print_exe_time() - Tracks the time since the first call, and prints
        the elapsed time on subsequent calls 

    Parameters
    ----------
    nothing
    
    Return
    ------
    nothing

    '''
    import datetime

    if not hasattr(exe_time, 'start'):
        exe_time.start = datetime.datetime.now()
        return
    else:
        end = datetime.datetime.now()

        diff = str(end - exe_time.start).split(':')
        secs = str(round(float(diff[2]), 1))
        if int(diff[0]) > 0:
            hours = pad_front(str(int(diff[0])), 2, '0') + ':'
            mins = pad_front(str(int(diff[1])), 2, '0') + ':'
        elif int(diff[1]) > 0:
            hours = ''
            mins = f'{int(diff[1])} min '
            secs += ' sec'
        else:
            hours, mins = '', ''
            secs += ' seconds'
        print(f'  Elapsed time: {hours}{mins}{secs}\n')

def file_test(filename):
    ''' file_test() - Check that the file exists and exit if it does not

    Parameters
    ----------
    filename : str
        file name
    
    Return
    ------
    nothing
    
    '''
    import os
    import iwfm as iwfm

    if not os.path.isfile(filename):  # test that input file exists
        iwfm.file_missing(filename)

# --------------------------------------------------------------------------------



def read_gw_file(gw_file, verbose=False):
    """ read_gw_file - Read an IWFM Groundwater file and return the number of nodes, 
        the scaling factors, and the parameter values
        
    Parameters
    ----------

    gw_file : str
        IWFM Groundwater file name

    verbose : bool, default=False
        Print to screen?

    Returns
    -------
    factors : list
        multiplication factors

    params_d : dictionary of lists
        default model parameters, key = node_layer, value = list of parameter values
    
    """

    params_d = {}
    comments = 'Cc*#'

    with open(gw_file, 'r') as f:
        gw_lines = f.read().splitlines()

    line_index = 10
    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    while gw_lines[line_index][0] not in comments:              # skip file names and units etc
        line_index += 1 

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    line_index += 1                                             # skip KDEB line

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    while gw_lines[line_index][0] not in comments:              # skip hydrograph information
        line_index += 1 

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    while gw_lines[line_index][0] not in comments:              # skip hydrograph lines
        line_index += 1 

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    while gw_lines[line_index][0] not in comments:              # skip face flow control lines
        line_index += 1 

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    line_index += 1                                             # skip NGROUP line

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    factors = [float(x) for x in gw_lines[line_index].split()]  # read factors
    line_index += 1                                             # skip to next line

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    while gw_lines[line_index][0] not in comments:              # skip time units
        line_index += 1 

    while gw_lines[line_index][0] in comments:                  # skip comment lines
        line_index += 1 

    f = open('parvals_keys.txt', 'w')                              # write parameter values to file
    parvals_d = {}                                              # initialize dictionary
    while gw_lines[line_index][0] not in comments:              # process parameter lines
        for l in range(0, nlay):                                # cycle through layers
            items = gw_lines[line_index].split()
            if l == 0:
                node = int(items[0])
                items.pop()

            key = f'{node}_{l+1}'
            parvals_d[key] = [float(x) for x in items]
            f.write(f'  => {node}=\t{l=}\t{key=}\t{parvals_d[key]=}\n')

            line_index += 1 
    f.close()

    f = open('parvals_d.txt', 'w')                              # write parameter values to file
    for key in parvals_d.keys():
        f.write(f'{key} {parvals_d[key]}\n')
    f.close()

    if verbose:     print(f'\n Read {gw_file}')

    return gw_lines, factors, parvals_d

# --------------------------------------------------------------------------------


def read_params(param_types, verbose=False):
    '''  read_params() - Interactively reads parameters for each node and parameter type

    Parameters
    ----------
    verbose : bool, default=False
        Print to screen?

    '''

    import sys
    
    # read new parameter values
    parvals, parnodes, count = [], [], 0
    for ptype in param_types:
        ans = input(f'\n\n Include data for parameter type {ptype}? [y/n] ').lower()

        pvals, pnodes = [], []
        if ans[0] == 'y':

            for layer in range(0, nlay):

                param_file = input(
                    f'\n Parameter value file for parameter type {ptype}, layer {layer+1}, or \'none\': ')

                layer_vals, layer_nodes = [], []
                if param_file == 'none':
                    layer_vals = [-1.0] * nnodes
                    pnodes.append(list(range(1,nnodes+1)))

                else:
                    file_test(param_file)
                    file_lines = open(param_file).read().splitlines()
                    for line in file_lines:
                        text = line.split()
                        layer_nodes.append(int(text[1]))
                        layer_vals.append(float(text[3]))
                    if verbose:
                        print(f'\n Read values for {len(file_lines):,} nodes from {param_file}')
                    count += 1

                pvals.append(layer_vals)
                pnodes.append(layer_nodes)

        else:
            for layer in range(0, nlay):
                pvals.append([-1] * nnodes)
                pnodes.append(list(range(1,nnodes+1)))

        parvals.append(pvals)
        parnodes.append(pnodes)

    f = open('parvals_new.txt', 'w')                              # write parameter values to file
    for item in parvals:
        f.write(f'{item}\n')
    f.close()

    f = open('parnodes.txt', 'w')                              # write parameter values to file
    for item in parnodes:
        f.write(f'{item}\n')
    f.close()

    if verbose:     print(f'\n Read {count} parameter files')

    return parvals, parnodes[0][0]

# --------------------------------------------------------------------------------


def write_gw_file(outfile, gw_lines, nlay, parnodes, parvals, fp, parvals_d, verbose=False):
    '''  write_gw_file() - receive a list of parameters and write them to 
         an IWFM-2015 Groundwater file    
    Parameters
    ----------
    outfile : str
        IWFM Groundwater file name

    gw_lines : list
        each item is one line from the existing (template) Groundwater file

    nlay : int
        Number of model layers

    parnodes : list
        Node numbers corresponding to parvals items

    parvals : list
        New parameter values

    fp : list
        Multiplier factors

    parvals_d : dictionary of lists
        Default parameter values if parvals < 0

    verbose : bool, default=False
        Print to screen?

    '''

    comments = 'Cc*#'

    line_index = 0
    with open(outfile, 'w') as f:

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] not in comments:  # write file names and units etc
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        f.write(f'{gw_lines[line_index]}\n')            # write KDEB line
        line_index += 1 

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] not in comments:  # write hydrograph information
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] not in comments:  # write hydrograph lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] not in comments:  # write face flow control lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        f.write(f'{gw_lines[line_index]}\n')            # write NGROUP line
        line_index += 1 


        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        # write factors
        f.write(f'\t{fp[0]}\t{fp[1]}\t{fp[2]}\t{fp[3]}\t{fp[4]}\t{fp[5]} \n')
        line_index += 1

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] not in comments:  # write time units
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        while gw_lines[line_index][0] in comments:      # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

        f.flush()

        for n in range(0, len(parnodes)):               # cycle through nodes
            for l in range(0, nlay):                    # cycle through layers
                pkh = parvals[0][l][n] if parvals[0][l][n] > 0 else parvals_d[f'{parnodes[n]}_{l+1}'][0]
                pss = parvals[1][l][n] if parvals[1][l][n] > 0 else parvals_d[f'{parnodes[n]}_{l+1}'][1]
                psy = parvals[2][l][n] if parvals[2][l][n] > 0 else parvals_d[f'{parnodes[n]}_{l+1}'][2]
                pkq = parvals[3][l][n] if parvals[3][l][n] > 0 else parvals_d[f'{parnodes[n]}_{l+1}'][3]
                pkv = parvals[4][l][n] if parvals[4][l][n] > 0 else parvals_d[f'{parnodes[n]}_{l+1}'][4]
                if l == 0:
                    f.write(f'\t{parnodes[n]}\t{pkh:.4f}\t{pss:.3E}\t{psy:.3f}\t{pkq:.3E}\t{pkv:.4f}\n')
                else: 
                    f.write(f'\t\t{pkh:.4f}\t{pss:.3E}\t{psy:.3f}\t{pkq:.3E}\t{pkv:.4f}\n')
                line_index += 1 
                f.flush()

        while line_index < len(gw_lines):           # write comment lines
            f.write(f'{gw_lines[line_index]}\n')
            line_index += 1 

    return

# --------------------------------------------------------------------------------



if __name__ == "__main__":
    ''' Run params2gw() from command line '''
    import sys

    verbose = True

    # read arguments from command line
    if len(sys.argv) > 1:  # arguments are listed on the command line
        gw_file          = sys.argv[1]         # Name of existing IWFM Groundwater file
        output_file      = sys.argv[2]         # Name of new IWFM Groundwater file
        nlay             = int(sys.argv[3])    # Number of model layers
        nnodes           = int(sys.argv[4])    # Number of nodes with parameter values

    else:  # get everything form the command line
        gw_file          = input('Name of existing IWFM Groundwater file: ')
        output_file      = input('Name of new IWFM Groundwater file: ')
        nlay             = int(input('Number of model layers: '))
        nnodes           = int(input('Number of nodes with parameter values: '))


    exe_time()  # initialize timer

    # read the existing Groundwater file and parameters
    gw_lines, factors, parvals_d = read_gw_file(gw_file, verbose=verbose)

    # get the new parameter values for nodes
    param_types = ['PKH', 'PS', 'PN', 'PV', 'PL']
    parvals, parnodes = read_params(param_types, verbose=verbose)

    # write the new Groundwater file
    write_gw_file(output_file, gw_lines, nlay, parnodes, parvals, factors, parvals_d, verbose=verbose)

    if verbose:
        print(f'\n\n Created Groundwater file {output_file}. ')
        print( ' All scaling factors from the original file have been preserved. ')
        print( ' Make sure these factors correctly account for the desired scaling.')
    print('\n')

    exe_time()  # print elapsed time


# real2iwfm.py
# Read parameter values for model nodes and combine into an IWFM
# overwrite file
# Copyright (C) 2020-2026 University of California
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


def write_overwrite_file(overwrite_file, in_lines, parnodes, nlay, parvals, fp, ctime, verbose=False):
    '''  write_overwrite_file() - receive a list of parameters and write them to 
         an IWFM-2015 overwrite file    

         From REAL2IGSM.F90 by Matt Tonkin, with modifications by others

    Parameters
    ----------
    overwrite_file : str
        Overwrite file name

    in_lines : list
        each item is one line from the existing (template) overwrite file

    parnodes : list
        Node numbers corresponding to parvals items

    nlay : int
        Number of model layers

    parvals : list
        New parameter values

    fp : list
        Multiplier factors

    ctime : str
        Time step in DSS format

    verbose : bool, default=False
        Print to screen?

    '''

    line_index = 0
    with open(overwrite_file, 'w') as f:

        while in_lines[line_index][0] == 'C':           # write comment lines
            f.write(f'{in_lines[line_index]}\n')
            line_index += 1 

        # write number of parameter lines
        f.write(f'    {len(parnodes[0][0] * nlay)}                       / NWRITE\n')
        line_index += 1

        while in_lines[line_index][0] == 'C':           # write comment lines
            f.write(f'{in_lines[line_index]}\n')
            line_index += 1 

        # write factors
        f.write(f'\t{fp[0]}\t{fp[1]}\t{fp[2]}\t{fp[3]}\t{fp[4]}\t{fp[5]}\t{fp[6]}\n')
        line_index += 1

        while in_lines[line_index][0] == 'C':           # write comment lines
            f.write(f'{in_lines[line_index]}\n')
            line_index += 1 

        # write time units
        f.write(f'    {ctime}               / TUNITKH\n')
        line_index += 1
        for i in range(0,2):                            # write remaining DSS time units
            f.write(f'{in_lines[line_index]}\n')
            line_index += 1 

        while in_lines[line_index][0] == 'C':           # write comment lines
            f.write(f'{in_lines[line_index]}\n')
            line_index += 1 

        for n in range(0, len(parnodes[0][1])):         # cycle through nodes
            for l in range(0, nlay):                    # cycle through layers
                pkh = parvals[0][l][n] if parvals[0][l][n] > 0 else -1
                ps  = parvals[1][l][n] if parvals[1][l][n] > 0 else -1
                pn  = parvals[2][l][n] if parvals[2][l][n] > 0 else -1
                pv  = parvals[3][l][n] if parvals[3][l][n] > 0 else -1
                pl  = parvals[4][l][n] if parvals[4][l][n] > 0 else -1
                sce = parvals[5][l][n] if parvals[5][l][n] > 0 else -1
                sci = parvals[6][l][n] if parvals[6][l][n] > 0 else -1

                f.write(f'\t{parnodes[0][l][n]}\t{l+1}\t{pkh:.4f}\t{ps:.3E}\t{pn:.3f}\t{pv:.3E}\t{pl:.4f}\t{sce:.3E}\t{sci:.3E}\n')

    return
# --------------------------------------------------------------------------------


def read_overwrite_file(overwrite_file, nnodes, nlay, param_types, verbose=False):
    '''  read_overwrite_file() - open and read an IWFM-2015 overwrite file  or 
              overwrite template file, and return the number of nodes, the
                scaling factors, and the parameter values  

         From REAL2IGSM.F90 by Matt Tonkin, with modifications by others

    Parameters
    ----------
    overwrite_file : str
        Overwrite file name

    nnodes : int
        Number of nodes with parameter values

    nlat : int
        Number of model layers

    param_types : list of strs
        Parameter type codes

    verbose : bool, default=False
        Print to screen?

    Returns
    -------
    nwrite : int
        number of parameter lines in overwrite file

    factors : list
        multiplication factors
    
    ctimes : list of strs
        time steps in DSS format

    parvals_d : dict
        parameter values for each node and layer

    in_lines : list
        each item is one line from the overwrite file
    
    '''
    import iwfm

    with open(overwrite_file) as f:
        in_lines = f.read().splitlines()               # open and read input file

    line_index = 0
    line_index = iwfm.skip_ahead(line_index,in_lines,0)               # skip comments 
    nwrite = int(in_lines[line_index].split()[0])                     # no. of parameter lines

    line_index = iwfm.skip_ahead(line_index,in_lines,1)               # skip comments
    factors = [in_lines[line_index].split()[0] for i in range(0,7)]   # scaling factors

    line_index = iwfm.skip_ahead(line_index,in_lines,4)

    line_index = iwfm.skip_ahead(line_index,in_lines,0)

    parvals_d = {}
    for line in in_lines[line_index:]:                                # skip comments
        if line[0] == 'C':
            break
        line = line.split()
        key = f'{line[0]}_{line[1]}'

        temp = {"node": int(line[0]), "layer": int(line[1]), "pkh": float(line[2]), 
                "ps": float(line[3]), "pn": float(line[4]), "pv": float(line[5]), 
                "pl": float(line[6]), "sce": float(line[7]), "sci": float(line[8])}
        parvals_d[key] = temp

    return nwrite, factors, parvals_d, in_lines
# --------------------------------------------------------------------------------



def real2iwfm(verbose=False):
    '''  real2iwfm() - prompts the user for the no. of layers (nlay) in
         and IWFM model application; and the no. of parameter types (ntype)
         for which pilot points have been employed in order to define node
         values. program real2iwfm then prompts for (nlay*ntype) file names
         where each of these files is the output from running program
         ppk2fac_iwfm in order to use pilot points to define nodal parameter
         values. These files are formatted with a header indicating the number
         of nodes that are in the full IWFM application, and the number of nodes
         that are 'informed' by the contents of that file on the basis of
         pilot points. program real2iwfm then concatenates these files, for each
         layer and for each parameter type, into a file compatible with the new
         IWFM external node-value replacement file designed by Can Dogrul.

         From REAL2IGSM.F90 by Matt Tonkin, with modifications by others

    Parameters
    ----------
    verbose : bool, default=False
        Print to screen?

    '''

    import sys
    import iwfm

    param_types = ['PKH', 'PS', 'PN', 'PV', 'PL', 'SCE', 'SCI']
    
    factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]               # factors for scaling parameters = 1.0 unless otherwise specified

    if verbose:
        print(' Program REAL2IWFM reformats the outputs of one or more  ')
        print(' output files from FAC2REALI into a node overwrite file that can ')
        print(' be read by IWFM.')

    overwrite_file = input('\n Name of existing overwrite file: ')
    iwfm.file_test(overwrite_file)

    output_file = input(' Name of new overwrite file: ')

    nlay = int(input( 'Number of model layers: '))

    nnodes = int(input(' Number of nodes with parameter values: '))

    ctime = input(' Parameter time-step units: ')

    nwrite, factors, oldparvals_d, in_lines = read_overwrite_file(
            overwrite_file, nnodes, nlay, param_types, verbose)

    # read new parameter values
    parvals, parnodes = [], []
    for ptype in param_types:
        ans = input(f'\n Include data for parameter type {ptype}? [y/n] ').lower()

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
                    iwfm.file_test(param_file)
                    with open(param_file) as f:
                        file_lines = f.read().splitlines()
                    for line in file_lines:
                        text = line.split()
                        layer_nodes.append(int(text[1]))
                        layer_vals.append(float(text[3]))
                    if verbose:
                        print(f' Read values for {len(file_lines)} nodes from {param_file}')

                pvals.append(layer_vals)
                pnodes.append(layer_nodes)

        else:
            for layer in range(0, nlay):
                pvals.append([-1] * nnodes)
                pnodes.append(list(range(1,nnodes+1)))

        parvals.append(pvals)
        parnodes.append(pnodes)

    write_overwrite_file(output_file, in_lines, parnodes, nlay, parvals, factors, ctime, verbose)

    if verbose:
        print(f'\n\n Created overwrite file {output_file}. ')
        print( ' All scaling factors from the original file have been preserved. ')
        print( ' Make sure these factors correctly account for the desired scaling.')

    return
# --------------------------------------------------------------------------------



if __name__ == "__main__":
    ''' Run real2iwfm() from command line '''
    import iwfm.debug as idb

    idb.exe_time()  # initialize timer
    real2iwfm(verbose=True)
    print('\n')
    idb.exe_time()  # print elapsed time


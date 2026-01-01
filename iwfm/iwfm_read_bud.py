# iwfm_read_bud.py
# Read IWFM Budget main file
# Copyright (C) 2020-2026 University of California
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

def iwfm_read_bud(bud_file, verbose=False):
    ''' iwfm_read_bud() - Read an IWFM Budget main input file, and 
        return a list of lists with the file information and some settings

    Parameters
    ----------
    but_file : str
        Name of IWFM Budget file

    verbose : bool, default=False
        Turn command-line output on or off
            
     Returns
    -------
    budget_list : list of lists
        Input and output file names, times etc

    '''
    import iwfm as iwfm

    with open(bud_file) as f:
        bud_lines = f.read().splitlines()

    line_index = iwfm.skip_ahead(0, bud_lines, 0)  # skip comments

    # read factors and labels
    factlou = float(bud_lines[line_index].split()[0])
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    unutlou=  bud_lines[line_index].split()[0]
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    factarou = float(bud_lines[line_index].split()[0])
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    unitarou = bud_lines[line_index].split()[0]
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    factvolou = float(bud_lines[line_index].split()[0])
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    unitvolou = bud_lines[line_index].split()[0]
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    cache = bud_lines[line_index].split()[0]
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    # read begin and end dates
    bdt = bud_lines[line_index].split()[0]
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    edt = bud_lines[line_index].split()[0]
    line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  

    # number of budgets to process
    nbudget = int(bud_lines[line_index].split()[0])
    
    factors = [nbudget, factlou, unutlou, factarou, unitarou, factvolou, unitvolou, bdt, edt]

    budget_list = []
    for b in range(nbudget):
        line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  
        hdffile = bud_lines[line_index].split()[0]

        line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  
        outfile = bud_lines[line_index].split()[0]

        line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  
        intprnt = bud_lines[line_index].split()[0]

        line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  
        nlprint = bud_lines[line_index].split()[0]

        line_index = iwfm.skip_ahead(line_index + 1, bud_lines, 0)  
        lprint = bud_lines[line_index].split()[0]

        budget_list.append([hdffile, outfile, intprnt, nlprint, lprint])

    return budget_list, factors



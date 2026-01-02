# iwfm_read_rz_pc.py
# Read ponded crop data from a file and organize them into lists
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


def iwfm_read_rz_pc(file, verbose=False):
    """iwfm_read_rz_pc() - Read ponded crop data from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the ponded crop data.
  
    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------

    crops : list
        A list of crop codes
    
    params : list
        A list of parameters: [cn, et, wsp, ip, pd, ad, rf, ru, ic]

    files : list
        A list of file names: [pc_area_file, pc_bd_file, pc_zb_file, pc_rd_file, pc_ms_file, pc_ts_file, pc_md_file]

    """
    import iwfm as iwfm

    npcrops = 5                                                 # number of ponded crop types (may be variable in future IWFM versions)

    if verbose: print(f"Entered iwfm_read_rz_pc() with {file}")

    with open(file) as f:
        pc_lines = f.read().splitlines()                   # open and read input file

    line_index = iwfm.skip_ahead(0, pc_lines, 0)                # skip to number of crop types
    pc_area_file = pc_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)   # skip to next value line
    nbcrop = int(pc_lines[line_index].split()[0])               # number of crop-specific budget files to produce

    budfiles = []
    for i in range(nbcrop):
        line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)
        budfiles.append(pc_lines[line_index].split()[0])                # read budget file names

    line_index = iwfm.skip_ahead(line_index + 1 + nbcrop, pc_lines, 0)  # skip to budget file names
    pc_bd_file = pc_lines[line_index].split()[0]                        # read crop budget file name

    line_index = iwfm.skip_ahead(line_index + 1 + nbcrop, pc_lines, 0)  # skip to budget file names
    pc_zb_file = pc_lines[line_index].split()[0]                        # read crop zbudget fractions file name

    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip budget file names
    fact = float(pc_lines[line_index].split()[0])                       # root zone depth conversion factor
    rzdepths = []
    for i in range(npcrops):
        line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line
        rzdepths.append(float(pc_lines[line_index].split()[0]) * fact)      # read root zone depths


    # how many elements?
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line
    ne = 0
    while (line_index + ne < len(pc_lines) and
           pc_lines[line_index+(ne)].split()[0] != 'C'):
        ne += 1

    if line_index + ne >= len(pc_lines):
        raise ValueError(
            f"'C' marker not found while counting ponded crop elements at line {line_index}"
        )

    ne -= 1                                                             # one to convert to zero index

    # curve numbers
    cn, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    # ET
    et, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    # ag water supply requirement
    wsp, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    # irrigation period
    ip, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    # rice and refuge operations input files
    pc_pd_file = pc_lines[line_index].split()[0]                        # read ponding depths file name
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    pc_po_file = pc_lines[line_index].split()[0]                        # read ponding operations file name
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    pd, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)    # read ponding depth column numbers
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    ad, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)    # read application depth column numbers
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    rf, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)    # read return flow depth column numbers
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    ru, line_index = iwfm.iwfm_read_param_table_ints(pc_lines, line_index, ne)    # read reuse flow depth column numbers
    line_index = iwfm.skip_ahead(line_index + 1, pc_lines, 0)           # skip to next value line

    # initial condition
    ic, line_index = iwfm.iwfm_read_param_table_floats(pc_lines, line_index, ne)

    crops = ['ri_n', 'ri_f', 'ri_d', 'rf_sl', 'rf_pr']
    params = [cn, et, wsp, ip, pd, ad, rf, ru, ic]
    files = [pc_area_file, pc_bd_file, pc_zb_file, pc_pd_file, pc_po_file]

        
    if verbose: print(f"Leaving iwfm_read_rz_pc()")

    return crops, params, files
